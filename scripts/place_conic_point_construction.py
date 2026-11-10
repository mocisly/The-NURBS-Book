"""Place 7.23 before its perspective construction and equations7.37-7.39."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_28.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.23。[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\({\mathbf{P}}_{1}\) (图 7.23)可以通过交叉线';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{19cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 7.23. 由端点 $\mathbf P_0,\mathbf P_2$、端切线 $\mathbf T_0,\mathbf T_2$ 和曲线上点 $\mathbf P$ 确定的一般圆锥弧。'+'\\\\\n'+
       r'$\mathbf P_1$ 为端切线的交点，$\mathbf Q$ 为直线 $\mathbf P_1\mathbf P$ 与弦的交点；两段弦长之比为 $u^2:(1-u)^2$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed7.23 before central projection argument and equations7.37-7.39.')
