"""Keep7.8 with its trigonometric parametrization before hyperbolic functions."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_08.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.8\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='双曲线使用双曲函数';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{16cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.8. 椭圆的最大面积参数化（式7.15）。\\\\\n'
       r'与图7.5取相同的 $a=4,b=2$ 和坐标比例；加号对应等角度参数 $u=i\pi/40$（$i=1,\ldots,19$），圆圈为 $u=0,\pi/2$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.8 after7.15, maintaining common scale with7.5.')
