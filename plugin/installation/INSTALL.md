## Direct ChatGPT plugin installation (2026)

The project contains **portable Agent Plugins** `plugin.json`, a first-run onboarding skill at `skills/setup/SKILL.md`, and a Codex compatibility manifest at `.codex-plugin/plugin.json`. For a user-created ChatGPT plugin, **upload the ZIP** via Plugins → Add → Upload plugin where available, or use **Plugin Creator** from Plugins → Add (+). The GitHub connector does not install plugins to ChatGPT accounts. See `plugin/adapters/chatgpt.md`.

# Install AI Live Translator in AI agents

## Universal fallback (any chat that accepts a user/system prompt)

Paste the complete contents of `prompt/live-translation.md` into a **new session's relevant instruction area**, then explicitly say "Activate AI Live Translator." Instruction persistence and priority depend on the host. This is portable behavior guidance, **not a universal installed plugin**.

## Agent Skills compatible runtimes / Codex

Copy `skills/ai-live-translator/` into an **Agent Skills discovery directory supported by the chosen host**, or load `SKILL.md` as instructed by that host. For Codex, use a suitable skills location and activate `$ai-live-translator` where supported. `AGENTS.md` is development governance, not the translator activation command. Refer to your Codex version's current skills install documentation.

## Claude Code native plugin

From a clone or extracted repository, start Claude Code with a local plugin directory using the CLI option `--plugin-dir <absolute-path-to-AI-Live-Translator>` on a version supporting plugin development. The manifest is at `.claude-plugin/plugin.json`. Invoke `/ai-live-translator:start` (or the skill). Validate in a machine with Claude Code installed: `claude plugin validate . --strict`. Plugin loading and exact command UX are version-dependent.

## GitHub Copilot

Use `.github/prompts/ai-live-translator.prompt.md` in an environment supporting prompt files or load `skills/ai-live-translator/SKILL.md` via its Agent Skills discovery mechanism. `.github/copilot-instructions.md` is repository development guidance and intentionally does not force all Copilot sessions into translator mode.

## Gemini and other agents

Follow `GEMINI.md` if recognized, but explicitly load the skill or paste the portable prompt. No assumption that reading `GEMINI.md` starts a translator.

## Important caveats

- There is no host-independent specification for automatically installing plugin packages across *all* AI agents.
- Markdown-only prompts cannot enforce direct-address detection against every host policy or recognize speech/call audio.
- Use `@agent:` for the least ambiguous explicit control syntax.
- Python files are validation/reference utilities and not necessary for actual translation.

## GitHub publishing

See [`PUBLISHING.md`](PUBLISHING.md) and the guarded PowerShell / Bash publishing scripts. The scripts create a private repository by default and require authenticated GitHub CLI.
