"""Group5.17(a,b,c) by its explanation and reconnect A5.4's interrupted else branch."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1];data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in (20,21)];assert all(e['applied'] for e in entries)
p=root/'chapter/5.tex';s=p.read_text(encoding='utf-8');intervals=[]
for e in entries:
    ref=e['replacement'];assert s.count(ref)==1;start=s.index('\\begin{center}\n'+ref);cap=re.search(r'(?m)^图\s*5\.17[.。].*$',s[start:]);assert cap;intervals.append((start,start+cap.end()))
for start,end in sorted(intervals,reverse=True):s=s[:start]+s[end:]
start=s.index('\n\\HRule\n',s.index('\\hspace*{5em} else',s.index('ALGORITHM A5.4')));end=s.index('\\hspace*{3em} \\{',start);old=s[start:end]
assert old.count('\\HRule')==2 and old.count('166 基本几何算法')==1 and not old.replace('\\HRule','').replace('166 基本几何算法','').strip();s=s[:start]+'\n\n'+s[end:]
caption=(r'图 5.17. 对图 5.9 的同一三次 \(\times\) 二次曲面进行中点节点细化，各图视角与尺度相同。\\ '
         r'(a) \(u\) 方向三轮，\(11\times4\) 控制点；(b) \(v\) 方向两轮，\(4\times10\) 控制点；(c) 两种细化组合，\(11\times10\) 控制点。\\ '
         r'细化使控制网逐步靠近曲面，曲面的几何形状和参数化保持不变。')
panels='\\begin{minipage}[b]{23.3cm}\n\\centering\n'+entries[0]['replacement']+'\n\\end{minipage}\\hfill\n\\begin{minipage}[b]{11.3cm}\n\\centering\n'+entries[1]['replacement']+'\n\\end{minipage}'
block='\\begin{center}\n\\begin{minipage}{35.6cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+panels+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n'
anchor='我们不需要额外的数学知识来开发结点细化算法';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
before=r'图 5.17a 到 5.17c 显示了对图 5.9 的表面进行的三次中点结点细化，分别在 \(u - ,v -\) 和两个方向上。'
after=r'图 5.17依次给出图5.9曲面在 \(u\) 方向三轮、\(v\) 方向两轮及两个方向组合的中点节点细化。'
assert s.count(before)==1;s=s.replace(before,after)
assert all(s.count(e['replacement'])==1 for e in entries);p.write_text(s,encoding='utf-8')
print('Grouped5.17(a,b,c) after5.16; clarified3u/2v rounds and joined A5.4 else branch.')
