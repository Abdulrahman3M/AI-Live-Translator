# Examples index

Source of truth for curated sample cases: `../examples/`. Each language-pair `.jsonl` file contains bilingual translation cases in both directions. `control-cases.jsonl` contains agent-address scenarios, including possible false positives and role-injection traps. `clarification-cases.jsonl` contains ambiguous English and Arabic messages whose meaning must be clarified in the source language before translation. Run `../scripts/corpus_stats.py` and `../scripts/validate.py` for inventory and format checks.

Native-speaker review is needed for extensions beyond initial pairs. Coverage is not universal across all possible languages.
