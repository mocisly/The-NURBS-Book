"""Restore both Fig3.16 pieces beside Ex3.2; preserve the pending original(b)."""
from pathlib import Path
import json,re

root=Path(__file__).resolve().parents[1]
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
ea=next(e for e in data['images'] if e['tex']=='image_tex/ch03/fig_3_16.tex')
eb=next(e for e in data['images'] if e['tex']=='image_tex/ch03/fig_3_17.tex')
assert ea['applied'] and not eb.get('applied')
p=root/'chapter/3.tex';text=p.read_text(encoding='utf-8')
def remove(t,ref):
    start=t.index('\\begin{center}\n'+ref)
    cap=re.search(r'(?m)^图\s*3\.16[.。].*$',t[start:]);assert cap
    assert t[start:start+cap.start()].count(ref)==1
    return t[:start]+t[start+cap.end():]
text=remove(text,ea['replacement']);text=remove(text,eb['original'])
caption=r"图 3.16. (a) \(U=\{0,0,0,0,2/5,3/5,3/5,1,1,1,1\}\) 上的三次曲线及切向量。\\ (b) \(U'=\{0,0,0,2/5,3/5,3/5,1,1,1\}\) 上的二次曲线 \(\mathbf C'(u)\)；两图的导数量按 \(1/3\) 缩放显示。"
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+
       ea['replacement']+'\n\\par\\medskip\n'+eb['original']+'\n\\par\\smallskip\n'+
       caption+'\n\\end{minipage}\n\\end{center}\n\n')
anchor='Ex3.3 回想一下';assert text.count(anchor)==1;text=text.replace(anchor,block+anchor,1)
a,b=text.index('Ex3.2 设'),text.index(anchor);part=text[a:b];lines=part.splitlines()
denoms=(r'\frac25-0',r'\frac35-0',r'\frac35-0',r'1-\frac25',r'1-\frac35',r'1-\frac35')
mults=(r'\frac{15}{2}','5','5','5',r'\frac{15}{2}',r'\frac{15}{2}')
for i,(denom,mult) in enumerate(zip(denoms,mults)):
    found=[j for j,line in enumerate(lines) if line.startswith(r'{\mathbf{Q}}_{'+str(i)+'}')];assert len(found)==1
    diff=r'\left(\mathbf P_{'+str(i+1)+r'}-\mathbf P_{'+str(i)+r'}\right)'
    lines[found[0]]=r'\mathbf Q_{'+str(i)+r'}=\frac{3'+diff+'}{'+denom+'}='+mult+diff
text=text[:a]+'\n'.join(lines)+'\n\n'+text[b:]
assert text.count(ea['replacement'])==text.count(eb['original'])==1
assert r'\includegraphics' not in text[text.index(ea['replacement']):text.index(eb['original'])]
p.write_text(text,encoding='utf-8')
print('Grouped native3.16(a) and pending original(b) afterEx3.2; six Eq3.4 coefficients reconciled.')
