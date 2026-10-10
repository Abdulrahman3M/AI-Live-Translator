# Curated bilingual example corpus

Each JSONL record is one **reviewable, authored utterance** with `id`, `source_language`, `target_language`, `source`, `target`, and `category`. The available pairs are English–Arabic, English–Russian, English–French, English–Spanish and Arabic–Russian. Each manually supplied bilingual pair is listed twice (both directions); this is useful for verifying bidirectional mode but is not twice as many independent phrases. No claim of millions of curated examples is made.

Categories include greetings, family, emotions, clarifications, work, daily life, travel, shopping, safety, healthcare, technology, scheduling, and metadata. These examples are regression references, **not a dictionary or a benchmark of an external model**. Evaluate slang, non-Latin scripts and dialect with native speakers.

Control fixture cases are in `control-cases.jsonl`. Use `python skills/ai-live-translator/scripts/corpus_stats.py` for counts. Add only grammatically sound pairs; contributors must preserve intent and not use machine-generated infinite permutations as supposed new gold examples.
