# Changelog

## [1.0.5] — 2026-10-11

### Added
- Defined separate end-user and advanced-user/maintainer guidance, fully listed on both project homepages.
- Localized end-user setup instructions in both selected languages only, for arbitrary language pairs.
- Added direct user guidance to use clear standard/formal language and avoid local dialects where possible; kept the “text of my next message is…” cue optional.
- Added a user-facing repeat/rephrase request for unclear messages and operative runtime rules to clarify before translation rather than guess.
- Added offline validation checks for setup guidance, homepage sections, and separation of host-specific instructions.

### Changed
- Kept ChatGPT message/voice-message and Voice Advanced options, transcription/background-noise notes, host portability, and variable accuracy in advanced-user/maintainer docs.
- Clarified that setup language recommendations do not authorize distorting dialect input; preserve meaning and tone.
- Synchronized release metadata to 1.0.5 across manifests, prompts, and documentation.

## [1.0.4] — 2026-10-10

### Changed
- Confirmed the ChatGPT display label as **AI Live Translator** in Title Case, with spaces and no hyphens; the internal plugin ID remains `ai-live-translator`.

### Improved
- Added detailed voice-transcript guidance to distinguish intended speech from other speakers and background noise.
- Instructed the assistant to request clarification when speaker attribution is uncertain instead of guessing or treating noise as the user's message.
- Synchronized release metadata to 1.0.4.

## [1.0.3] — 2026-10-10

### Improved
- Added a one-output-per-message rule and a silent duplicate/source-echo check to reduce repeated translations and conversational replies.
- Strengthened multilingual language detection, mixed-language handling, dialect/register preservation and uncertainty behavior.
- Added bilingual first-use guidance recommending ChatGPT Voice Advanced and Auto-detect based on owner testing, with clear model- and language-pair variability notes.
- Synchronized release identifiers to 1.0.3 across manifests, prompts, docs and version metadata.


All notable releases follow [Semantic Versioning](https://semver.org/).

## [1.0.2] — 2026-10-10

### Fixed
- Simplified the ChatGPT installation ZIP after v1.0.1 was rejected by ChatGPT.
- Synchronized release identifiers to **1.0.2** (not 1.0.20) across root and distribution manifests, documentation and version metadata.
- Documented the dedicated ChatGPT ZIP build process to prevent users uploading incompatible source archives.

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
