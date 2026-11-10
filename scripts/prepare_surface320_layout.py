"""Bring both Fig3.20 pieces together and restore the interrupted continuity paragraph."""
from pathlib import Path
import json,re

root=Path(__file__).resolve().parents[1];data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
a=next(e for e in data['images'] if e['tex']=='image_tex/ch03/fig_3_21.tex')
b=next(e for e in data['images'] if e['tex']=='image_tex/ch03/fig_3_22.tex')
assert a['applied'] and not b.get('applied')
p=root/'chapter/3.tex';text=p.read_text(encoding='utf-8')
for ref in (a['replacement'],b['original']):
    start=text.index('\\begin{center}\n'+ref)
    caption=re.search(r'(?m)^图\s*3\.20[.。].*$',text[start:]);assert caption
    text=text[:start]+text[start+caption.end():]
caption=r'图 3.20. 按代表性控制点构造的B样条曲面：(a) \(5\times4\) 控制网；(b) 对应的双三次曲面。\\ \(p=q=3,\quad U=\{0,0,0,0,1/2,1,1,1,1\}\)，\\ \(V=\{0,0,0,0,1,1,1,1\}\)。'
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+a['replacement']+
    '\n\\par\\medskip\n'+b['original']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n')
anchor='张量积基函数的性质源于';assert text.count(anchor)==1;text=text.replace(anchor,block+anchor,1)
text,n=re.subn(r'节点的重数。在\s+在图',r'节点的重数。在图',text);assert n==1
assert text.count(a['replacement'])==text.count(b['original'])==1
p.write_text(text,encoding='utf-8')
print('Grouped native3.20(a) with pending original(b); representative data stated and continuity sentence restored.')
