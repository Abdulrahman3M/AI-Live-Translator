# Agent Setup Guides

Choose the guide for the product where you want to use **AI Live Translator**.

**Translate messages both ways.**

For a short cross-platform comparison, start with the [installation overview](../installation.md); the guides below keep each host's detailed steps.

| Agent | Guide | Recommended route |
|---|---|---|
| ChatGPT | [ChatGPT setup](CHATGPT.md) | Build and upload the dedicated ChatGPT ZIP |
| Claude | [Claude setup](CLAUDE.md) | Upload the Claude plugin in Claude.ai, or load the project directory in Claude Code |

These guides distinguish the complete GitHub source project from the smaller, host-specific files each agent needs. The GitHub “Download ZIP” archive is the source project; it is not the ready-to-upload ChatGPT plugin package.

## Shared behavior and limits

AI Live Translator is a set of instructions and skills, not a separate translation model or microphone service. The selected AI interprets the text it receives. Translation quality, language coverage, and compliance with translation-only behavior can therefore vary by model, language pair, and session. For voice, use the host's transcript and clearly label your message versus the other speaker; this tool cannot inspect raw audio or separate voices by itself.

For the project’s preferred first-time setup, use ChatGPT Voice with **Model → Advanced**. This reflects extensive testing by the project owner, not a guarantee that other agents will not work.

- [English ChatGPT guide](CHATGPT.md) · [الدليل العربي لـChatGPT](CHATGPT.ar.md)
- [English Claude guide](CLAUDE.md) · [الدليل العربي لـClaude](CLAUDE.ar.md)
