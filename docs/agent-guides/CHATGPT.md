# Use AI Live Translator with ChatGPT

This guide covers the recommended ChatGPT plugin upload, what to select from a complete GitHub download, how to activate the translator, and how to update an older upload.

**AI Live Translator** — Translate messages both ways.

## Which files do I upload?

### Recommended: build the dedicated ChatGPT plugin archive

Do **not** upload GitHub's automatic repository ZIP as the ChatGPT plugin. Download/extract the full repository, then run the included builder from the repository root:

```bash
python plugin/installation/build-chatgpt.py
```

On some systems, use `python3` instead of `python`. The script creates:

```text
dist/AI-Live-Translator-ChatGPT-Plugin-v1.0.7.zip
```

The exact versioned name is taken from the repository's `VERSION` file, so use the name printed by the script if a newer release is present. Upload **that generated file only**.

The builder packages the files ChatGPT needs:

- `plugin.json`, `README.md`, and `LICENSE`
- OpenAI composer/listing icons under `assets/`
- `prompt/`
- `skills/ai-live-translator/` and its supporting files
- `skills/setup/`

You do not need to upload the rest of the source repository, development tests, CI configuration, Claude manifest, or Codex manifest to ChatGPT. The builder chooses the correct files and checks that the package is valid.

### If you only want the prompt

For a manual, one-chat setup, open `prompt/live-translation.md`, copy its complete contents into the instruction area supported by your ChatGPT workspace, and start a new chat. This is a prompt-based setup, not an installed plugin, and how persistent it is depends on the ChatGPT feature you use.

## Upload the plugin

1. Download the complete project from the repository and extract it.
2. Open a terminal in the extracted project folder (the folder containing `VERSION` and `plugin.json`).
3. Run the builder command above and note the generated ZIP path.
4. In ChatGPT, open the plugin or skill management area available to your account or workspace.
5. Choose **Upload plugin** if that option is available, then select the generated `AI-Live-Translator-ChatGPT-Plugin-v*.zip`. The label and availability of upload controls can vary by account and workspace. If your workspace does not offer this route, follow its available Skills or Plugin Creator workflow; do not substitute GitHub's automatic source ZIP.
6. Finish the upload flow and confirm that **AI Live Translator** appears in your available plugins/skills.
7. Start a **new chat**, invoke/select **AI Live Translator**, and follow its setup prompt to choose the two languages.
8. Send one short test message in either language. The expected behavior is one translation into the other selected language, without an answer to the message itself.

For voice, the project recommends ChatGPT Voice with **Voice → Model → Advanced** (the menu may be arranged differently as ChatGPT changes). This setting has been tested extensively by the project owner. Keep language detection on Auto-detect when appropriate and let the transcript finish before sending.

## Update an older ChatGPT upload

1. Build the current ZIP from the current project files using the script above, or download the matching versioned ChatGPT archive from the project's release/library source.
2. In ChatGPT's plugin details or management screen, choose **Upload new version** if shown, then select the new ZIP.
3. If your account does not show an update action, remove the old manually uploaded copy and upload the new ZIP using the available workflow.
4. Start a new chat and test a single translation. Existing conversations may continue using the behavior they already loaded.

A GitHub repository update does not automatically replace a manually uploaded ChatGPT plugin. The ZIP must be uploaded to the account/workspace again unless that plugin was installed through a source-sync workflow.

## Voice clarity and translation quality

Speak one utterance at a time and label the speaker when the transcript could be ambiguous, for example **“My message: …”** and **“Other person's message: …”**. Avoid speaking over the other person, television, or nearby conversations. ChatGPT supplies a transcript to the translator; the translator itself cannot listen to the microphone, identify the physical speaker, or reliably distinguish background noise. If multiple voices are mixed or the transcript is uncertain, repeat the sentence cleanly, type it, or identify the speaker. Do not ask the AI to guess.

The tool is built from a prompt and skills, not a dedicated translation model. ChatGPT is the most extensively tested host for this project and is the recommended starting point. Other compatible AI systems can be tried, but quality and instruction-following can differ across models, language pairs, and sessions.

## Official references

- [OpenAI Help Center: Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/12584461-plugins-in-chatgpt-and-codex)
- [OpenAI Help Center: Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt)
