# ChatGPT Plugin Distribution (v1.0.2)

The GitHub source ZIP is **not** the installable ChatGPT distribution. The initial v1.0.1 upload was rejected by ChatGPT; the simplified v1.0.2 package was accepted in the user's ChatGPT account.

## Build from the repository

From the repository root, run:

```sh
python plugin/installation/build-chatgpt.py
```

This creates `dist/AI-Live-Translator-ChatGPT-Plugin-v1.0.2.zip`, with a root `plugin.json`, the onboarding skill, the translation skill, prompts, rules, examples and scripts. It excludes host-specific manifests, GitHub metadata, and repository maintenance documents.

Install the generated ZIP in ChatGPT under **Plugins → Add → Upload plugin**. Do not upload GitHub's auto-generated repository archive.

For Claude Code, use the repository's `.claude-plugin/plugin.json` and `plugin/installation/INSTALL.md` rather than the ChatGPT ZIP.

The manifest's semantic version must exactly match `VERSION`, currently **1.0.2** (not 1.0.20). The host may display its own release number; check the plugin's actual metadata before attributing it to this repository.

Note: Packaging validation does not guarantee acceptance by every ChatGPT account or every Claude Code version.
