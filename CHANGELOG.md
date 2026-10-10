# Changelog

All notable releases follow [Semantic Versioning](https://semver.org/).

## [1.0.1] — 2026-10-10

### Added
- Root portable Agent Plugins `plugin.json` manifest for ChatGPT and compatible runtimes.
- `.codex-plugin/plugin.json` fallback, skills-only first-run onboarding skill, and repository-local plugin marketplace manifest.
- Direct ChatGPT plugin installation and verification instructions; no external services or credentials.

### Changed
- Synchronize release version to 1.0.1 across manifests, README files and release documents.

## [1.0.0] — 2026-10-10

### Added
- Portable Agent Skills package, strict dual-language live-translation prompt, bilingual setup examples and explicit address controls.
- Claude Code plugin manifest and commands plus Copilot, Codex, Gemini, ChatGPT and generic-agent installation guidance.
- Large multilingual bidirectional examples corpus, deterministic command-router reference, stdlib validation and regression tests.
- Version synchronization rule across manifests, documentation and CHANGELOG.

### Limitations
- Model text translation depends on chosen host and model. No universal installer, direct API, phone, microphone, or background interpreter is bundled.
