"""Group the two reviewed Fig5.3 panels after their length-ratio explanation."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_0{n}.tex') for n in (3,4)]
assert all(e.get('applied') for e in entries)
p=root/'chapter/5.tex';text=p.read_text(encoding='utf-8');intervals=[]
for e in entries:
    ref=e['replacement'];assert text.count(ref)==1
    start=text.index('\\begin{center}\n'+ref)
    cap=re.search(r'(?m)^图\s*5\.3[.。].*$',text[start:]);assert cap
    intervals.append((start,start+cap.end()))
for start,end in sorted(intervals,reverse=True):text=text[:start]+text[end:]
caption=(r'图 5.3. 控制多边形边按节点跨度的划分。\\ '
         r'(a) 代表性控制多边形与节点向量 \(\{0,0,0,0,1,2,3,4,4,5,6,7,7,7,7\}\)，小圆为不同的内部划分点；零跨度对应零长度子段。\\ '
         r'(b) 放大的 \(L_3=\mathbf P_2\mathbf P_3\)，由 \([u_3,u_6]=[0,3]\) 分成三段，\(\lambda_3^j=1/3\)、\(d_3^j=d_3/3\)。')
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\medskip\n'+entries[1]['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n')
anchor='现在图 5.3a 和 5.3b 以及公式';assert text.count(anchor)==1
text=text.replace(anchor,block+anchor,1)
assert all(text.count(e['replacement'])==1 for e in entries)
p.write_text(text,encoding='utf-8')
print('Grouped native5.3(a,b) after the normalized-leg-length explanation.')
