# Build AI Live Translator release packages

**AI Live Translator** — Translate messages both ways.

Build from the project root with Python 3. The version is read from `VERSION`; update all release metadata together before building.

```sh
python plugin/installation/build-chatgpt.py
python plugin/installation/build_release.py
```

The commands create five version-matched archives in ignored `dist/`:

- `AI-Live-Translator-ChatGPT-Plugin-v<VERSION>.zip` — dedicated, minimal ChatGPT plugin archive.
- `AI-Live-Translator-Codex-Plugin-v<VERSION>.zip` — Codex manifest, skills, commands, and referenced assets.
- `AI-Live-Translator-Claude-Code-Plugin-v<VERSION>.zip` — Claude Code manifest, commands, portable translator skill, and resources.
- `AI-Live-Translator-Agent-Skill-v<VERSION>.zip` — portable `ai-live-translator/` skill folder with its rules, examples, references, scripts, and icons.
- `AI-Live-Translator-Source-v<VERSION>.zip` — complete project source in a versioned top-level folder; this is not an installable plugin.

The builders verify ZIP integrity, manifest versions, required entry points, and declared icon paths. Run the validator and unit suite in `AGENTS.md` before publishing. The GitHub Actions workflow builds all five archives and creates the Release with `docs/releases/v<VERSION>.md` only when a matching `v*` tag is pushed to GitHub.

Use the ChatGPT ZIP for ChatGPT plugin upload where the account interface supports it; do not substitute GitHub's automatically generated source archive. Host installation flows and plugin support can vary by product version.
