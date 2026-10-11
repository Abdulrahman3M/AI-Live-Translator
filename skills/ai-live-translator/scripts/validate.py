#!/usr/bin/env python3
"""Offline package and fixture integrity validator. No non-stdlib requirements."""
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[3]
EXAMPLES=ROOT/'skills/ai-live-translator/examples'
NEEDED=['plugin.json','.codex-plugin/plugin.json','.agents/plugins/marketplace.json','skills/setup/SKILL.md','README.md','README.ar.md','AGENTS.md','VERSION','CHANGELOG.md','LICENSE','prompt/live-translation.md','prompt/setup-messages.md',
        'skills/ai-live-translator/SKILL.md','skills/ai-live-translator/rules/address-and-control.md',
        '.claude-plugin/plugin.json','plugin/metadata.json','plugin/installation/INSTALL.md','plugin/commands/start.md']
def validate():
    errors=[]
    for rel in NEEDED:
        if not (ROOT/rel).is_file(): errors.append('Missing '+rel)
    if errors:return errors
    version=(ROOT/'VERSION').read_text(encoding='utf-8').strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+',version): errors.append('VERSION is not SemVer x.y.z')
    plugin=json.loads((ROOT/'.claude-plugin/plugin.json').read_text(encoding='utf-8'))
    metadata=json.loads((ROOT/'plugin/metadata.json').read_text(encoding='utf-8'))
    portable=json.loads((ROOT/'plugin.json').read_text(encoding='utf-8'))
    codex=json.loads((ROOT/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    for field,value in [('plugin.version',plugin.get('version')),('metadata.version',metadata.get('version')),('portable.version',portable.get('version')),('codex.version',codex.get('version'))]:
        if value!=version: errors.append(f'{field} differs from VERSION')
    for doc in ['README.md','README.ar.md','AGENTS.md','prompt/live-translation.md']:
        if version not in (ROOT/doc).read_text(encoding='utf-8'):errors.append('Version not synchronized in '+doc)
    if ('['+version+']') not in (ROOT/'CHANGELOG.md').read_text(encoding='utf-8'):errors.append('Missing current changelog entry')
    prompt_text=(ROOT/'prompt/live-translation.md').read_text(encoding='utf-8')
    setup_text=(ROOT/'prompt/setup-messages.md').read_text(encoding='utf-8')
    readme_text=(ROOT/'README.md').read_text(encoding='utf-8')
    ready=prompt_text.split('## READY',1)[1].split('## TRANSLATING',1)[0]
    required_user_guidance=['both selected languages','please use the clear, standard or formal form','avoid local dialects','text of my next message is','repeat or rephrase the message more clearly','never show setup or accuracy advice in a language outside the selected pair']
    for phrase in required_user_guidance:
        if phrase.lower() not in prompt_text.lower(): errors.append('Missing user guidance rule: '+phrase)
    for phrase in ['The text of my next message is:','If your message is unclear','Modern Standard Arabic','standard English']:
        if phrase.lower() not in setup_text.lower(): errors.append('Missing bilingual setup copy: '+phrase)
    for phrase in ['## End-user setup guidance','## Advanced user and maintainer guidance','## Translation contract']:
        if phrase not in readme_text: errors.append('Missing README guidance section: '+phrase)
    if 'Voice Advanced' in ready or "ChatGPT's" in ready:
        errors.append('Host-specific workflow leaked into end-user READY guidance')
    skill=(ROOT/'skills/ai-live-translator/SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith('---\n'):errors.append('Skill missing YAML frontmatter')
    else:
        front=skill.split('---',2)[1]
        for key in ['name: ai-live-translator','description:']:
            if key not in front:errors.append('Skill missing '+key)
    for cmd in plugin.get('commands',{}).values():
        if not (ROOT/cmd.get('source','')[2:]).is_file():errors.append('Missing Claude command '+str(cmd))
    if portable.get('extensions',{}).get('com.openai',{}).get('onboardingSkill')!='./skills/setup/SKILL.md':errors.append('Bad portable onboarding skill path')
    if any(len(d)>64 for d in [plugin['name']]):errors.append('Bad plugin name')
    primary={x.name for x in ROOT.iterdir() if x.is_dir() and not x.name.startswith('.')}
    if primary!={'prompt','skills','plugin'}: errors.append('Expected three functional directories, got '+str(primary))
    seen=set(); directions=set(); categories=set(); count=0
    for file in sorted(EXAMPLES.glob('*.jsonl')):
        for index,line in enumerate(file.read_text(encoding='utf-8').splitlines(),1):
            if not line.strip():continue
            try:r=json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f'{file.name}:{index} invalid JSON {e}');continue
            if file.name=='control-cases.jsonl':
                if not {'input','mode','expected_kind','expected_action','expected_mode'} <=r.keys():errors.append('Incomplete control fixture')
                continue
            if not {'id','source_language','target_language','source','target','category'} <= r.keys():errors.append(f'Incomplete corpus record {file.name}:{index}');continue
            if not r['source'].strip() or not r['target'].strip() or r['source_language']==r['target_language']:
                errors.append(f'Invalid corpus example {file.name}:{index}')
            if r['id'] in seen:errors.append('Duplicate ID: '+r['id'])
            seen.add(r['id']);directions.add((r['source_language'],r['target_language']));categories.add(r['category']);count+=1
    if count<500: errors.append(f'Too few directional examples: {count}')
    if len(categories)<10:errors.append('Insufficient categories')
    if len(directions)<8:errors.append('Insufficient language directions')
    info=json.loads((ROOT/'plugin/corpus-counts.json').read_text(encoding='utf-8'))
    if info['directional_records']!=count:errors.append('Corpus counts mismatch')
    return errors
if __name__=='__main__':
    failures=validate()
    if failures:
        print('VALIDATION FAILED:'); print('\n'.join(' - '+e for e in failures));sys.exit(1)
    print('VALIDATION PASSED: manifest, version, portable skill, 3-folder architecture and multilingual corpus')
