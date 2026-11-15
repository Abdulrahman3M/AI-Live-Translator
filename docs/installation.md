# Choose an installation method

**AI Live Translator** — Translate messages both ways.

## Direct downloads — published v1.0.8

**The latest published release is v1.0.8.** Download the matching host package below; the [release notes](releases/v1.0.8.md) summarize the changes from v1.0.8.

- [ChatGPT plugin — AI-Live-Translator-ChatGPT-Plugin-v1.0.8.zip](https://github.com/Abdulrahman3M/AI-Live-Translator/releases/download/v1.0.8/AI-Live-Translator-ChatGPT-Plugin-v1.0.8.zip)
- [Codex plugin — AI-Live-Translator-Codex-Plugin-v1.0.8.zip](https://github.com/Abdulrahman3M/AI-Live-Translator/releases/download/v1.0.8/AI-Live-Translator-Codex-Plugin-v1.0.8.zip)
- [Claude Code plugin — AI-Live-Translator-Claude-Code-Plugin-v1.0.8.zip](https://github.com/Abdulrahman3M/AI-Live-Translator/releases/download/v1.0.8/AI-Live-Translator-Claude-Code-Plugin-v1.0.8.zip)
- [Portable Agent Skill — AI-Live-Translator-Agent-Skill-v1.0.8.zip](https://github.com/Abdulrahman3M/AI-Live-Translator/releases/download/v1.0.8/AI-Live-Translator-Agent-Skill-v1.0.8.zip)
- [Source code — AI-Live-Translator-Source-v1.0.8.zip](https://github.com/Abdulrahman3M/AI-Live-Translator/releases/download/v1.0.8/AI-Live-Translator-Source-v1.0.8.zip)

## Which package fits?

| Host | Recommended package and route | Icon behavior |
| --- | --- | --- |
| ChatGPT | Upload the ChatGPT ZIP, or open its extracted files in Plugin Creator where available. | The OpenAI plugin interface references the 128 px composer image and 512 px logo. |
| Codex | Install the Codex plugin ZIP through a supported local marketplace, or load the Agent Skill from a supported skills directory. | The Codex-compatible manifest references the composer and logo assets. |
| Claude Code | Extract the Claude Code ZIP and load its local plugin directory with `--plugin-dir`, or use Claude Code's marketplace workflow. | The host controls plugin presentation; its manifest does not define an icon field. |
| GitHub Copilot | Install the portable Agent Skill or follow the Copilot adapter for prompt-file support. | No portable Copilot icon field is declared. |
| Gemini and other agents | Install the portable Agent Skill where supported, or load `skills/ai-live-translator/SKILL.md` / `prompt/live-translation.md` manually. | Display depends on the host; Agent Skills has no universal plugin icon field. |

The plugin icon remains separate from the wide project hero. SVG is the icon source, with 64, 128, 256, and 512 px PNG exports for supported surfaces.

## Full instructions

For command-by-command setup and host limitations, see [`plugin/installation/INSTALL.md`](../plugin/installation/INSTALL.md), [`plugin/installation/BUILD-RELEASE.md`](../plugin/installation/BUILD-RELEASE.md), and the adapters under [`plugin/adapters/`](../plugin/adapters/README.md).
