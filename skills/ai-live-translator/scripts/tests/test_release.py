import importlib.util
import sys
import unittest
from pathlib import Path
SKILL_ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('alt_validator', SKILL_ROOT/'scripts/validate.py')
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)
class ReleaseTests(unittest.TestCase):
    def test_package_integrity(self):
        self.assertEqual(validator.validate(),[])
    def test_stats_command(self):
        import subprocess
        import json
        result=subprocess.run([sys.executable,str(SKILL_ROOT/'scripts/corpus_stats.py')],capture_output=True,text=True,check=True)
        stats=json.loads(result.stdout)
        self.assertGreaterEqual(stats['directional_records'],600)
        self.assertGreaterEqual(stats['control_fixtures'],70)
    def test_corpus_is_bidirectional(self):
        import json
        examples=SKILL_ROOT/'examples'
        for f in examples.glob('en-*.jsonl'):
            rows=[json.loads(line) for line in f.read_text(encoding='utf-8').splitlines()]
            lookup={(r['source_language'],r['target_language'],r['source'],r['target']) for r in rows}
            for r in rows:
                with self.subTest(id=r['id']):
                    self.assertIn((r['target_language'],r['source_language'],r['target'],r['source']),lookup)
if __name__=='__main__':unittest.main()
