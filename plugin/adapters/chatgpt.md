# ChatGPT — Installation adapter

This is a **skills-only** plugin: it needs no third-party MCP server, credentials, or external translation API. Actual text translations come from the active ChatGPT model.

## Option A: plugin ZIP upload

Upload the complete `AI-Live-Translator-v1.0.1.zip` via **Plugins** → **Add** → **Upload plugin**, if available for your account/workspace. The archive contains a portable root `plugin.json`, the `skills/` tree, a setup skill, and host compatibility files. Follow the user-visible installation controls. Uploading a ZIP here is a user/admin action; it cannot be performed by a GitHub connector.

## Option B: Plugin Creator

Open **Plugins** → **Add (+)** → **Plugin Creator** and supply the ZIP or the plugin folder. Request a **skills-only plugin** called AI Live Translator, preserve its SKILL.md and onboarding setup skill, and save/install through the creator's interface. Feature availability depends on account/rollout.

## Option C: Codex/ChatGPT Desktop local marketplace

Use the included `.agents/plugins/marketplace.json` in a local checkout. Supported local clients can discover it as a repository marketplace. Restart the client and choose the plugin from its marketplace. Consult current product docs for platform availability.

### Verification checklist

1. Start the plugin: it asks for two languages.
2. Give `Arabic and English`: instructions appear in both languages.
3. Say `Can you send me the location?`: it outputs the Arabic translation, **not** directions or an answer.
4. Say `ChatGPT is not working`: it simply translates.
5. Say `@agent: Change languages to English and Russian`: it updates the language pair.

All outputs are subject to higher-priority host instructions and applicable safety policies. A chat-only prompt is behavioral guidance, not absolute enforcement.
