"""Place7.9 after its hyperbolic parametrization with an explicit comparison."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_09.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.9\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='参数化抛物线由方程给出(图 7.7)';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{16cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.9. 双曲线的最大面积参数化（式7.16）。\\\\\n'
       r'与图7.6取相同的 $a=b=1$、端点及坐标比例；加号对应 $u=i\ln9/20$（$i=1,\ldots,19$），圆圈为 $u=0,\ln9$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.9 by7.16 with same geometric window as7.6.')
