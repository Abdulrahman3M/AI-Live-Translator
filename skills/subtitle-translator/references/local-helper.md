# Offline subtitle helper

The optional Python 3 standard-library helper handles deterministic file operations. The executing AI agent reads the source, performs the translation and reviews it; this script does not translate, access the network, or inspect rendering. Subtitle text and JSON checkpoints may be sensitive: keep them in an authorized local location.

Extract a style profile without exporting dialogue:

```sh
python skills/subtitle-translator/scripts/subtitle_tools.py extract reference.ass
```

After translating **every** dialogue event in order, save a UTF-8 JSON array containing one translated string per event. Encode a subtitle line break as JSON `\\N`; retain ASS override tags in their original order. Then assemble:

```sh
python skills/subtitle-translator/scripts/subtitle_tools.py assemble source.srt translations.json output.ass --reference reference.ass
python skills/subtitle-translator/scripts/subtitle_tools.py assemble source.srt translations.json output.ass --reference reference.ass --profile overrides.json
python skills/subtitle-translator/scripts/subtitle_tools.py assemble source.ass translations.json output.ass
python skills/subtitle-translator/scripts/subtitle_tools.py assemble source.ass translations.json output.ass --reference reference.ass
```

For longer work, initialize a private resumable checkpoint instead of a plain array:

```sh
python skills/subtitle-translator/scripts/subtitle_tools.py checkpoint source.srt Arabic checkpoint.json --dialect Egyptian
python skills/subtitle-translator/scripts/subtitle_tools.py assemble source.srt checkpoint.json output.ass --reference reference.ass
```

Replace each `null` in `translations` with its corresponding agent-authored translation, preserving event order; record uncertain lines in `unresolved` and the intended destination in `output_path` when known. Save progress after each manageable batch, keeping the checkpoint separate from the deliverable. The next unfinished event is the first remaining `null`. On resumption, check the target language, dialect and source identity; the helper compares the source file's SHA-256 before assembly and refuses partial translations. Retain the checkpoint securely if work is interrupted. A completed checkpoint may still contain unresolved items requiring a report and human review. Do not share or upload it without authorization.

The output is UTF-8 with BOM and must not already exist. For SRT, omit `--reference` to use the documented Calibri default. The first reference style supplies the visual style; missing style fields use defaults. A JSON `--profile` supplies explicit settings over the reference; see [example settings](../examples/sample-profile.json). Fields use ASS names and string values; color values use `&HAABBGGRR` (or a valid shorter ASS hex value), not RGB. Font size, scaling, border, alignment and margins are validated. The helper copies no reference event text or inline styling; any speaker-label or sound-effect styling must be intentionally included in the agent-authored strings. For ASS, the helper preserves the original event fields and checks that override sequences remain in order. Without a reference or profile it retains source styles. With one, it restyles a single-style source only when the source and chosen profile declare the same resolution; source style names and all event fields remain intact. It refuses multiple source styles or different canvases because blind remapping can change positioning or meaning. Inline overrides are retained and may override the reference look; inspect and document these conflicts. Use a reviewed manual method for cases the helper rejects.

SRT times round to the nearest centisecond, with half-centiseconds rounded up; overlapping events remain overlapping. The helper converts balanced `<b>`, `<i>` and `<u>` spans to ASS overrides when the translated event retains the same markup sequence. It rejects other markup, invalid blocks, and quantized zero-duration events rather than silently discarding them. It does not implement a full ASS validator, font discovery, automatic bidi wrapping, speaker identification, semantic review, or rendering. Unicode direction controls, meaningful tags, readable line breaks, style decisions and source correspondence remain the agent's responsibility. Do not apply Arabic controls to other languages. A script success message is not proof of accurate translation, correct glyph shaping, or visual equivalence.
