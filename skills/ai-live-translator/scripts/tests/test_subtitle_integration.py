import importlib.util
import pathlib
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[4]

class SubtitleIntegrationTests(unittest.TestCase):
    def test_home_routes_both_skills(self):
        text = (ROOT / 'skills/setup/SKILL.md').read_text(encoding='utf-8-sig')
        for entry in ('../ai-live-translator/SKILL.md', '../subtitle-translator/SKILL.md'):
            self.assertIn(entry, text)
            self.assertTrue((ROOT / 'skills/setup' / entry).resolve().is_file())
        self.assertIn('without an explicit function', text)

    def test_subtitle_contract_and_reference(self):
        text = (ROOT / 'skills/subtitle-translator/SKILL.md').read_text(encoding='utf-8-sig')
        for value in ('target language', 'dialect', 'color', 'ASS', 'timings', 'BOM'):
            self.assertIn(value, text)
        ref = (ROOT / 'skills/subtitle-translator/references/ass-rtl.md').read_text(encoding='utf-8-sig')
        for value in ('[Script Info]', '[V4+ Styles]', '[Events]', 'U+202B', r'{\c&H3CC8FF&}', r'\N'):
            self.assertIn(value, ref)

    def test_direct_translation_and_reference_precedence_are_explicit(self):
        text = (ROOT / 'skills/subtitle-translator/SKILL.md').read_text(encoding='utf-8-sig')
        for value in ('ordered batches', 'checkpoint', 'external service', 'explicit user choices', 'reference', 'partial'):
            self.assertIn(value, text)

    def test_persistent_execution_contract_is_packaged_in_each_subtitle_plugin(self):
        for script in ('build-chatgpt.py', 'build_release.py'):
            spec = importlib.util.spec_from_file_location('persistent_' + script.replace('-', '_'), ROOT / 'plugin/installation' / script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            with tempfile.TemporaryDirectory() as temp:
                paths = [pathlib.Path(temp) / 'chatgpt.zip'] if script == 'build-chatgpt.py' else list(module.build_archives(pathlib.Path(temp)).values())[:2]
                if script == 'build-chatgpt.py':
                    module.build_archive(paths[0])
                for path in paths:
                    with zipfile.ZipFile(path) as archive:
                        contract = archive.read('skills/subtitle-translator/SKILL.md').decode('utf-8')
                        for phrase in ('large event count', 'ordered batches', 'existing goal', 'without confirmation', 'every source event', 'partial output'):
                            self.assertIn(phrase, contract, str(path))

    def test_chatgpt_and_claude_archives_include_subtitle_skill(self):
        for script in ('build-chatgpt.py', 'build_release.py'):
            spec = importlib.util.spec_from_file_location('builder_' + script.replace('-', '_'), ROOT / 'plugin/installation' / script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            with tempfile.TemporaryDirectory() as temp:
                if script == 'build-chatgpt.py':
                    output = pathlib.Path(temp) / 'chatgpt.zip'
                    module.build_archive(output)
                else:
                    output = module.build_archives(pathlib.Path(temp))['claude_code']
                with zipfile.ZipFile(output) as archive:
                    self.assertIn('skills/subtitle-translator/SKILL.md', archive.namelist())
                    self.assertIn('skills/subtitle-translator/references/ass-rtl.md', archive.namelist())
                    self.assertIn('skills/subtitle-translator/scripts/subtitle_tools.py', archive.namelist())
                    self.assertIn('skills/subtitle-translator/examples/sample-reference.ass', archive.namelist())
                    self.assertIsNone(archive.testzip())

if __name__ == '__main__':
    unittest.main()
