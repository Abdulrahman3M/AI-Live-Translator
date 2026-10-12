#!/usr/bin/env python3
"""Count authored examples and directions without network access or third-party packages."""
from pathlib import Path
import collections, json
EXAMPLES=Path(__file__).resolve().parents[1]/'examples'
def stats():
    files={}
    for p in sorted(EXAMPLES.glob('*.jsonl')):
        lines=[json.loads(line) for line in p.read_text(encoding='utf-8').splitlines() if line.strip()]
        non_translation=p.name in {'control-cases.jsonl','clarification-cases.jsonl'}
        files[p.name]={'records':len(lines),'directions':dict(collections.Counter(f"{x['source_language']}→{x['target_language']}" for x in lines)) if not non_translation else {}}
    translation_files={name:file for name,file in files.items() if name not in {'control-cases.jsonl','clarification-cases.jsonl'}}
    return {'files':files,'directional_records':sum(f['records'] for f in translation_files.values()),
            'curated_bilingual_pairs':sum(f['records']//2 for f in translation_files.values()),
            'control_fixtures':files.get('control-cases.jsonl',{}).get('records',0),
            'clarification_fixtures':files.get('clarification-cases.jsonl',{}).get('records',0)}
if __name__=='__main__': print(json.dumps(stats(),indent=2,ensure_ascii=False))
