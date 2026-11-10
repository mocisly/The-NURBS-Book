"""Pair7.16's actual circle sampling and matching rational bases at Ex7.2."""
import re
import image_tex as p
d=p.load();ee=[next(e for e in d['images'] if e['tex']==f'image_tex/ch07/fig_7_{i}.tex') for i in (16,17)]
assert all(e['applied'] for e in ee)
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
for e in ee:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.16\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='为了指示参数化，圆上的点被标记';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{30cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'
       '\\begin{minipage}{14cm}\\centering\n'+ee[0]['replacement']+
       '\n\\end{minipage}\\hfill\n\\begin{minipage}{14cm}\\centering\n'+ee[1]['replacement']+
       '\n\\end{minipage}\n\\par\\smallskip\n'
       r'图 7.16. 基于九点方形的 NURBS 圆，两图使用 Ex7.2 给出的同一组节点、控制点和权重。'+'\\\\\n'
       r'(a) 控制多边形与等参数步长采样点 $u=i/80$，四个节点处的采样点与控制点圆圈重合；(b) 对应的九个有理基函数 $R_{i,2}$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
for e in ee:assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8');print('Paired7.16 native parameter/control diagram and matching rational bases before continuity discussion.')
