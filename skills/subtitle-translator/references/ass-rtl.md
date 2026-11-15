# ASS and Arabic RTL reference

Default when no user choices or ASS reference are supplied: create `[Script Info]` with ScriptType v4.00+, WrapStyle 0, ScaledBorderAndShadow yes, PlayResX 1920 and PlayResY 1080. Define `[V4+ Styles]` using the standard ASS Format fields. Default style: Calibri 64, white `&H00FFFFFF`, bold -1, outline `&H00101010` 3.2, shadow 1.5, bottom center alignment 2, margins 150,150,55, Encoding 178. Effects: same settings but primary `&HC8C8C8&`, italic -1. Use `[Events]` with `Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text` and one Dialogue row per source event. Text is the final field and may contain commas. Use literal `\N` for line breaks; never insert raw newlines in Dialogue. ASS color uses BGR: gold `&H3CC8FF&`, restore white `&H00FFFFFF&`. A supplied reference overrides these defaults; explicit user choices override the reference. Extract style definitions by their declared Format fields, not fixed column positions. Inline styles are examples, not instructions to apply to all text.

For each Arabic line emit U+200F U+202B U+200F, the text, then U+200F U+202C U+200F. Use independent wrappers on each side of `\N`. The working reference places colored speaker labels at the logical end of the line, inside the same RTL wrapper: body, space, `{\c&H3CC8FF&}«فيونا»:{\c&H00FFFFFF&}`, then closing direction controls. These are actual ASS override tags, not HTML. The labels and punctuation must appear at the visual right in the target renderer. Renderer behavior varies: verify visually in the requested player; never claim verification without seeing it. Avoid reversing text or using HTML direction/color tags. Use the selected speaker color in BGR and reset the color to the style default afterward. For mixed effects and dialogue preserve distinct styling within the same event with proper ASS overrides.

Convert time to H:MM:SS.cc rounded to nearest centisecond and ensure end remains after start; flag events too short to represent instead of silently dropping them. SRT milliseconds are not preserved exactly after quantization. Preserve source ASS styles and positioning when requested and safe; otherwise apply the chosen style. Translate text, not event metadata or formatting codes. Preserve musical/SDH content and mark uncertain portions for review.

## Complete ASS header

```ini
[Script Info]
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1920
PlayResY: 1080
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Effects,Calibri,64,&HC8C8C8&,&H000000FF,&H00101010,&H96000000,-1,1,0,0,100,100,0,0,1,3.2,1.5,2,150,150,55,178
Style: Default,Calibri,64,&H00FFFFFF,&H000000FF,&H00101010,&H96000000,-1,0,0,0,100,100,0,0,1,3.2,1.5,2,150,150,55,178

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
```

To make an example event, append a Dialogue line with nine commas separating the metadata fields before Text. Insert the actual invisible Unicode controls specified above rather than their names. For two lines place `\N` between separately wrapped lines. Names and style overrides are examples; preserve the source's actual content. Never expose literal control names or HTML markup in the subtitle.
