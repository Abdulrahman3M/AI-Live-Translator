# Voice Turn Management — Host-Aware Behavioral Policy

This policy is **best-effort instruction guidance**, not microphone/DSP code. It applies to voice-derived input when a host supplies useful transcript/turn information. The existing text-only translation contract remains authoritative for committed chat messages. See `../../../docs/agent-guides/CHATGPT.md` for platform limits.

## 1. Semantic End-of-Turn Detection

- If the host exposes **interim/partial speech** and a pending turn, prefer semantic completion over a brief pause: a breath, hesitation, filler, or an unfinished clause is not automatically a completed utterance. Use punctuation, grammar, meaning, and context together; silence alone is insufficient.
- Give a speaker the chance to finish naturally **without requiring** "I am done", a wake phrase, or button press when the host allows it. Do not enforce an arbitrary ten-second delay: this skill has no access to a silence timer or host voice activity detector.
- If the host has already finalized a message, process that message normally. **Do not hold up complete typed text or deliberately delay finalized transcripts** waiting for extra audio that the skill cannot receive.
- If a finalized transcript is genuinely too incomplete or ambiguous to translate faithfully, ask once in the source language for a clear repeat or continuation; do not infer missing words or silently combine unrelated turns.
- Short complete phrases (e.g., "Yes.", "No.", "Tomorrow.") are valid translation inputs and must not be dropped just because they are brief.

## 2. Uninterrupted Translation Mode

- Once translation output begins, **prioritize finishing the current translation once**, with no source echo or duplicate output. Do not voluntarily switch to unrelated conversation from background words detected during output.
- If the host exposes output-state or interruption preferences, **request non-interruptible playback when available**, then listen for the next speaker after the current response finishes. Do not claim a skill can mute a microphone, disable barge-in, buffer speech, or force playback completion.
- The hosting voice engine can still interrupt, truncate, or cancel speech. If a response is interrupted, avoid claiming it finished or automatically restarting a full duplicate. Continue/retry only where the host gives a reliable continuation mechanism or an explicit direct instruction.
- Explicit controls addressed to the agent and higher-priority safety controls remain authoritative; this policy is **not** a blanket instruction to ignore all inputs.

## 3. Intentional Speech, Noise, and Language Direction

1. **Intent gate:** Treat the host-provided *utterance* as intentional speech only when the transcript and context clearly support it. Ignore *clearly marked* noise, stray background conversation, TV, or overlapping speech unrelated to the participants. Never suppress a genuine short turn on length alone.
2. **Language gate:** Identify the dominant source language using the complete utterance, its words, script, and conversation context from **either selected language**, not speaker identity or accent alone. Mixed language follows the existing language-detection policy.
3. **Translation gate:** Translate exactly once into the other selected language, preserving meaning, dialect, names, negation, and tone. If foreground speech versus ambient speech or translation direction remains uncertain, ask for one clean repeat or speaker label rather than inventing ownership, language, or words.

## 4. Availability and Priority

The skill receives messages/transcripts supplied by the host. It cannot inspect raw audio, perform noise suppression, voice identification, voice activity detection, semantic endpointing at the engine level, or manage playback automatically. Instructions above affect the agent's **interpretation** of data where available, never override the host's capture/end-of-turn/interrupt pipeline. In ChatGPT Advanced Voice, pause thresholds, playback lock, and microphone gating are not exposed to this Markdown skill. An independently engineered realtime client with supported audio/turn controls would be needed for enforceable audio behavior.

Normal priority remains: host policies and safety > explicit direct control > translation-only contract > this best-effort voice guidance. No additional plugins, server, audio recording, tracking, or secret access are required.
