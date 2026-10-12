# First Release, Project Hero, and Download Packages

## Goal

Prepare the first GitHub Release for AI Live Translator as version 1.0.7, add a text-free project hero that communicates bidirectional translation across languages, and provide reproducible direct-download packages for the supported installation routes.

The project homepage means both `README.md` and `README.ar.md`. The release must describe the tool's capabilities and limits in English and Arabic. The existing `main` branch already contains the earlier icon, installation guidance, examples, and governance changes; this work builds on that state.

## Approved direction

- Hero: a wide editorial illustration without text. Show two simplified people, two speech bubbles, opposing loop arrows, and abstract language marks. Use the established navy, teal, and cyan identity so the image is legible without depending on a reader's language.
- Version: `1.0.7`, synchronized with the repository's release rule.
- Release downloads: five assets: ChatGPT plugin, Codex plugin, Claude Code plugin, portable Agent Skill, and a source-code archive.
- Keep the existing translation behavior and safety contract unchanged.

## Design

### Homepage image and presentation

Create one wide raster hero image under `assets/` and reference it near the top of both READMEs, after the title and before the quick-start section. Add concise, localized alt text. Do not put words, flags, or culture-specific symbols in the artwork. Keep the existing square plugin icon for manifests and small host surfaces; the hero image serves the project page only.

### Version and release information

Advance the release version to `1.0.7` consistently in `VERSION`, the root and host plugin manifests, `plugin/metadata.json`, both README titles and release sections, and `CHANGELOG.md`. Add a bilingual release-notes file under `docs/releases/` describing bidirectional text translation, translation-only handling, language and dialect coverage, context/tone preservation, direct-address controls, and host/model variability.

The GitHub Release is created for tag `v1.0.7` only after the validated changes have been committed and pushed to `main`. The release notes are read from the checked-in bilingual notes file and all five generated ZIP files are attached.

### Download package builder

Keep `plugin/installation/build-chatgpt.py` as the dedicated ChatGPT package builder. Add a standard-library Python release builder that creates the other four ZIP files under ignored `dist/`:

1. **Codex plugin:** include `.codex-plugin/plugin.json`, the referenced skill and commands, and any referenced icon files.
2. **Claude Code plugin:** include `.claude-plugin/plugin.json`, its command sources, the portable translator skill and required resources.
3. **Portable Agent Skill:** include the `ai-live-translator/` skill folder with its metadata, rules, examples, references, scripts, tests only when required at runtime, and icon assets. Exclude repository-only test/cache data.
4. **Source code:** include the tracked project source with a versioned top-level folder; exclude `.git`, generated `dist/` content, caches, virtual environments, temporary files, and editor/OS state.

All package filenames include `v1.0.7`. The builder verifies ZIP integrity, required entry points, versions where manifests exist, and that declared relative assets resolve inside their package. Package contents must be deterministic from the committed repository state.

Update the GitHub Actions workflow to run the repository validator and unittest suite, build all five archives, upload them as workflow artifacts, and create the release with the five assets when a `v*` tag is pushed. Release creation must not happen on ordinary branch pushes or `workflow_dispatch` without a release tag.

### Documentation

Update the short English and Arabic installation maps under `docs/` to link directly to the latest release downloads and explain which package fits each platform. Keep command-by-command setup in `plugin/installation/` and the existing advanced guidance intact. Update both READMEs to make the hero, quick start, platform selector, and release downloads easy to find without repeating the same installation explanation in multiple sections.

Use the canonical name **AI Live Translator** and the short description **Translate messages both ways** consistently in manifests, package instructions, release notes, and README metadata. Localize the short description in Arabic guidance as **ترجمة الرسائل ذهابًا وإيابًا**.

## Validation and acceptance

- `python skills/ai-live-translator/scripts/validate.py` succeeds.
- `python -m unittest discover -s skills/ai-live-translator/scripts/tests -v` succeeds, including new regression coverage for package paths, manifest versions, archive integrity, excluded files, and README hero/download links.
- All five archives build with filenames and version references set to `1.0.7`; their entry points and referenced assets resolve.
- Both README files display the hero image and point to the platform guide and release downloads.
- English and Arabic release notes explain the same capabilities and limits.
- `git diff --check` succeeds; generated archives and test caches are removed locally after verification and are not committed.
- The final release tag points to the commit pushed to `origin/main`, and the GitHub Release contains the five expected ZIP assets.

## Out of scope

- Changing translation or routing behavior.
- Claiming that every host has a native plugin installer or icon field.
- Adding telemetry, network calls, transcript storage, microphone access, credentials, or autonomous messaging.
- Publishing to third-party plugin marketplaces.

## Risks and decisions

- Host plugin formats differ. Each ZIP must use its host's existing manifest and documented layout; the portable Agent Skill is the fallback for Copilot, Gemini, and other environments without a compatible plugin package format.
- The GitHub Actions release depends on repository permission to create Releases. Workflow failure must leave the already-pushed source commit and tag intact and report the exact failure.
- The generated illustration is a raster project-page asset. Existing vector and square icon assets remain the scalable host identity.
