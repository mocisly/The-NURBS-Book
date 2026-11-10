"""Keep Fig5.20 and5.21 by their shared surface decomposition explanation."""
import argparse,re
from pathlib import Path
import image_tex as pipeline
p=argparse.ArgumentParser(description=__doc__);p.add_argument('figure',choices=['5.20','5.21']);a=p.parse_args()
data=pipeline.load();numbers=[24] if a.figure=='5.20' else [25,26]
entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in numbers]
assert all(e['applied'] for e in entries)
path=pipeline.ROOT/'chapter/5.tex';text=path.read_text(encoding='utf-8')
for e in entries:
    ref=e['replacement'];assert text.count(ref)==1
    pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*'+re.escape(a.figure)+r'\.[^\n]*'
    text,count=re.subn(pattern,'',text,count=1);assert count==1,e['tex']
if a.figure=='5.20':
    drawing=entries[0]['replacement']
    caption=(r'图 5.20. 要分解的三次$\times$二次曲面，(a)代表性$5\times4$控制网；(b)同一曲面的等参数线。'
             '\\\\\n'+r'节点向量为$U=\{0,0,0,0,3/5,1,1,1,1\}$、$V=\{0,0,0,2/5,1,1,1\}$，各权重为1。图5.21沿用同一曲面。')
else:
    drawing=('\\begin{minipage}[b]{13cm}\n'+entries[0]['replacement']+'\n\\end{minipage}\\hfill\n'
             '\\begin{minipage}[b]{13cm}\n'+entries[1]['replacement']+'\n\\end{minipage}')
    caption=(r'图 5.21. 将图5.20在$u=3/5$、$v=2/5$处分解为四块三次$\times$二次Bézier曲面。'
             '\n'+r'(a)各块$4\times3$控制网；(b)对应的曲面片。内部节点分别细化到三重、二重，曲面形状与参数化保持不变。'
             '\n'+r'各块仅作显示平移，以便观察分界；平移前相邻边界完全一致。')
    assert text.count('172 基本几何算法')==1
    text=text.replace('172 基本几何算法','')
block=('\\begin{center}\n\\begin{minipage}{28cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+drawing+
       '\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n')
anchor='现在我们给出一个算法';assert text.count(anchor)==1
text=text.replace(anchor,block+anchor,1)
for e in entries:assert text.count(e['replacement'])==1
path.write_text(text,encoding='utf-8');print('Placed '+a.figure+' after surface decomposition introduction, before curve extraction algorithm.')
