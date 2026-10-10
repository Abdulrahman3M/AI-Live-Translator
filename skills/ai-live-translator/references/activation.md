# Activation and state

This skill is intentionally session-scoped. Installed skill metadata allows discovery; it does **not** imply automatic activation in unrelated chats. Activate by using the host's skill mechanism or pasting the portable prompt. State sequence:

```text
INACTIVE --explicit skill activation--> SETUP --pair supplied--> READY
READY --bilingual onboarding delivered--> TRANSLATING
TRANSLATING --initial direct address: pause--> PAUSED
PAUSED --initial direct address: resume--> TRANSLATING
TRANSLATING --initial direct address: change pair--> READY
TRANSLATING/PAUSED --initial direct address: stop--> STOPPED
```

Ordinary text during TRANSLATING never changes state. Host-native slash commands may act as direct controls if executed as commands by the host. Reply *only with translated text* unless explicitly addressed or clarification strictly necessary.
