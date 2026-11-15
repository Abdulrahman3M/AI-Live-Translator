---
name: setup
description: Choose live bilingual translation or SRT/ASS subtitle translation and route to the appropriate skill.
---

# Translator — Home

When the plugin is invoked without an explicit function, briefly offer: 1. Live translation between two languages; 2. SRT/ASS subtitle translator. Ask the user to choose. If the request clearly identifies a function, route directly without asking again.

For live translation, load `../ai-live-translator/SKILL.md`, ask for the two languages if missing, and follow its setup and translation-only contract. For subtitle translation, load `../subtitle-translator/SKILL.md` and ask only for its missing settings. Never start translation-only mode for a subtitle task. Explicitly addressed controls can stop live mode and return to this home.
