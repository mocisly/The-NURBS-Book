"""Check semantic index coverage and exact preservation of formulas/code/artwork."""
from pathlib import Path
import collections,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/backmatter'
if not (WORK/'baseline.json').exists():
    from compile_minted_book import inputs
    current=json.loads((ROOT/'image_tex/reports/backmatter-compile.json').read_text(encoding='utf-8'))
    assert inputs()==current['source_hashes'],'Sources changed since the reviewed backmatter publication.'
    print('Current sources match the reviewed bibliography/index publication.')
    raise SystemExit(0)
baseline=json.loads((WORK/'baseline.json').read_text(encoding='utf-8'))
changes=json.loads((WORK/'citation-migration.json').read_text(encoding='utf-8'))
def expected_citations(s,path):
    mapping={r['before']:r['after']for r in changes if r['path']==path}
    return re.sub(r'\[([^\]\n]+)\]',lambda m:mapping.get(m[0],m[0]),s)
blocks=0;figure_calls=0
for n in range(1,14):
    name=f'chapter/{n}.tex';before=(WORK/'before'/name).read_text(encoding='utf-8');now=(ROOT/name).read_text(encoding='utf-8')
    plain=re.sub(r'\\BookIndexMark\{p\d+\}','',now)
    assert plain==expected_citations(before,name),f'Unintended body change: {name}'
    minted=re.findall(r'\\begin\{minted\}.*?\\end\{minted\}',now,re.S)
    assert minted==baseline['minted'][f'{n}.tex'],name;blocks+=len(minted)
    old_figs=re.findall(r'\\BookFigure(?:\[[^\]]*\])?\{[^}]+\}',before)
    assert old_figs==re.findall(r'\\BookFigure(?:\[[^\]]*\])?\{[^}]+\}',now),name;figure_calls+=len(old_figs)
    assert not any('BookIndexMark'in s for s in re.findall(r'(?<!\\)%[^\n]*',now)),name
    assert not [m for m in re.findall(r'\[[^\]\n]*[A-Za-z]+\d{2}[a-z]?[^\]\n]*\]',plain)if '\\'not in m],name
for path,h in baseline['native_figure_hashes'].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h,path
assert blocks==109 and figure_calls==435
entries=json.loads((ROOT/'backmatter/index-entries.json').read_text(encoding='utf-8'))
points=json.loads((ROOT/'backmatter/index-locations.json').read_text(encoding='utf-8'))
assert len(entries)==359 and len({e['id']for e in entries})==359
assert {e['id']for e in entries}=={i for p in points for i in p['entries']}
assert len(points)==len({p['id']for p in points})
for p in points:
    s=(ROOT/f"chapter/{p['chapter']}.tex").read_text(encoding='utf-8');assert s.count(r'\BookIndexMark{'+p['id']+'}')==1,p['id']
    for block in re.findall(r'\\begin\{minted\}.*?\\end\{minted\}',s,re.S):assert p['id']not in block
bib=(ROOT/'chapter/14.tex').read_text(encoding='utf-8');found=re.findall(r'\\bibitem\[([^]]+)\]\{([^}]+)\}',bib)
assert len(found)==173 and all(a==b for a,b in found)
data=json.loads((ROOT/'backmatter/bibliography.json').read_text(encoding='utf-8'))
matches=list(re.finditer(r'\\bibitem\[[^]]+\]\{([^}]+)\}\s*',bib))
for i,m in enumerate(matches):
    end=matches[i+1].start()if i+1<len(matches)else bib.index(r'\end{BookBibliography}')
    assert m[1]==data[i]['key']and bib[m.end():end].strip()==expected_citations(data[i]['text'],'chapter/14.tex'),m[1]
keys={a for a,b in found};used=set()
for n in range(1,15):
    s=(ROOT/f'chapter/{n}.tex').read_text(encoding='utf-8')
    for group in re.findall(r'\\cite\{([^}]+)\}',s):used.update(group.split(','))
assert used<=keys,used-keys
original=(ROOT/'image_tex/reports/backmatter-index-original.tex').read_text(encoding='utf-8').splitlines()
numeric={n for n,line in enumerate(original,1)if re.search(r'\d',line)and n not in [434,806]}
covered={n for e in entries for n in e['source_lines']};assert numeric<=covered
report=dict(status='passed',preserved_native_sources=len(baseline['native_figure_hashes']),preserved_figure_calls=figure_calls,preserved_minted_blocks=blocks,bibliography_entries=173,unique_cited_keys=len(used),citation_groups_migrated=len(changes),index_entries=len(entries),index_source_locations=len(points),original_numeric_index_lines_covered=len(numeric),original_running_header_lines_removed=[434,806],body_text_and_formulas_unchanged_except_citations_and_invisible_marks=True)
(WORK/'source-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
