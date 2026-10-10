# Claude Code adapter

Load repository root as a plugin directory. `.claude-plugin/plugin.json` registers `plugin/commands/start.md` as `/ai-live-translator:start`; the standard `skills/` tree is discoverable. Run `claude plugin validate . --strict` when CLI is available. Explicitly invoke the command; ordinary project chats remain unaffected.

For control behavior see `skills/ai-live-translator/rules/address-and-control.md`.
