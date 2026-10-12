import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
SKILL_ROOT = Path(__file__).resolve().parents[2]
ROOT = SKILL_ROOT.parents[1]
SPEC = importlib.util.spec_from_file_location('alt_validator', SKILL_ROOT/'scripts/validate.py')
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)
BUILD_SPEC = importlib.util.spec_from_file_location('chatgpt_builder', ROOT/'plugin/installation/build-chatgpt.py')
builder = importlib.util.module_from_spec(BUILD_SPEC)
sys.modules[BUILD_SPEC.name] = builder
BUILD_SPEC.loader.exec_module(builder)
class ReleaseTests(unittest.TestCase):
    def test_package_integrity(self):
        self.assertEqual(validator.validate(),[])
    def test_stats_command(self):
        import subprocess
        import json
        result=subprocess.run([sys.executable,str(SKILL_ROOT/'scripts/corpus_stats.py')],capture_output=True,text=True,check=True)
        stats=json.loads(result.stdout)
        self.assertEqual(stats['directional_records'],664)
        self.assertEqual(stats['curated_bilingual_pairs'],332)
        self.assertEqual(stats['control_fixtures'],81)
        self.assertEqual(stats['clarification_fixtures'],2)
        self.assertEqual(stats['files']['clarification-cases.jsonl']['directions'],{})
    def test_corpus_is_bidirectional(self):
        examples=SKILL_ROOT/'examples'
        for f in examples.glob('en-*.jsonl'):
            rows=[json.loads(line) for line in f.read_text(encoding='utf-8').splitlines()]
            lookup={(r['source_language'],r['target_language'],r['source'],r['target']) for r in rows}
            for r in rows:
                with self.subTest(id=r['id']):
                    self.assertIn((r['target_language'],r['source_language'],r['target'],r['source']),lookup)

    def test_branding_is_consistent_across_manifests(self):
        portable=json.loads((ROOT/'plugin.json').read_text(encoding='utf-8'))
        codex=json.loads((ROOT/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))
        claude=json.loads((ROOT/'.claude-plugin/plugin.json').read_text(encoding='utf-8'))
        metadata=json.loads((ROOT/'plugin/metadata.json').read_text(encoding='utf-8'))
        portable_interface=portable['extensions']['com.openai']['interface']
        codex_interface=codex['interface']
        self.assertEqual(portable_interface['displayName'],'AI Live Translator')
        self.assertEqual(metadata['name'],'AI Live Translator')
        self.assertEqual(metadata['short_description'],portable_interface['shortDescription'])
        self.assertEqual(codex_interface['displayName'],portable_interface['displayName'])
        self.assertEqual(portable_interface['shortDescription'],'Translate messages both ways')
        self.assertEqual(codex_interface['shortDescription'],portable_interface['shortDescription'])
        self.assertEqual({portable['description'],codex['description'],claude['description'],metadata['description']},
                         {'Translate messages both ways'})
        self.assertIn('Translate messages both ways',(ROOT/'README.md').read_text(encoding='utf-8'))
        self.assertIn('ترجمة الرسائل ذهابًا وإيابًا',(ROOT/'README.ar.md').read_text(encoding='utf-8'))

    def test_platform_installation_overviews_are_easy_to_find(self):
        english=(ROOT/'docs/installation.md').read_text(encoding='utf-8')
        arabic=(ROOT/'docs/installation.ar.md').read_text(encoding='utf-8')
        readme=(ROOT/'README.md').read_text(encoding='utf-8')
        readme_ar=(ROOT/'README.ar.md').read_text(encoding='utf-8')
        self.assertIn('[Choose an installation method](docs/installation.md)',readme)
        self.assertIn('[اختر طريقة التثبيت](docs/installation.ar.md)',readme_ar)
        for host in ('ChatGPT','Codex','Claude Code','GitHub Copilot','Gemini'):
            self.assertIn(host,english)
        self.assertIn('ChatGPT',arabic)
        self.assertIn('Claude Code',arabic)

    def test_supported_icon_paths_resolve_and_png_sizes_match(self):
        portable=json.loads((ROOT/'plugin.json').read_text(encoding='utf-8'))
        codex=json.loads((ROOT/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))
        interface=portable['extensions']['com.openai']['interface']
        self.assertEqual(interface['composerIcon'],'./assets/ai-live-translator-icon-128.png')
        self.assertEqual(interface['logo'],'./assets/ai-live-translator-icon-512.png')
        self.assertEqual(codex['interface']['composerIcon'],interface['composerIcon'])
        self.assertEqual(codex['interface']['logo'],interface['logo'])
        for size in (64,128,256,512):
            path=ROOT/f'assets/ai-live-translator-icon-{size}.png'
            self.assertTrue(path.is_file(),str(path))
            header=path.read_bytes()[:24]
            self.assertEqual(header[:8],b'\x89PNG\r\n\x1a\n')
            self.assertEqual((int.from_bytes(header[16:20],'big'),int.from_bytes(header[20:24],'big')),(size,size))
        agent_metadata=(SKILL_ROOT/'agents/openai.yaml').read_text(encoding='utf-8')
        self.assertIn('display_name: AI Live Translator',agent_metadata)
        self.assertIn('short_description: Translate messages both ways',agent_metadata)
        self.assertIn('icon_small: ./assets/ai-live-translator-icon-64.png',agent_metadata)
        self.assertIn('icon_large: ./assets/ai-live-translator-icon-512.png',agent_metadata)
        self.assertEqual((SKILL_ROOT/'assets/ai-live-translator-icon-64.png').read_bytes(),(ROOT/'assets/ai-live-translator-icon-64.png').read_bytes())
        self.assertEqual((SKILL_ROOT/'assets/ai-live-translator-icon-512.png').read_bytes(),(ROOT/'assets/ai-live-translator-icon-512.png').read_bytes())

    def test_chatgpt_archive_contains_declared_icon_assets(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            archive_path=Path(directory)/'plugin.zip'
            builder.build_archive(archive_path)
            with __import__('zipfile').ZipFile(archive_path) as archive:
                names=set(archive.namelist())
                self.assertIn('assets/ai-live-translator-icon.svg',names)
                self.assertIn('assets/ai-live-translator-icon-128.png',names)
                self.assertIn('assets/ai-live-translator-icon-512.png',names)

    def test_curated_examples_cover_dialect_names_dates_and_times(self):
        examples=[json.loads(line) for line in (SKILL_ROOT/'examples/en-ar.jsonl').read_text(encoding='utf-8').splitlines()]
        by_id={item['id']:item for item in examples}
        for case_id in ('en-ar-0196-a','en-ar-0196-b','en-ar-0197-a','en-ar-0197-b'):
            with self.subTest(id=case_id):
                self.assertIn(case_id,by_id)
        self.assertIn('Maya',by_id['en-ar-0196-a']['source'])
        self.assertIn('٢٧ أكتوبر',by_id['en-ar-0196-b']['source'])
        self.assertIn('PDF',by_id['en-ar-0197-a']['source'])
        self.assertIn('dialect',by_id['en-ar-0196-a']['category'])

    def test_ambiguity_fixtures_require_source_language_clarification(self):
        path=SKILL_ROOT/'examples/clarification-cases.jsonl'
        cases=[json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
        self.assertGreaterEqual(len(cases),2)
        self.assertEqual({case['source_language'] for case in cases},{'en','ar'})
        for case in cases:
            with self.subTest(id=case['id']):
                self.assertEqual(case['expected_action'],'ASK_CLARIFICATION')
                self.assertTrue(case['message'].strip())
                self.assertTrue(case['clarification_question'].strip())
if __name__=='__main__':unittest.main()
