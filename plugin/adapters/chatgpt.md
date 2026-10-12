# ChatGPT — Installation adapter

This is a **skills-only** plugin: it needs no third-party MCP server, credentials, or external translation API. Actual text translations come from the active ChatGPT model.

## Option A: plugin ZIP upload

Upload the generated `AI-Live-Translator-ChatGPT-Plugin-v1.0.7.zip` via **Plugins** → **Add** → **Upload plugin**, if available for your account/workspace. Build this archive from the merged `main` branch using `python plugin/installation/build-chatgpt.py`; the script reads the current `VERSION`, validates the OpenAI icon paths, and verifies the packaged manifest. Follow the user-visible installation controls. Uploading a ZIP here is a user/admin action; it cannot be performed by a GitHub connector.

## Option B: Plugin Creator

Open **Plugins** → **Add (+)** → **Plugin Creator** and supply the newly built v1.0.7 ZIP or extracted plugin folder. If an existing plugin can be edited, update it there; otherwise create a new plugin from the updated files. Request a **skills-only plugin** called AI Live Translator, preserve its SKILL.md and onboarding setup skill, and save/install through the creator's interface. Feature availability depends on account/rollout.

The package declares the composer icon and listing logo in the OpenAI interface extension and includes skill-level small and large icons. The generic portable manifest does not define a universal icon field.

## Option C: Codex/ChatGPT Desktop local marketplace

Use the included `.agents/plugins/marketplace.json` in a local checkout. Supported local clients can discover it as a repository marketplace. Restart the client and choose the plugin from its marketplace. Consult current product docs for platform availability.

### Verification checklist

1. Start the plugin: it asks for two languages.
2. Give `Arabic and English`: instructions appear in both languages.
3. Say `Can you send me the location?`: it outputs the Arabic translation, **not** directions or an answer.
4. Say `ChatGPT is not working`: it simply translates.
5. Say `@agent: Change languages to English and Russian`: it updates the language pair.

All outputs are subject to higher-priority host instructions and applicable safety policies. A chat-only prompt is behavioral guidance, not absolute enforcement.
