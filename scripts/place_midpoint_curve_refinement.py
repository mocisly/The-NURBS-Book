"""Group Fig5.16's three views and reconnect the interrupted A5.4 header."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1];data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in (18,19)];assert all(e['applied'] for e in entries)
p=root/'chapter/5.tex';s=p.read_text(encoding='utf-8');intervals=[]
for e in entries:
    ref=e['replacement'];assert s.count(ref)==1;start=s.index('\\begin{center}\n'+ref);cap=re.search(r'(?m)^图\s*5\.16[.。].*$',s[start:]);assert cap;intervals.append((start,start+cap.end()))
for start,end in sorted(intervals,reverse=True):s=s[:start]+s[end:]
assert s.count('164 基本几何算法')==1;s=s.replace('164 基本几何算法','')
start=s.index('\n\\HRule\n',s.index('/* Input: n, p, U, Pw, X, r */'));end=s.index('\\hspace*{3em} /* Output: Ubar, Qw */',start);old=s[start:end]
assert old.count('\\HRule')==2 and not old.replace('\\HRule','').strip();s=s[:start]+'\n\n'+s[end:]
caption=(r'图 5.16. 三次曲线的中点节点细化，各图坐标尺度相同。\\ '
         r'(a) 定义在 \(\{0,0,0,0,3/10,7/10,1,1,1,1\}\) 上的代表性六点控制网；(b) 第一次细化，9个控制点；(c) 第二次细化，15个控制点。\\ '
         r'箭头标出相对于(a)新增的节点。曲线及其参数化始终不变，控制多边形逐步靠近曲线。')
panels='\\begin{minipage}[b]{22.6cm}\n\\centering\n'+entries[0]['replacement']+'\n\\end{minipage}\\hfill\n\\begin{minipage}[b]{10.6cm}\n\\centering\n'+entries[1]['replacement']+'\n\\end{minipage}'
block='\\begin{center}\n\\begin{minipage}{34.2cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+panels+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n'
anchor='我们不需要额外的数学知识来开发结点细化算法';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
assert all(s.count(e['replacement'])==1 for e in entries);p.write_text(s,encoding='utf-8')
print('Grouped5.16(a,b,c) by midpoint-refinement explanation; restored7/10 omitted in OCR and joined A5.4 Input/Output.')
