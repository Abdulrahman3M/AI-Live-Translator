# Choose an installation method

**AI Live Translator** — Translate messages both ways.

The project provides a portable Agent Skill and prompt. Each host loads them differently, and icon display depends on that host's plugin interface.

| Host | Recommended route | Icon behavior |
| --- | --- | --- |
| ChatGPT | Build the dedicated ZIP with `python plugin/installation/build-chatgpt.py`, then upload it or open it in Plugin Creator where available. | The OpenAI plugin interface references `assets/ai-live-translator-icon-128.png` for the composer and the 512 px image as its logo. |
| Codex | Install the plugin through a supported local marketplace or load the Agent Skill from a supported skills directory. | The Codex-compatible manifest uses the same composer and logo assets. The skill also declares small and large icons for OpenAI-compatible skill surfaces. |
| Claude Code | Load this repository as a local plugin using `.claude-plugin/plugin.json`, or follow Claude Code's marketplace workflow. | This manifest does not define an icon field; the host controls plugin presentation. |
| GitHub Copilot | Follow the Copilot adapter and load the skill or prompt format supported by your Copilot environment. | No portable Copilot icon field is declared. |
| Gemini and other agents | Explicitly load `skills/ai-live-translator/SKILL.md` or paste `prompt/live-translation.md` into the relevant instruction area. | Display depends on the host; Agent Skills has no universal plugin icon field. |

The portable Agent Plugins manifest keeps host-specific presentation inside the relevant host extension. The SVG is the source artwork; square PNG exports at 64, 128, 256, and 512 px cover skill, composer, and listing uses.

For current OpenAI manifest fields and icon requirements, see [Package your plugin](https://developers.openai.com/plugins/build/plugins) and [Upload and submit your plugin](https://developers.openai.com/plugins/deploy/submission). The [portable manifest specification](https://agent-plugins.org/plugin-authors/manifest) defines package metadata separately from client-specific icon support.

## Full instructions

For command-by-command setup, update guidance, and host limitations, see [`plugin/installation/INSTALL.md`](../plugin/installation/INSTALL.md) and the platform adapters under [`plugin/adapters/`](../plugin/adapters/README.md).
