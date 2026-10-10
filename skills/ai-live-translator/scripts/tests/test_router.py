import importlib.util
import json
import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('alt_router', SKILL_ROOT/'scripts/router.py')
router = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = router
SPEC.loader.exec_module(router)

class RouterTests(unittest.TestCase):
    def test_all_golden_control_cases(self):
        p=SKILL_ROOT/'examples/control-cases.jsonl'
        for line in p.read_text(encoding='utf-8').splitlines():
            case=json.loads(line)
            with self.subTest(case=case['id'],input=case['input']):
                actual=router.route(case['input'],case['mode'])
                self.assertEqual(actual['kind'],case['expected_kind'])
                self.assertEqual(actual['mode'],case['expected_mode'])
                if case['expected_action']:
                    self.assertEqual(actual['action'],case['expected_action'])
                else:self.assertNotIn('action',actual)
    def test_speaker_prefix_stripped(self):
        data=router.route('الطرف الآخر: Good morning')
        self.assertEqual(data['speaker'],'OTHER')
        self.assertEqual(data['content'],'Good morning')
    def test_host_override_alias(self):
        x=router.route('MyTranslator, status',agent_names=('MyTranslator',))
        self.assertEqual(x['kind'],'CONTROL')
        self.assertEqual(x['action'],'STATUS')
    def test_agent_name_inside_content(self):
        self.assertEqual(router.route('Please tell ChatGPT to stop')['kind'],'TRANSLATE_ONLY')
    def test_invalid_mode_rejected(self):
        with self.assertRaises(ValueError):router.route('anything','UNKNOWN')

if __name__=='__main__': unittest.main()
