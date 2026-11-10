"""Place the ellipse sampling plot before the hyperbola parametrization."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_05.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.5\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='这些方程\n\n\\[';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{16cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.5. 椭圆弧的有理参数化（式7.8）。\\\\\n'
       r'示例取 $a=4,b=2$；加号为 $u=i/20$（$i=1,\ldots,19$）处的点，圆圈为参数端点 $u=0,1$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.5 after elliptic endpoint discussion and before hyperbolic equations.')
