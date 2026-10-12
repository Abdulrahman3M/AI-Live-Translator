import importlib.util
import json
import re
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

    def test_release_metadata_is_synchronized_to_v1_0_7(self):
        self.assertEqual((ROOT/'VERSION').read_text(encoding='utf-8').strip(),'1.0.7')
        for relative in ('plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json','plugin/metadata.json'):
            with self.subTest(manifest=relative):
                self.assertEqual(json.loads((ROOT/relative).read_text(encoding='utf-8'))['version'],'1.0.7')
        self.assertEqual((ROOT/'README.md').read_text(encoding='utf-8').splitlines()[0],'# AI Live Translator · v1.0.7')
        self.assertEqual((ROOT/'README.ar.md').read_text(encoding='utf-8').splitlines()[0],'# AI Live Translator · v1.0.7')
        self.assertIn('## [1.0.7]',(ROOT/'CHANGELOG.md').read_text(encoding='utf-8'))

    def test_project_hero_is_a_wide_png_referenced_with_localized_alt_text(self):
        hero=ROOT/'assets/ai-live-translator-hero.png'
        self.assertTrue(hero.is_file(),str(hero))
        header=hero.read_bytes()[:24]
        self.assertEqual(header[:8],b'\x89PNG\r\n\x1a\n')
        width=int.from_bytes(header[16:20],'big')
        height=int.from_bytes(header[20:24],'big')
        self.assertGreater(width,height)
        for filename in ('README.md','README.ar.md'):
            with self.subTest(readme=filename):
                text=(ROOT/filename).read_text(encoding='utf-8')
                match=re.search(r'!\[([^\]]+)\]\(assets/ai-live-translator-hero\.png\)',text)
                self.assertIsNotNone(match)
                self.assertGreater(len(match.group(1).strip()),5)
        arabic=(ROOT/'README.ar.md').read_text(encoding='utf-8')
        match=re.search(r'!\[([^\]]+)\]\(assets/ai-live-translator-hero\.png\)',arabic)
        self.assertTrue(any(word in match.group(1) for word in ('ترجمة','الترجمة')))

    def test_release_builder_creates_four_versioned_verified_archives(self):
        release_builder_path=ROOT/'plugin/installation/build_release.py'
        self.assertTrue(release_builder_path.is_file(),str(release_builder_path))
        release_spec=importlib.util.spec_from_file_location('release_builder',release_builder_path)
        release_builder=importlib.util.module_from_spec(release_spec)
        sys.modules[release_spec.name]=release_builder
        release_spec.loader.exec_module(release_builder)
        output_root=ROOT/'dist'
        output_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=output_root) as directory:
            archives=release_builder.build_archives(Path(directory))
            self.assertEqual(set(archives),{'codex','claude_code','agent_skill','source'})
            expected_names={
                'codex':'AI-Live-Translator-Codex-Plugin-v1.0.7.zip',
                'claude_code':'AI-Live-Translator-Claude-Code-Plugin-v1.0.7.zip',
                'agent_skill':'AI-Live-Translator-Agent-Skill-v1.0.7.zip',
                'source':'AI-Live-Translator-Source-v1.0.7.zip',
            }
            for key,archive_path in archives.items():
                with self.subTest(package=key):
                    self.assertEqual(Path(archive_path).name,expected_names[key])
                    with __import__('zipfile').ZipFile(archive_path) as archive:
                        self.assertIsNone(archive.testzip())
                        names=set(archive.namelist())
                        self.assertTrue(names)
                        self.assertFalse(any(name.startswith(('.git/','dist/','__pycache__/','.venv/')) for name in names))
                        self.assertFalse(any(name.endswith(('.pyc','.tmp','.temp')) for name in names))
                        if key in ('codex','claude_code'):
                            manifest_path='.codex-plugin/plugin.json' if key=='codex' else '.claude-plugin/plugin.json'
                            manifest=json.loads(archive.read(manifest_path))
                            self.assertEqual(manifest['version'],'1.0.7')
                            for field in ('composerIcon','logo'):
                                asset=manifest.get('interface',{}).get(field)
                                if isinstance(asset,str) and asset.startswith('./'):
                                    self.assertIn(asset[2:],names)
                        if key=='codex':
                            for required in ('.codex-plugin/plugin.json','skills/setup/SKILL.md','skills/ai-live-translator/SKILL.md','plugin/commands/start.md','plugin/commands/help.md'):
                                self.assertIn(required,names)
                        elif key=='claude_code':
                            for required in ('.claude-plugin/plugin.json','plugin/commands/start.md','plugin/commands/help.md','skills/ai-live-translator/SKILL.md'):
                                self.assertIn(required,names)
                        elif key=='agent_skill':
                            for required in ('ai-live-translator/SKILL.md','ai-live-translator/agents/openai.yaml','ai-live-translator/rules/translation-contract.md','ai-live-translator/examples/en-ar.jsonl','ai-live-translator/references/activation.md','ai-live-translator/scripts/router.py','ai-live-translator/assets/ai-live-translator-icon-64.png'):
                                self.assertIn(required,names)
                            self.assertFalse(any('/tests/' in name for name in names))
                        else:
                            source_root='AI-Live-Translator-v1.0.7/'
                            self.assertTrue(all(name.startswith(source_root) for name in names))
                            for required in ('VERSION','plugin.json','assets/ai-live-translator-hero.png','skills/ai-live-translator/SKILL.md'):
                                self.assertIn(source_root+required,names)

    def test_five_release_assets_have_direct_links_in_bilingual_guides(self):
        assets=(
            'AI-Live-Translator-ChatGPT-Plugin-v1.0.7.zip',
            'AI-Live-Translator-Codex-Plugin-v1.0.7.zip',
            'AI-Live-Translator-Claude-Code-Plugin-v1.0.7.zip',
            'AI-Live-Translator-Agent-Skill-v1.0.7.zip',
            'AI-Live-Translator-Source-v1.0.7.zip',
        )
        base='https://github.com/Abdulrahman3M/AI-Live-Translator/releases/download/v1.0.7/'
        for filename in ('docs/installation.md','docs/installation.ar.md'):
            text=(ROOT/filename).read_text(encoding='utf-8')
            with self.subTest(guide=filename):
                for asset in assets:
                    self.assertIn(base+asset,text)
        build_guide=ROOT/'plugin/installation/BUILD-RELEASE.md'
        self.assertTrue(build_guide.is_file(),str(build_guide))
        build_text=build_guide.read_text(encoding='utf-8')
        self.assertIn('build-chatgpt.py',build_text)
        self.assertIn('build_release.py',build_text)

    def test_english_release_notes_cover_features_and_limits(self):
        release_notes=ROOT/'docs/releases/v1.0.7.md'
        self.assertTrue(release_notes.is_file(),str(release_notes))
        text=release_notes.read_text(encoding='utf-8')
        for phrase in ('bidirectional','text-only','ordinary messages','tone','context','dialect','explicitly addressing the agent','model'):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(),text.lower())
        self.assertNotRegex(text,r'[\u0600-\u06FF]')

    def test_readmes_surface_downloads_and_remove_duplicate_chatgpt_install_section(self):
        assets=(
            'AI-Live-Translator-ChatGPT-Plugin-v1.0.7.zip',
            'AI-Live-Translator-Codex-Plugin-v1.0.7.zip',
            'AI-Live-Translator-Claude-Code-Plugin-v1.0.7.zip',
            'AI-Live-Translator-Agent-Skill-v1.0.7.zip',
            'AI-Live-Translator-Source-v1.0.7.zip',
        )
        for filename,heading,guide in (('README.md','## Downloads','docs/installation.md'),('README.ar.md','## التنزيلات','docs/installation.ar.md')):
            text=(ROOT/filename).read_text(encoding='utf-8')
            with self.subTest(readme=filename):
                self.assertIn(heading,text)
                self.assertIn(guide,text)
                for asset in assets:
                    self.assertIn(asset,text)
                self.assertLessEqual(text.count('## حزمة التثبيت المخصصة لـ ChatGPT'),1)

    def test_agents_governance_documents_release_package_and_tag_flow(self):
        text=(ROOT/'AGENTS.md').read_text(encoding='utf-8')
        self.assertIn('plugin/installation/build_release.py',text)
        self.assertIn('portable Agent Skill',text)
        self.assertIn('GitHub Release',text)
        self.assertIn('tag',text.lower())

    def test_release_workflow_builds_all_archives_and_publishes_only_tags(self):
        workflow=(ROOT/'.github/workflows/build-chatgpt-plugin.yml').read_text(encoding='utf-8')
        self.assertIn('python plugin/installation/build-chatgpt.py',workflow)
        self.assertIn('python plugin/installation/build_release.py',workflow)
        self.assertIn('path: dist/*.zip',workflow)
        self.assertIn("if: startsWith(github.ref, 'refs/tags/v')",workflow)
        self.assertIn('docs/releases/v$(cat VERSION).md',workflow)
        self.assertIn('gh release create',workflow)

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
