# ChatGPT installation status and steps

The installed GitHub connector does not have a `create_repository` action and the installed ChatGPT plugin management connector does not provide creation/upload of personal plugins. These require the user's action in GitHub CLI/browser and ChatGPT UI. Do not claim otherwise.

1. Publish GitHub with the guarded local `publish-github.ps1` or `publish-github.sh` script. This creates a private repository by default.
2. Upload `AI-Live-Translator-ChatGPT-Plugin-v1.0.8.zip` in Plugins → Add → Upload plugin (if present), or open Plugin Creator under Plugins → Add (+) and submit the files as a skills-only plugin.
3. Start `AI Live Translator`. Update an existing copy with the v1.0.8 distribution in ChatGPT's plugin management flow; if the interface does not offer replace/update, remove the old copy and add the new archive, then activate it in a fresh chat. Check the setup asks for two languages and that ordinary text is translated rather than answered.
4. When workspace GitHub import is supported, an admin may instead import the repository URL as a plugin marketplace (see official documentation and permissions).

No external MCP app exists for this skills-only translator, and no ChatGPT account installation occurs when publishing to GitHub alone.
