"""Apply reviewed physical scales and the corrected figure 1.2 placement."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];BUILD=ROOT/'tmp/figure-layout'
def prepare_sources():
    p=ROOT/'chapter/1.tex';s=p.read_text(encoding='utf-8')
    pat=r'\\begin\{figure\}\[ht\]\s*\\centering\s*\\BookFigure\[\]\{ch01/fig_1_02.tex\}.*?\\end\{figure\}'
    m=re.search(pat,s,re.S)
    if m:
        block=m[0].replace(r'\begin{figure}[ht]',r'\begin{center}\begin{minipage}{12cm}').replace(r'\caption{',r'\captionof{figure}{').replace(r'\end{figure}',r'\end{minipage}\end{center}')
        s=s[:m.start()]+s[m.end():]
        anchor='表面由形式为'
        i=s.index(anchor);s=s[:i]+block+'\n\n'+s[i:];p.write_text(s,encoding='utf-8')
    p=ROOT/'main.tex';s=p.read_text(encoding='utf-8')
    anchor=r'\input{\subfix{image_tex/common.tex}}'
    if 'image_tex/figure-layout.tex'not in s:s=s.replace(anchor,anchor+'\n'+r'\input{\subfix{image_tex/figure-layout.tex}}');p.write_text(s,encoding='utf-8')
    for p in (ROOT/'image_tex').glob('ch*/*.tex'):
        s=p.read_text(encoding='utf-8')
        if r'\begin{axis}'not in s or 'BookAxisInverseScale'in s:continue
        def axis(m):
            options=m[1]
            options=re.sub(r'\b(width|height)=(\d+(?:\.\d+)?)(cm|mm)',lambda n:f'{n[1]}={{{n[2]}{n[3]}*\\BookGeometryScale}}',options)
            options=re.sub(r'at=\{\(([^)]*)\)\}',lambda n:'at={('+re.sub(r'(-?\d+(?:\.\d+)?)(cm|mm)',lambda q:'{'+q[1]+q[2]+r'*\BookGeometryScale}',n[1])+')}',options)
            return r'\begin{scope}[scale=\BookAxisInverseScale]'+'\n'+r'\begin{axis}['+options+']'
        s=re.sub(r'\\begin\{axis\}\[([^\]]+)\]',axis,s)
        s=s.replace(r'\end{axis}',r'\end{axis}'+'\n'+r'\end{scope}')
        p.write_text(s,encoding='utf-8')
    print('Prepared figure 1.2 placement and font-preserving axis sizing.')

def picture_scales():
    for p in (ROOT/'image_tex').glob('ch*/*.tex'):
        s=p.read_text(encoding='utf-8')
        s=s.replace(r',scale=\BookGeometryScale','').replace(r'[scale=\BookGeometryScale]','')
        starts=list(re.finditer(r'\\begin\{tikzpicture\}',s))
        for m in reversed(starts):
            i=m.end()
            while i<len(s)and s[i].isspace():i+=1
            if s[i:i+1]=='[':
                j=i+1;depth=0
                while j<len(s):
                    if s[j]=='{':depth+=1
                    elif s[j]=='}':depth-=1
                    elif s[j]==']'and depth==0:break
                    j+=1
                assert j<len(s),p
                s=s[:j]+r',scale=\BookGeometryScale'+s[j:]
            else:s=s[:m.end()]+r'[scale=\BookGeometryScale]'+s[m.end():]
        p.write_text(s,encoding='utf-8')
    print('Added geometric scale to explicit native picture roots only.')

def scales():
    merged={r['path']:r for r in json.loads((BUILD/'revision.json').read_text(encoding='utf-8'))}
    for name in ['touchups','spacing','spacing2','labels','final-refinements','final-label']:
        p=BUILD/f'{name}.json'
        if p.exists():
            for r in json.loads(p.read_text(encoding='utf-8')):merged[r['path']]=r
    records=list(merged.values())
    (BUILD/'final-sizes.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    text='% Per-figure geometry factors, verified against 11pt body text.\n'
    for r in records:text+=f"\\expandafter\\def\\csname BookFigureScale@{r['path']}\\endcsname{{{r['scale']}}}\n"
    (ROOT/'image_tex/figure-scales.tex').write_text(text,encoding='utf-8')
    print(f'Applied {len(records)} individual geometry factors.')

def captions():
    pat=r'\\begin\{center\}\s*(\\BookFigure\[[^\]]*\]\{([^}]+)\})\s*\\end\{center\}\s*(?:\\hspace\*\{3em\}\s*)?(图\s*\d+\.\d+\.[^\n]+)'
    changes=[]
    for p in (ROOT/'chapter').glob('*.tex'):
        s=p.read_text(encoding='utf-8')
        def block(m):
            width='10cm'if m[2]in ['ch01/fig_1_03.tex','ch01/fig_1_04.tex']else'14cm'
            changes.append(dict(chapter=p.name,figure=m[2],caption=m[3]))
            return r'\begin{center}'+'\n'+r'\begin{minipage}{'+width+'}\n'+r'\centering'+'\n'+m[1]+'\n'+r'\captionsetup{font=small,justification=centering,singlelinecheck=false,skip=6pt}'+'\n'+r'\captionof*{figure}{'+m[3]+'}\n'+r'\end{minipage}'+'\n'+r'\end{center}'
        s=re.sub(pat,block,s)
        if changes and s!=p.read_text(encoding='utf-8'):p.write_text(s,encoding='utf-8')
    p=ROOT/'chapter/1.tex';s=p.read_text(encoding='utf-8')
    m=re.search(r'\\begin\{center\}\s*\\begin\{minipage\}\{10cm\}\s*\\centering\s*\\BookFigure\[[^\]]*\]\{ch01/fig_1_04.tex\}.*?\\end\{center\}',s,re.S)
    if m:
        block=m[0];s=s[:m.start()]+s[m.end():];i=s.index('在某一点存在法向量');s=s[:i]+block+'\n\n'+s[i:];p.write_text(s,encoding='utf-8')
    (BUILD/'caption-placements.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Kept {len(changes)} early captions with their diagrams; moved figure 1.4 next to (1.4).')

if __name__=='__main__':
    import sys
    if sys.argv[1]=='prepare':prepare_sources()
    elif sys.argv[1]=='picture-scales':picture_scales()
    elif sys.argv[1]=='scales':scales()
    elif sys.argv[1]=='captions':captions()
