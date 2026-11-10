"""Join the two reviewed Fig4.10 panels with one correct complete caption."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch04/fig_4_{n}.tex') for n in (10,11)]
assert all(e.get('applied') for e in entries)
p=root/'chapter/4.tex';text=p.read_text(encoding='utf-8');intervals=[]
for e in entries:
    ref=e['replacement'];assert text.count(ref)==1
    start=text.index('\\begin{center}\n'+ref)
    cap=re.search(r'(?m)^图\s*4\.10[.。].*$',text[start:]);assert cap
    intervals.append((start,start+cap.end()))
for start,end in sorted(intervals,reverse=True):text=text[:start]+text[end:]
caption=(r'图 4.10. \(R_{4,2}(u,v)=w_{4,2}f/[1+(w_{4,2}-1)f]\)，\(f=N_{4,3}(u)N_{2,2}(v)\)。\\ '
         r'\(U=(0,0,0,0,1/4,1/2,3/4,1,1,1,1)\)，\\ '
         r'\(V=(0,0,0,1/5,2/5,3/5,3/5,4/5,1,1,1)\)。\\ '
         r'(a) \(w_{4,2}=2/5\)；(b) \(w_{4,2}=6\)。其他权重均为1，两侧曲线为未加权基函数。')
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\medskip\n'+entries[1]['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n')
anchor='使用齐次坐标表示 NURBS 曲面是方便的';assert text.count(anchor)==1
text=text.replace(anchor,block+anchor,1)
assert all(text.count(e['replacement'])==1 for e in entries)
p.write_text(text,encoding='utf-8')
print('Grouped both native4.10 panels; single caption restores full clamped U/V and states the exact rational basis.')
