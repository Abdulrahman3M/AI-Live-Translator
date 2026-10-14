# ChatGPT Plugin Distribution (v1.0.8)

Build the ChatGPT-specific ZIP from the merged repository source. GitHub's automatically generated source ZIP is **not** the installable plugin archive.

## Build the archive

1. Download the repository from the `main` branch and extract it, or update your local clone:
   ```sh
   git switch main
   git pull origin main
   ```
2. From the repository root, run:
   ```sh
   python plugin/installation/build-chatgpt.py
   ```
3. The script reads `VERSION` and verifies it matches the root `plugin.json`. For v1.0.8 it creates:
   ```
   dist/AI-Live-Translator-ChatGPT-Plugin-v1.0.8.zip
   ```

The archive contains the root plugin manifest, OpenAI icon assets, setup skill, translator skill, prompts, rules, examples and runtime scripts. It includes the 128 px composer icon, 512 px listing logo, Agent Skill icon metadata, and the full-size SVG source. The script checks the archive integrity and confirms its embedded plugin version and icon paths.

## Install or update in ChatGPT

In ChatGPT, open **Plugins → Add → Upload plugin** (if this option is available) and upload the generated version-matched ZIP. If the interface instead offers **Plugin Creator**, choose the existing AI Live Translator plugin to edit/update it, or create it from the new ZIP/folder if editing an existing plugin is unavailable. Review the generated plugin details, save, then open AI Live Translator and confirm it asks for two languages and shows the updated localized setup guidance.

Do **not** upload GitHub's auto-generated source ZIP. Use the archive whose version matches `VERSION`.

For Claude Code, use `.claude-plugin/plugin.json` and `plugin/installation/INSTALL.md`, not the ChatGPT ZIP.

Note: Plugin Creator/upload options can vary by account and product rollout. Building the archive verifies its structure and version; it cannot guarantee acceptance by every ChatGPT account.
