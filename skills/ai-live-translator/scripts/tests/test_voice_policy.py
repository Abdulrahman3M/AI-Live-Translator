import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / "skills/ai-live-translator"
CASES = SKILL / "examples/voice-turn-cases.json"
POLICY = SKILL / "rules/voice-turn-management.md"

class VoiceTurnPolicyTests(unittest.TestCase):
    def test_policy_is_present_and_host_aware(self):
        policy = POLICY.read_text(encoding="utf-8")
        for expected in (
            "Semantic End-of-Turn Detection",
            "Uninterrupted Translation Mode",
            "Intentional Speech, Noise, and Language Direction",
            "interim/partial speech",
            "ten-second delay",
            "cannot inspect raw audio",
            "ChatGPT Advanced Voice",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, policy)

    def test_corpus_covers_voice_failure_modes_without_claiming_audio_control(self):
        cases = json.loads(CASES.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 12)
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        actions = {case["expected_action"] for case in cases}
        self.assertTrue({
            "WAIT_FOR_SEMANTIC_COMPLETION", "PRIORITIZE_CURRENT_TRANSLATION",
            "IGNORE_UNRELATED_BACKGROUND", "DETECT_LANGUAGE_AND_TRANSLATE_ONCE",
            "ASK_CLARIFICATION", "TRANSLATE_ONCE", "NO_FALSE_COMPLETION",
            "HONOR_DIRECT_CONTROL"
        }.issubset(actions))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(all(case.get(k) for k in ("scenario", "host_signal", "expected_action", "note")))

    def test_voice_policy_referenced_in_skill_prompt_and_readmes(self):
        for rel in ("skills/ai-live-translator/SKILL.md", "prompt/live-translation.md",
                    "README.md", "README.ar.md", "docs/agent-guides/CHATGPT.md",
                    "docs/agent-guides/CHATGPT.ar.md"):
            with self.subTest(path=rel):
                self.assertIn("Voice Turn Management", (ROOT / rel).read_text(encoding="utf-8"))

    def test_existing_text_only_translation_invariants_preserved(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        prompt = (ROOT / "prompt/live-translation.md").read_text(encoding="utf-8")
        self.assertIn("text-only", skill)
        self.assertIn("**exactly one final translation", prompt)
        self.assertIn("## READY", prompt)
        self.assertIn("## TRANSLATING", prompt)
        self.assertIn("## Priority and limitations", prompt)

if __name__ == "__main__":
    unittest.main()
