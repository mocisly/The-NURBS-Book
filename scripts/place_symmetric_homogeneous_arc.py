"""Put6.12 at the circular-arc example, outside the next mapping derivation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_13.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.12\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='在实践中，通常不需要使用高于一阶的有理重新参数化函数。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{22cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n图 6.12. 权重为 $\\{1,\\sqrt2/2,1\\}$ 的圆弧及其齐次表示。\\\\\n'
       '虚线为齐次多项式曲线和控制多边形，实线为它们在 $W=1$ 平面上的中心投影；点线连接同一参数处的对应点。\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(ref)==1
f.write_text(s,encoding='utf-8');print('Placed6.12 immediately after Ex6.7/6.55, before the next rational mapping formulas; caption correctly says homogeneous.')
