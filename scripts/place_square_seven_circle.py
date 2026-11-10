"""Keep the seven-point square circle with the data and continuity in Ex7.6."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_24.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.21\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='算法 A7.1 在三维空间中构建';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{32cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.21. 基于七点方形的 NURBS 圆，由图7.20的两个半圆拼接而成，使用 Ex7.6 的节点和权重。\\\\\n'+
       r'(a) 控制多边形与等参数步长采样点 $u=i/80$；(b) 对应的七个有理基函数。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed7.21 after Ex7.6 data and continuity, before MakeNurbsCircle discussion.')
