#!/usr/bin/env python3
"""Offline ASS visual-profile extraction; never translates subtitle text."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

SCRIPT_FIELDS = {'PlayResX', 'PlayResY', 'WrapStyle', 'ScaledBorderAndShadow', 'YCbCr Matrix'}
COLOR_FIELDS = {'PrimaryColour', 'SecondaryColour', 'OutlineColour', 'BackColour'}
ASS_TAG = re.compile(r'\{\\[^}]*\}')
SRT_TIME = re.compile(r'(\d{2,}):(\d{2}):(\d{2}),(\d{3})')
HTML_TAG = re.compile(r'</?[A-Za-z][^>]*>')
DEFAULT_STYLE = dict(zip(
    ('Name', 'Fontname', 'Fontsize', 'PrimaryColour', 'SecondaryColour', 'OutlineColour',
     'BackColour', 'Bold', 'Italic', 'Underline', 'StrikeOut', 'ScaleX', 'ScaleY', 'Spacing',
     'Angle', 'BorderStyle', 'Outline', 'Shadow', 'Alignment', 'MarginL', 'MarginR', 'MarginV', 'Encoding'),
    ('Default', 'Calibri', '64', '&H00FFFFFF', '&H000000FF', '&H00101010', '&H96000000',
     '-1', '0', '0', '0', '100', '100', '0', '0', '1', '3.2', '1.5', '2', '150', '150', '55', '178')))


def _srt_centiseconds(value):
    match = SRT_TIME.fullmatch(value)
    if not match:
        raise ValueError('Invalid SRT timestamp')
    hours, minutes, seconds, millis = map(int, match.groups())
    if minutes > 59 or seconds > 59:
        raise ValueError('Invalid SRT timestamp')
    return ((hours * 3600 + minutes * 60 + seconds) * 1000 + millis + 5) // 10


def _ass_time(value):
    hours, rest = divmod(value, 360000)
    minutes, rest = divmod(rest, 6000)
    seconds, centiseconds = divmod(rest, 100)
    return f'{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}'


def _srt_tags(text):
    tags = HTML_TAG.findall(text)
    stack = []
    for tag in tags:
        if not re.fullmatch(r'</?[biu]>', tag, re.IGNORECASE):
            raise ValueError('Unsupported SRT markup')
        tag = tag.lower()
        if tag.startswith('</'):
            if not stack or stack.pop() != tag[2]:
                raise ValueError('Unbalanced SRT markup')
        else:
            stack.append(tag[1])
    if stack:
        raise ValueError('Unbalanced SRT markup')
    return [tag.lower() for tag in tags]


def _convert_srt_tags(text, style):
    defaults = {'b': style['Bold'], 'i': style['Italic'], 'u': style['Underline']}
    stack = []
    def convert(match):
        tag = match.group().lower()
        letter = tag[2] if tag.startswith('</') else tag[1]
        if tag.startswith('</'):
            stack.pop()
            enabled = letter in stack or int(defaults[letter]) != 0
        else:
            stack.append(letter)
            enabled = True
        return '{\\' + letter + ('1' if enabled else '0') + '}'
    return HTML_TAG.sub(convert, text)


def parse_srt(source):
    """Parse strict SRT blocks and quantize to ASS centiseconds; fail closed."""
    blocks = re.split(r'\n[ \t]*\n', source.replace('\r\n', '\n').replace('\r', '\n').strip())
    events = []
    for number, block in enumerate(blocks, 1):
        lines = block.split('\n')
        if len(lines) < 3 or not lines[0].strip().isdigit() or not lines[2:]:
            raise ValueError(f'Malformed SRT block {number}')
        timing = re.fullmatch(r'\s*(\S+)\s+-->\s+(\S+)\s*', lines[1])
        if not timing:
            raise ValueError(f'Malformed timing in SRT block {number}')
        start, end = (_srt_centiseconds(value) for value in timing.groups())
        if end <= start:
            raise ValueError(f'SRT block {number} cannot be represented after rounding')
        text = r'\N'.join(lines[2:])
        if not text.strip():
            raise ValueError(f'Empty SRT block {number}')
        if re.search(r'\{\\[^}]*\}', text):
            raise ValueError(f'SRT markup in block {number} requires manual preservation')
        _srt_tags(text)
        rounded = any(int(value[-3:]) % 10 for value in timing.groups())
        events.append({'start': _ass_time(start), 'end': _ass_time(end), 'text': text, 'rounded': rounded})
    return events


def _ass_event_lines(source):
    lines = source.splitlines(keepends=True)
    section = ''
    fields = None
    event_lines = []
    for index, raw in enumerate(lines):
        line = raw.rstrip('\r\n')
        stripped = line.strip()
        if stripped.startswith('[') and stripped.endswith(']'):
            section = stripped.lower()
        elif section == '[events]' and ':' in line:
            key, value = line.split(':', 1)
            if key.strip().lower() == 'format':
                fields = [field.strip().lower() for field in value.split(',')]
                if (not fields or fields[-1] != 'text' or len(set(fields)) != len(fields)
                        or not {'start', 'end', 'style'} <= set(fields)):
                    raise ValueError('ASS event Format must have unique fields and Text last')
            elif key.strip().lower() == 'dialogue':
                if not fields:
                    raise ValueError('ASS dialogue before event Format')
                parts = value.split(',', len(fields) - 1)
                if len(parts) != len(fields) or not parts[-1].strip():
                    raise ValueError(f'Malformed ASS dialogue at line {index + 1}')
                times = []
                for field in ('start', 'end'):
                    match = re.fullmatch(r'(\d+):([0-5]\d):([0-5]\d)\.(\d{2})', parts[fields.index(field)].strip())
                    if not match:
                        raise ValueError(f'Invalid ASS time at line {index + 1}')
                    h, m, s, cs = map(int, match.groups())
                    times.append(((h * 60 + m) * 60 + s) * 100 + cs)
                if times[1] <= times[0]:
                    raise ValueError(f'Invalid ASS time range at line {index + 1}')
                event_lines.append((index, key, parts, raw[len(line):], parts[fields.index('style')].strip()))
    if not event_lines:
        raise ValueError('No ASS dialogue events found')
    return lines, event_lines


def assemble_ass(source, translations):
    """Replace dialogue text only, requiring one translation and matching tags per event."""
    lines, event_lines = _ass_event_lines(source)
    if len(event_lines) != len(translations):
        raise ValueError('Translation count does not match dialogue count')
    for (index, key, parts, newline, _style), translation in zip(event_lines, translations):
        if not isinstance(translation, str) or not translation.strip() or '\n' in translation or '\r' in translation:
            raise ValueError('Translation must be nonempty and contain no raw newlines')
        if ASS_TAG.findall(parts[-1]) != ASS_TAG.findall(translation):
            raise ValueError('ASS override tags must be preserved in order')
        parts[-1] = translation
        lines[index] = key + ':' + ','.join(parts) + newline
    return ''.join(lines)


def merge_profile(reference, overrides):
    """Merge explicit settings over reference and defaults; validate supported fields."""
    if not isinstance(reference, dict) or not isinstance(overrides, dict):
        raise ValueError('Profile must be an object')
    style = dict(DEFAULT_STYLE)
    info = {'PlayResX': '1920', 'PlayResY': '1080', 'WrapStyle': '0', 'ScaledBorderAndShadow': 'yes'}
    for profile in (reference, overrides):
        if set(profile) - {'script_info', 'styles'}:
            raise ValueError('Unknown profile fields')
        script = profile.get('script_info', {})
        styles = profile.get('styles', [])
        if not isinstance(script, dict) or not isinstance(styles, list) or (styles and not isinstance(styles[0], dict)):
            raise ValueError('Invalid profile structure')
        if set(script) - SCRIPT_FIELDS or (styles and set(styles[0]) - set(DEFAULT_STYLE)):
            raise ValueError('Unknown profile settings')
        info.update(script)
        if styles:
            style.update(styles[0])
    for key, value in style.items():
        if not isinstance(value, str) or not value.strip() or any(c in value for c in ',\r\n'):
            raise ValueError(f'Invalid style field {key}')
        if key in COLOR_FIELDS and not re.fullmatch(r'&H[0-9A-Fa-f]{1,8}&?', value):
            raise ValueError(f'Invalid {key}')
    for key in ('Fontsize', 'ScaleX', 'ScaleY', 'Outline', 'Shadow', 'Spacing', 'Angle'):
        try:
            number = float(style[key])
        except ValueError:
            raise ValueError(f'Invalid {key}') from None
        if not math.isfinite(number) or (key in ('Fontsize', 'ScaleX', 'ScaleY') and number <= 0) or (key in ('Outline', 'Shadow') and number < 0):
            raise ValueError(f'Invalid {key}')
    for key in ('Bold', 'Italic', 'Underline', 'StrikeOut', 'BorderStyle', 'Alignment', 'MarginL', 'MarginR', 'MarginV', 'Encoding'):
        if not re.fullmatch(r'-?\d+', style[key]):
            raise ValueError(f'Invalid {key}')
    for key in ('MarginL', 'MarginR', 'MarginV'):
        if int(style[key]) < 0:
            raise ValueError(f'Invalid {key}')
    if int(style['Alignment']) not in range(1, 10) or int(style['BorderStyle']) not in (1, 3):
        raise ValueError('Invalid Alignment or BorderStyle')
    for key, value in info.items():
        if not isinstance(value, str) or not value or any(c in value for c in '\r\n'):
            raise ValueError(f'Invalid {key}')
        if key in ('PlayResX', 'PlayResY') and (not value.isdigit() or int(value) <= 0):
            raise ValueError(f'Invalid {key}')
    if info.get('WrapStyle') not in ('0', '1', '2', '3'):
        raise ValueError('Invalid WrapStyle')
    if info.get('ScaledBorderAndShadow', '').lower() not in ('yes', 'no'):
        raise ValueError('Invalid ScaledBorderAndShadow')
    return {'script_info': info, 'styles': [style]}


def restyle_ass(source, profile):
    """Apply a style to a single-style ASS on the same canvas without touching events."""
    source_profile = extract_profile(source)
    if len(source_profile['styles']) != 1:
        raise ValueError('ASS restyling requires one source style; multiple styles need manual mapping')
    supplied_info = profile.get('script_info', {})
    original_info = source_profile['script_info']
    for dimension in ('PlayResX', 'PlayResY'):
        if dimension not in supplied_info or dimension not in original_info or supplied_info[dimension] != original_info[dimension]:
            raise ValueError('ASS source and reference resolution must match for safe positioning')
    chosen = merge_profile(profile, {})['styles'][0]
    lines = source.splitlines(keepends=True)
    section = ''
    fields = None
    changed = 0
    for index, raw in enumerate(lines):
        line = raw.rstrip('\r\n')
        stripped = line.strip()
        if stripped.startswith('[') and stripped.endswith(']'):
            section = stripped.lower()
        elif section == '[v4+ styles]' and ':' in line:
            key, value = line.split(':', 1)
            if key.strip().lower() == 'format':
                fields = [item.strip() for item in value.split(',')]
            elif key.strip().lower() == 'style':
                if not fields or any(field not in DEFAULT_STYLE for field in fields):
                    raise ValueError('Unsupported ASS style fields')
                values = [item.strip() for item in value.split(',')]
                if len(values) != len(fields):
                    raise ValueError('Malformed ASS style')
                original = dict(zip(fields, values))
                style = [original['Name'] if field == 'Name' else chosen[field] for field in fields]
                lines[index] = key + ': ' + ','.join(style) + raw[len(line):]
                changed += 1
    if changed != 1:
        raise ValueError('Cannot identify the single source style')
    return ''.join(lines)


def srt_to_ass(events, translations, profile):
    """Assemble translated SRT events using a reference style; does not translate."""
    if not events or len(events) != len(translations):
        raise ValueError('Translation count does not match event count')
    if not profile.get('styles'):
        raise ValueError('Profile has no styles')
    merged = merge_profile(profile, {})
    style = merged['styles'][0]
    info = merged['script_info']
    rows = ['[Script Info]', 'ScriptType: v4.00+']
    rows.extend(f'{key}: {value}' for key, value in info.items())
    rows.extend(['', '[V4+ Styles]', 'Format: ' + ', '.join(style),
                 'Style: ' + ','.join(style.values()), '', '[Events]',
                 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text'])
    for event, translation in zip(events, translations):
        if not isinstance(translation, str) or not translation.strip() or '\n' in translation or '\r' in translation:
            raise ValueError('Translation must be nonempty and contain no raw newlines')
        if _srt_tags(event['text']) != _srt_tags(translation):
            raise ValueError('SRT markup must be preserved in order')
        translation = _convert_srt_tags(translation, style)
        rows.append(f"Dialogue: 0,{event['start']},{event['end']},{style['Name']},,0,0,0,,{translation}")
    return '\n'.join(rows) + '\n'


def extract_profile(source):
    """Extract declared styles and visual script settings, excluding all events."""
    section = ''
    fields = None
    info = {}
    styles = []
    for line_number, raw in enumerate(source.splitlines(), 1):
        line = raw.strip()
        if line.startswith('[') and line.endswith(']'):
            section = line.lower()
            continue
        if ':' not in line or line.startswith(';'):
            continue
        key, value = (part.strip() for part in line.split(':', 1))
        if section == '[script info]' and key in SCRIPT_FIELDS:
            info[key] = value
        elif section == '[v4+ styles]' and key.lower() == 'format':
            fields = [part.strip() for part in value.split(',')]
            if not fields or len(set(fields)) != len(fields) or 'Name' not in fields:
                raise ValueError(f'Invalid style Format at line {line_number}')
        elif section == '[v4+ styles]' and key.lower() == 'style':
            if fields is None:
                raise ValueError(f'Style before Format at line {line_number}')
            values = [part.strip() for part in value.split(',')]
            if len(values) != len(fields):
                raise ValueError(f'Style field count mismatch at line {line_number}')
            style = dict(zip(fields, values))
            for color in COLOR_FIELDS & style.keys():
                if not re.fullmatch(r'&H[0-9A-Fa-f]{1,8}&?', style[color]):
                    raise ValueError(f'Invalid {color} at line {line_number}')
            styles.append(style)
    if not styles:
        raise ValueError('No ASS V4+ styles found')
    for dimension in ('PlayResX', 'PlayResY'):
        if dimension in info and (not info[dimension].isdigit() or int(info[dimension]) <= 0):
            raise ValueError(f'Invalid {dimension}')
    return {'script_info': info, 'styles': styles}


def validate_ass(source):
    """Check event records and their style references; not a full renderer validation."""
    styles = [style['Name'] for style in extract_profile(source)['styles']]
    if len(styles) != len(set(styles)):
        raise ValueError('Duplicate ASS style names')
    events = _ass_event_lines(source)[1]
    for index, _key, _parts, _newline, style in events:
        if style not in styles:
            raise ValueError(f'Undefined ASS style at line {index + 1}')
    return len(events)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    extract = commands.add_parser('extract', help='Print a visual profile as JSON')
    extract.add_argument('reference', type=Path, help='ASS reference file (UTF-8 or UTF-8 BOM)')
    checkpoint = commands.add_parser('checkpoint', help='Create an empty resumable translation checkpoint')
    checkpoint.add_argument('source', type=Path)
    checkpoint.add_argument('target_language')
    checkpoint.add_argument('output', type=Path, help='New checkpoint JSON file; never overwritten')
    checkpoint.add_argument('--dialect', default='')
    assemble = commands.add_parser('assemble', help='Assemble agent-authored translations')
    assemble.add_argument('source', type=Path)
    assemble.add_argument('translations', type=Path, help='JSON array of translated event strings')
    assemble.add_argument('output', type=Path, help='New ASS file; never overwritten')
    assemble.add_argument('--reference', type=Path, help='ASS reference for SRT conversion')
    assemble.add_argument('--profile', type=Path, help='JSON settings overriding reference values for SRT conversion')
    args = parser.parse_args(argv)
    try:
        if args.command == 'extract':
            profile = extract_profile(args.reference.read_text(encoding='utf-8-sig'))
            json.dump(profile, sys.stdout, ensure_ascii=False, indent=2)
            print()
            return
        source_bytes = args.source.read_bytes()
        source = source_bytes.decode('utf-8-sig')
        suffix = args.source.suffix.lower()
        if args.command == 'checkpoint':
            if not args.target_language.strip():
                raise ValueError('Target language must not be empty')
            if suffix == '.srt':
                count = len(parse_srt(source))
            elif suffix == '.ass':
                count = len(_ass_event_lines(source)[1])
            else:
                raise ValueError('Source must be .srt or .ass')
            data = {'schema': 1, 'source_sha256': hashlib.sha256(source_bytes).hexdigest(),
                    'source_name': args.source.name, 'output_path': None,
                    'target_language': args.target_language, 'dialect': args.dialect,
                    'translations': [None] * count, 'unresolved': []}
            with args.output.open('x', encoding='utf-8', newline='\n') as output:
                json.dump(data, output, ensure_ascii=False, indent=2)
                output.write('\n')
            print(f'Created incomplete checkpoint for {count} events at {args.output}.')
            return
        translations = json.loads(args.translations.read_text(encoding='utf-8-sig'))
        unresolved_count = None
        if isinstance(translations, dict):
            if translations.get('schema') != 1 or translations.get('source_sha256') != hashlib.sha256(source_bytes).hexdigest():
                raise ValueError('Checkpoint source identity does not match')
            if not isinstance(translations.get('target_language'), str) or not translations['target_language'].strip():
                raise ValueError('Checkpoint target language is missing')
            unresolved = translations.get('unresolved', [])
            if not isinstance(unresolved, list):
                raise ValueError('Checkpoint unresolved items must be an array')
            unresolved_count = len(unresolved)
            translations = translations.get('translations')
            if not isinstance(translations, list) or any(not isinstance(item, str) or not item.strip() for item in translations):
                raise ValueError('Checkpoint is partial; every event needs a translation')
        if not isinstance(translations, list):
            raise ValueError('Translations must be a JSON array or checkpoint')
        rounded_count = None
        if suffix == '.srt':
            profile = (extract_profile(args.reference.read_text(encoding='utf-8-sig'))
                       if args.reference else {'styles': [DEFAULT_STYLE]})
            if args.profile:
                profile = merge_profile(profile, json.loads(args.profile.read_text(encoding='utf-8-sig')))
            events = parse_srt(source)
            rounded_count = sum(event['rounded'] for event in events)
            result = srt_to_ass(events, translations, profile)
        elif suffix == '.ass':
            result = assemble_ass(source, translations)
            if args.reference or args.profile:
                reference = (extract_profile(args.reference.read_text(encoding='utf-8-sig'))
                             if args.reference else extract_profile(source))
                override = json.loads(args.profile.read_text(encoding='utf-8-sig')) if args.profile else {}
                declared = dict(reference.get('script_info', {}))
                if isinstance(override, dict) and isinstance(override.get('script_info', {}), dict):
                    declared.update(override.get('script_info', {}))
                if not {'PlayResX', 'PlayResY'} <= declared.keys():
                    raise ValueError('Reference or profile resolution must be declared for ASS restyling')
                result = restyle_ass(result, merge_profile(reference, override))
        else:
            raise ValueError('Source must be .srt or .ass')
        if validate_ass(result) != len(translations):
            raise ValueError('Output event count does not match translation count')
        with args.output.open('x', encoding='utf-8-sig', newline='') as output:
            output.write(result)
        unresolved_note = f'; {unresolved_count} unresolved items' if unresolved_count is not None else ''
        rounding_note = f'; {rounded_count} events rounded to centiseconds' if rounded_count is not None else ''
        print(f'Wrote {len(translations)} events to {args.output}{rounding_note}{unresolved_note}; visual and semantic review required.')
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f'Cannot process subtitles: {error}\n')


if __name__ == '__main__':
    main()
