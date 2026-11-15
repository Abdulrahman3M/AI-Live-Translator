import importlib.util
import pathlib
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[4]
PATH = ROOT / 'skills/subtitle-translator/scripts/subtitle_tools.py'


class SubtitleToolsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not PATH.exists():
            return
        spec = importlib.util.spec_from_file_location('subtitle_tools', PATH)
        cls.tool = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.tool)

    def test_extracts_reference_using_declared_fields_without_dialogue(self):
        self.assertTrue(PATH.exists(), 'subtitle style extraction helper is missing')
        source = '''[Script Info]\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 0\n[V4+ Styles]\nFormat: Name, Fontsize, Fontname, PrimaryColour, Outline, Alignment\nStyle: Default,64,Calibri,&H00FFFFFF,3.2,2\n[Events]\nFormat: Layer, Text\nDialogue: 0,private dialogue\n'''
        profile = self.tool.extract_profile(source)
        self.assertEqual(profile['script_info']['PlayResX'], '1920')
        self.assertEqual(profile['styles'][0]['Fontname'], 'Calibri')
        self.assertNotIn('private dialogue', str(profile))

    def test_alternate_reference_and_invalid_color(self):
        self.assertTrue(PATH.exists(), 'subtitle style extraction helper is missing')
        reference = '''[Script Info]\nPlayResX: 1280\nPlayResY: 720\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour\nStyle: Default,Arial,42,&H0000FFFF\n'''
        profile = self.tool.extract_profile(reference)
        self.assertEqual(profile['styles'][0]['Fontsize'], '42')
        self.assertEqual(profile['script_info']['PlayResX'], '1280')
        with self.assertRaisesRegex(ValueError, 'PrimaryColour'):
            self.tool.extract_profile(reference.replace('&H0000FFFF', 'yellow'))

    def test_ass_translation_preserves_metadata_commas_and_overrides(self):
        source = ('[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
                  r'Dialogue: 2,0:00:01.00,0:00:03.00,Default,A,0,0,0,fx,{\pos(100,200)}Hello, friend' '\n'
                  'Dialogue: 0,0:00:02.00,0:00:04.00,Default,,0,0,0,,Second\n')
        output = self.tool.assemble_ass(source, [r'{\pos(100,200)}مرحبا، صديقي', 'الثاني'])
        self.assertIn(r'Dialogue: 2,0:00:01.00,0:00:03.00,Default,A,0,0,0,fx,{\pos(100,200)}مرحبا، صديقي', output)
        self.assertIn('0:00:02.00,0:00:04.00', output)
        with self.assertRaisesRegex(ValueError, 'override'):
            self.tool.assemble_ass(source, ['مرحبا', 'الثاني'])
        with self.assertRaisesRegex(ValueError, 'count'):
            self.tool.assemble_ass(source, ['مرحبا'])

    def test_srt_rounding_and_rejects_unrepresentable_or_malformed(self):
        source = '1\n00:00:01,005 --> 00:00:02,014\nHello, world\n\n2\n00:00:01,900 --> 00:00:03,000\nSecond line\n'
        events = self.tool.parse_srt(source)
        self.assertEqual([(e['start'], e['end']) for e in events], [('0:00:01.01', '0:00:02.01'), ('0:00:01.90', '0:00:03.00')])
        self.assertEqual(events[0]['text'], 'Hello, world')
        with self.assertRaisesRegex(ValueError, 'represent'):
            self.tool.parse_srt('1\n00:00:01,001 --> 00:00:01,004\nHi\n')
        with self.assertRaisesRegex(ValueError, 'block'):
            self.tool.parse_srt('1\nnot a timing\nHi\n')

    def test_srt_ass_assembly_uses_reference_and_translations(self):
        reference = ('[Script Info]\nPlayResX: 1280\nPlayResY: 720\nWrapStyle: 0\n'
                     '[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour\n'
                     'Style: Default,Arial,42,&H0000FFFF\n')
        events = self.tool.parse_srt('1\n00:00:01,005 --> 00:00:02,014\nHello\n')
        result = self.tool.srt_to_ass(events, ['مرحبا، صديق'], self.tool.extract_profile(reference))
        self.assertIn('PlayResX: 1280', result)
        self.assertIn('Style: Default,Arial,42,&H0000FFFF,', result)
        self.assertIn('Dialogue: 0,0:00:01.01,0:00:02.01,Default,,0,0,0,,مرحبا، صديق', result)
        with self.assertRaisesRegex(ValueError, 'count'):
            self.tool.srt_to_ass(events, [], self.tool.extract_profile(reference))

    def test_cli_assembles_bom_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / 'input.srt'
            translated = root / 'translations.json'
            output = root / 'result.ass'
            source.write_text('1\n00:00:01,005 --> 00:00:02,014\nHello\n', encoding='utf-8')
            translated.write_text(json.dumps(['مرحبا'], ensure_ascii=False), encoding='utf-8')
            command = [sys.executable, str(PATH), 'assemble', str(source), str(translated), str(output)]
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('1 events rounded', result.stdout)
            self.assertTrue(output.read_bytes().startswith(b'\xef\xbb\xbf'))
            self.assertIn('مرحبا', output.read_text(encoding='utf-8-sig'))
            again = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
            self.assertNotEqual(again.returncode, 0)
            self.assertIn('exists', again.stderr.lower())

    def test_rejects_srt_markup_that_would_be_lost_and_invalid_ass_time(self):
        with self.assertRaisesRegex(ValueError, 'markup'):
            self.tool.parse_srt('1\n00:00:01,000 --> 00:00:02,000\n<font color="red">Quiet</font>\n')
        source = ('[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
                  'Dialogue: 0,broken,0:00:02.00,Default,,0,0,0,,Hi\n')
        with self.assertRaisesRegex(ValueError, 'time'):
            self.tool.assemble_ass(source, ['أهلًا'])

    def test_srt_italic_span_survives_without_styling_adjacent_dialogue(self):
        source = '1\n00:00:01,000 --> 00:00:03,000\n<i>[Door closes]</i> Hello\n'
        events = self.tool.parse_srt(source)
        result = self.tool.srt_to_ass(events, ['<i>[يُغلق الباب]</i> أهلًا'], {'styles': [self.tool.DEFAULT_STYLE]})
        self.assertIn(r'{\i1}[يُغلق الباب]{\i0} أهلًا', result)
        with self.assertRaisesRegex(ValueError, 'markup'):
            self.tool.srt_to_ass(events, ['[يُغلق الباب] أهلًا'], {'styles': [self.tool.DEFAULT_STYLE]})

    def test_explicit_profile_overrides_reference_and_invalid_values_fail(self):
        reference = {'script_info': {'PlayResX': '1280'}, 'styles': [{'Name': 'Default', 'Fontname': 'Arial', 'Fontsize': '42'}]}
        override = {'script_info': {'PlayResX': '1920'}, 'styles': [{'Fontsize': '60'}]}
        profile = self.tool.merge_profile(reference, override)
        self.assertEqual(profile['script_info']['PlayResX'], '1920')
        self.assertEqual(profile['styles'][0]['Fontname'], 'Arial')
        self.assertEqual(profile['styles'][0]['Fontsize'], '60')
        with self.assertRaisesRegex(ValueError, 'Fontsize'):
            self.tool.merge_profile(reference, {'styles': [{'Fontsize': '-2'}]})
        with self.assertRaisesRegex(ValueError, 'WrapStyle'):
            self.tool.merge_profile(reference, {'script_info': {'WrapStyle': '9'}})

    def test_synthetic_fixture_preserves_overlap_and_line_breaks(self):
        examples = ROOT / 'skills/subtitle-translator/examples'
        events = self.tool.parse_srt((examples / 'sample.srt').read_text(encoding='utf-8'))
        translations = json.loads((examples / 'sample-translations.json').read_text(encoding='utf-8'))
        profile = self.tool.extract_profile((examples / 'sample-reference.ass').read_text(encoding='utf-8'))
        result = self.tool.srt_to_ass(events, translations, profile)
        rows = [line for line in result.splitlines() if line.startswith('Dialogue:')]
        self.assertEqual(len(rows), 2)
        self.assertIn('0:00:01.01,0:00:03.00', rows[0])
        self.assertIn('0:00:02.50,0:00:04.00', rows[1])
        self.assertIn(r'\N', rows[1])
        expected = examples / 'sample-expected.ass'
        self.assertTrue(expected.exists(), 'Synthetic expected output is missing')
        self.assertEqual(result, expected.read_text(encoding='utf-8-sig'))

    def test_restyle_ass_preserves_events_and_requires_matching_canvas(self):
        source = ('[Script Info]\nPlayResX: 1280\nPlayResY: 720\n'
                  '[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour\n'
                  'Style: Dialogue,Old,30,&H00FFFFFF\n'
                  '[Events]\nFormat: Layer, Start, End, Style, Text\n'
                  r'Dialogue: 2,0:00:01.00,0:00:03.00,Dialogue,{\pos(10,20)}Hi, Sam' '\n')
        profile = {'script_info': {'PlayResX': '1280', 'PlayResY': '720'},
                   'styles': [{'Name': 'Default', 'Fontname': 'Arial', 'Fontsize': '42'}]}
        output = self.tool.restyle_ass(source, profile)
        self.assertIn('Style: Dialogue,Arial,42,', output)
        self.assertEqual(output.split('[Events]')[1], source.split('[Events]')[1])
        profile['script_info']['PlayResX'] = '1920'
        with self.assertRaisesRegex(ValueError, 'resolution'):
            self.tool.restyle_ass(source, profile)

    def test_mixed_direction_music_and_effect_tags_survive_assembly(self):
        source = ('[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
                  r'Dialogue: 0,0:00:01.00,0:00:04.00,Default,,0,0,0,,{\i1}♪ Music ♪{\i0}\NTrain 42, Maya' '\n')
        translated = r'{\i1}♪ موسيقى ♪{\i0}\Nقطار City 42، مايا'
        result = self.tool.assemble_ass(source, [translated])
        self.assertTrue(result.rstrip().endswith(translated))
        self.assertIn(r'{\i0}\N', result)

    def test_restyle_rejects_multiple_source_styles(self):
        source = ('[Script Info]\nPlayResX: 1280\nPlayResY: 720\n[V4+ Styles]\n'
                  'Format: Name, Fontname, Fontsize\nStyle: Default,Arial,42\nStyle: Effects,Arial,42\n')
        profile = {'script_info': {'PlayResX': '1280', 'PlayResY': '720'}, 'styles': [{'Name': 'Default'}]}
        with self.assertRaisesRegex(ValueError, 'multiple styles'):
            self.tool.restyle_ass(source, profile)

    def test_cli_restyle_refuses_reference_with_unknown_resolution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / 'source.ass'
            source.write_text('[Script Info]\nPlayResX: 1920\nPlayResY: 1080\n[V4+ Styles]\nFormat: Name, Fontname\nStyle: Default,Arial\n[Events]\nFormat: Start, End, Style, Text\nDialogue: 0:00:01.00,0:00:02.00,Default,Hi\n', encoding='utf-8')
            reference = root / 'reference.ass'
            reference.write_text('[V4+ Styles]\nFormat: Name, Fontname\nStyle: Default,Arial\n', encoding='utf-8')
            translated = root / 'translations.json'
            translated.write_text(json.dumps(['أهلًا']), encoding='utf-8')
            output = root / 'result.ass'
            result = subprocess.run([sys.executable, str(PATH), 'assemble', str(source), str(translated), str(output), '--reference', str(reference)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('resolution', result.stderr.lower())
            self.assertFalse(output.exists())

    def test_validation_rejects_undefined_ass_style(self):
        source = ('[V4+ Styles]\nFormat: Name, Fontname\nStyle: Default,Arial\n'
                  '[Events]\nFormat: Start, End, Style, Text\n'
                  'Dialogue: 0:00:01.00,0:00:02.00,Missing,Hi\n')
        with self.assertRaisesRegex(ValueError, 'style'):
            self.tool.validate_ass(source)

    def test_checkpoint_rejects_partial_and_changed_source(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            source = root / 'input.srt'
            checkpoint = root / 'checkpoint.json'
            output = root / 'result.ass'
            source.write_text('1\n00:00:01,000 --> 00:00:02,000\nHello\n', encoding='utf-8')
            init = subprocess.run([sys.executable, str(PATH), 'checkpoint', str(source), 'Arabic', str(checkpoint)], capture_output=True, text=True)
            self.assertEqual(init.returncode, 0, init.stderr)
            command = [sys.executable, str(PATH), 'assemble', str(source), str(checkpoint), str(output)]
            partial = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(partial.returncode, 0)
            self.assertFalse(output.exists())
            data = json.loads(checkpoint.read_text(encoding='utf-8-sig'))
            self.assertEqual(data['source_name'], 'input.srt')
            self.assertIsNone(data['output_path'])
            data['translations'][0] = 'أهلًا'
            data['unresolved'] = ['Review greeting register']
            checkpoint.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
            source.write_text(source.read_text(encoding='utf-8') + '\nchanged', encoding='utf-8')
            changed = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(changed.returncode, 0)
            self.assertIn('source', changed.stderr.lower())
            source.write_text('1\n00:00:01,000 --> 00:00:02,000\nHello\n', encoding='utf-8')
            completed = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIn('1 unresolved', completed.stdout)
            self.assertIn('أهلًا', output.read_text(encoding='utf-8-sig'))
