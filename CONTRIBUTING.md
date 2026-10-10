# Contributing to AI Live Translator

Thanks for improving cross-language human communication. Keep changes grounded in genuine spoken or written usage rather than inflated synthetic benchmark counts.

- Follow `AGENTS.md`; preserve exactly three main functional directories: `prompt/`, `skills/`, `plugin/`.
- Runtime behavior lives in the skill rules. Keep the portable prompt and host adapters consistent with those rules.
- Add new bilingual pairs as two JSONL records with distinct, stable IDs. Preserve both directions; don't claim that directional duplication creates two independent source phrases.
- For every new direct-address control case, add a positive/negative pair to `skills/ai-live-translator/examples/control-cases.jsonl`.
- Check idioms, politeness, tense, negation, numbers, names, typography, dialect and age/gender assumptions with fluent reviewers.
- Validate offline:

```sh
python skills/ai-live-translator/scripts/validate.py
python -m unittest discover -s skills/ai-live-translator/scripts/tests -v
```

- Model-output quality requires separate evaluation; passing local tests only certifies the package structure and deterministic router.
- Before cutting a release, synchronize `VERSION`, `.claude-plugin/plugin.json`, `plugin/metadata.json`, both README headings, prompt version, `AGENTS.md`, and `CHANGELOG.md`.
