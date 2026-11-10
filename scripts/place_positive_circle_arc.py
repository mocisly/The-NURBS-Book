"""Return7.19 to Ex7.4 and repair its verified smoothness sentence."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_22.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.19\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='Ex7.5 使用四个控制点的半圆';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.19. 图7.18的圆弧在$u=1/2$处插入一次节点后，权重变为$\\{1,1/4,1/4,1\\}$。\\\\\n'
       r'(a) 新控制多边形与采样点；圆弧、参数及坐标比例与图7.18相同；(b) 对应的四个非负有理基函数。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
wrong=r'\({\mathbf{C}}^{w}\left( u\right)\) 和 \(\mathbf{C}\left( u\right)\) 在 \({C}^{2}\) 上是 \(u \in  \left\lbrack  {0,1}\right\rbrack\) 连续的；插入节点并没有改变这一点。'
right=r'\(\mathbf C^w(u)\) 和 \(\mathbf C(u)\) 在整个区间 \(u\in[0,1]\) 上均保持 \(C^2\) 连续；节点插入未改变曲线的几何形状或参数化。'
assert s.count(wrong)==1;s=s.replace(wrong,right,1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.19 at end ofEx7.4 beforeEx7.5; restored verifiedC2smoothness wording.')
