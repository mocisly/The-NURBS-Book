"""Verify geometric data and code survive physical-size changes."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/figure-layout'
if not (WORK/'baseline.json').exists():
    from compile_minted_book import inputs
    report=ROOT/'image_tex/reports/backmatter-compile.json'
    if not report.exists():report=ROOT/'image_tex/reports/figure-layout-compile.json'
    archived=json.loads(report.read_text(encoding='utf-8'))
    assert inputs()==archived['source_hashes'],'Sources changed since the reviewed publication.'
    print('Current figure layout sources match the reviewed publication.')
    raise SystemExit(0)
b=json.loads((WORK/'baseline.json').read_text(encoding='utf-8'))
changed=[];checked=[]
for name,old in b['source_hashes'].items():
    if not re.match(r'image_tex/ch\d+/',name):continue
    s=(ROOT/name).read_text(encoding='utf-8')
    if (WORK/'layout-offsets.json').exists():
        for note in json.loads((WORK/'layout-offsets.json').read_text(encoding='utf-8')):
            if note['path']==name:s=s.replace(note['after'],note['before'])
    s=s.replace(r',scale=\BookGeometryScale','').replace(r'[scale=\BookGeometryScale]','')
    s=s.replace('[book figure bounds]','[use as bounding box]')
    s=s.replace(',book panel tag','').replace('[book panel tag]','')
    s=s.replace(r'\begin{scope}[scale=\BookAxisInverseScale]'+'\n','')
    s=s.replace(r'\end{axis}'+'\n'+r'\end{scope}',r'\end{axis}')
    s=re.sub(r'\{(-?(?:\d+(?:\.\d*)?|\.\d+))(cm|mm)\*\\BookGeometryScale\}',lambda m:m[1]+m[2],s)
    candidates=[s.encode(),s.replace('\n','\r\n').encode()]
    # The two original migrated TikZ files contained CR-CR-LF line endings.
    candidates.append(s.replace('\n\n','PAIR').replace('\n','\r\n').replace('PAIR','\r\r\n').encode())
    if old not in [hashlib.sha256(x).hexdigest()for x in candidates]:changed.append(name)
    else:checked.append(name)
assert not changed,changed
for name,blocks in b['minted'].items():
    assert blocks==re.findall(r'\\begin\{minted\}.*?\\end\{minted\}',(ROOT/'chapter'/name).read_text(encoding='utf-8'),re.S),name
if 'inline13_before'in b:
    s=(ROOT/'chapter/13.tex').read_text(encoding='utf-8').replace(',scale=.75','')
    assert b['inline13_before']==re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',s,re.S)
before=(WORK/'chapter-1-before.tex').read_text(encoding='utf-8')
after=(ROOT/'chapter/1.tex').read_text(encoding='utf-8')
assert sorted(re.findall(r'\\BookFigure\[[^\]]*\]\{([^}]+)\}',before))==sorted(re.findall(r'\\BookFigure\[[^\]]*\]\{([^}]+)\}',after))
assert after.index('fig_1_02.tex')<after.index('表面由形式为')
result=dict(status='passed',native_sources_with_identical_geometric_data=len(checked),minted_blocks_unchanged=sum(len(x)for x in b['minted'].values()),figure_1_2_before_surface_introduction=True)
for n in [8,10]:
    p=WORK/f'chapter-{n}-before-break.tex'
    if p.exists():assert (ROOT/f'chapter/{n}.tex').read_text(encoding='utf-8')==p.read_text(encoding='utf-8').replace(r'\clearpage','',1)
result['redundant_opening_breaks_removed']=[n for n in [8,10]if (WORK/f'chapter-{n}-before-break.tex').exists()]
(WORK/'source-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
