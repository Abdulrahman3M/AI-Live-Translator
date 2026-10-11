# Use AI Live Translator with Claude

“Claude” has more than one installation surface. This guide covers **Claude.ai / Claude Desktop / Cowork** plugin upload and **Claude Code** local loading. The complete GitHub project can be used as the source, but select the right plugin folder and preserve its directory structure.

## Which files are required?

For the plugin, keep these paths together under one plugin root:

- `.claude-plugin/plugin.json` — Claude plugin manifest and command paths.
- `plugin/commands/` — command Markdown files referenced by the manifest.
- `skills/` — the translator and setup skills, including their supporting reference, example, script, and asset files.
- `prompt/live-translation.md` — optional fallback if you want to use the prompt manually rather than as a plugin.

The simplest safe choice is to keep the full repository folder intact and use its root as the plugin root. The project’s Python utilities, tests, ChatGPT-specific `plugin.json`, and CI files are not needed by Claude at runtime. If you create a smaller folder or ZIP, preserve the paths above exactly; the manifest refers to paths inside the plugin root.

## Claude.ai, Claude Desktop, and Cowork: upload the plugin

1. Download and extract the repository, or prepare a folder containing the required paths listed above.
2. Confirm that the plugin root contains `.claude-plugin/plugin.json` and that `plugin/commands/` and `skills/` are alongside `.claude-plugin/`.
3. If using a ZIP, zip the plugin root or its contents so the archive contains exactly one `.claude-plugin/plugin.json` at the plugin root. Do not upload GitHub’s automatic source ZIP without checking its folder nesting.
4. In Claude, open **Customize → Plugins → Add → Upload plugin**.
5. Select the prepared plugin folder, `.zip`, or `.plugin` archive as supported by the upload dialog. Review the plugin details and add it.
6. In a new conversation, type `/` to find the plugin skill/command, or invoke the start command shown by the plugin. This project also defines the Claude Code command `/ai-live-translator:start`; command availability and naming can differ across Claude surfaces.
7. Follow the setup prompts to choose both languages, then test with one short sentence.

After an account-level upload, the plugin may be available across Claude chat, Cowork, and Claude Code using that account, subject to the components each surface supports. Plugin upload controls and organization permissions can vary.

## Claude Code: load the local repository

1. Install Claude Code and download/extract or clone the repository.
2. Open a terminal in any working directory.
3. Pass the **absolute path to the repository root** (the directory containing `.claude-plugin/`) to Claude Code:

```bash
claude --plugin-dir "/absolute/path/to/AI-Live-Translator"
```

For example, on macOS/Linux, if you extracted it into Downloads:

```bash
claude --plugin-dir "$HOME/Downloads/AI-Live-Translator"
```

4. In the launched Claude Code session, run `/ai-live-translator:start` to begin, or run `/ai-live-translator:help` for the help command.
5. If a command or skill is missing, run `claude plugin validate "/absolute/path/to/AI-Live-Translator"`, then check that you used the repository root and did not move the manifest or command files.
6. This `--plugin-dir` method loads the plugin for that session. Start Claude Code with the flag again for another session. To install/update through a Claude Code marketplace or account-synced plugin, use that installation source’s own update controls.

To load a newer local version, replace or update the extracted repository folder with the new project files, then restart Claude Code with `--plugin-dir` (or run `/reload-plugins` after editing files during an active session). Account-uploaded Claude plugins are managed under **Customize → Plugins** and updated according to their source; a manually uploaded copy may require uploading/replacing its new archive.

## Manual prompt-only fallback

If you are using a Claude chat surface without plugin upload, copy all of `prompt/live-translation.md` into the supported project or conversation instructions and explicitly activate the translator. This is prompt-based behavior, not an installed plugin, and available instruction persistence varies by Claude surface.

## Voice clarity and quality

Clearly separate the words addressed to the AI from the other speaker and surrounding sounds. Use labels such as **“My message:”** and **“Other person's message:”**, speak one turn at a time, and avoid talking over television or nearby conversations. The skill consumes text supplied by Claude; it does not process raw microphone audio or identify speakers. If the transcript has overlap, noise, or an uncertain speaker, ask for a clean repeat, typed message, or speaker label instead of guessing.

AI Live Translator contains instructions and skills, not a dedicated translation model. This project has been tested most extensively with ChatGPT, so that is the recommended starting point. Claude and other compatible agents may still be tried; accuracy and adherence can vary with the AI model, language pair, and session.

## Official references

- [Claude plugins for Claude.ai, Desktop, and Cowork](https://claude.com/docs/plugins/overview)
- [Claude Code: Plugins overview](https://code.claude.com/docs/en/plugins)
- [Claude Code: Create a plugin and load it locally](https://code.claude.com/docs/en/plugins/create)
