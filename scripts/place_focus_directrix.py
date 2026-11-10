"""Place the geometric definition after7.2 without splitting its sentence."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_01.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.1\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
s=s.replace('其中 \\(e\\) 是一个称为离心率的比例常数。离心率\n','其中 \\(e\\) 是一个称为离心率的比例常数。离心率',1)
s=s.replace('离心率\n\n\n','离心率',1)
anchor='即，位于 \\({xy}\\) 平面的圆锥曲线由一个二次代数方程表示。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{14cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.1. 通过焦点和准线定义圆锥曲线。\\\\\n'
       r'图示取 $e=1$ 的抛物线：准线为 $x=0$，与 $y$ 轴重合；$\mathbf{PD}$ 垂直于准线，且 $|\mathbf{PF}|=|\mathbf{PD}|$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.1 after7.2, keeping eccentricity classification sentence together.')
