"""Join the two reviewed Fig4.11 panels with one correct complete caption."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch04/fig_4_{n}.tex') for n in (12,13)]
assert all(e.get('applied') for e in entries)
p=root/'chapter/4.tex';text=p.read_text(encoding='utf-8');intervals=[]
for e in entries:
    ref=e['replacement'];assert text.count(ref)==1
    start=text.index('\\begin{center}\n'+ref)
    cap=re.search(r'(?m)^图\s*4\.11[.。].*$',text[start:]);assert cap
    intervals.append((start,start+cap.end()))
for start,end in sorted(intervals,reverse=True):text=text[:start]+text[end:]
caption=(r'图 4.11. 三次 \(\times\) 二次NURBS示意曲面，节点向量同图4.10。\\ '
         r'(a) \(w_{4,2}=2/5\)；(b) \(w_{4,2}=6\)。其他权重均为1。\\ '
         r'两图共用代表性 \(7\times8\) 控制网，整体上移显示以便观察；圈出的是 \(\mathbf P_{4,2}\)。')
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\medskip\n'+entries[1]['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n')
anchor='使用齐次坐标表示 NURBS 曲面是方便的';assert text.count(anchor)==1
text=text.replace(anchor,block+anchor,1)
assert all(text.count(e['replacement'])==1 for e in entries)
p.write_text(text,encoding='utf-8')
print('Grouped native4.11(a,b) before the homogeneous-surface introduction; restored the interrupted Ex4.3 calculation.')
