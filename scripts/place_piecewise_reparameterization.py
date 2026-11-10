"""Keep all four6.11 panels together immediately after their scalar spline data."""
import re
import image_tex as p
d=p.load();es=[next(e for e in d['images'] if e['tex']=='image_tex/ch06/'+name) for name in ('fig_6_11.tex','fig_6_12.tex')]
assert all(e['applied'] for e in es)
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8')
for e in es:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.11\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
s,n=re.subn(r'(?m)^\(a\) \\\(.+?\(b\).+\n','',s,count=1);assert n==1
anchor='现在我们转向使用有理(或分段有理)函数进行重新参数化。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{28cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+es[0]['replacement']+
       '\n\\par\\vspace{.8\\baselineskip}\n'+es[1]['replacement']+
       '\n\\par\\smallskip\n图 6.11. 用四组给定标量 B 样条函数重参数化同一条代表性三次曲线。\\\\\n'
       '虚线为原控制多边形，实线为新控制多边形和未改变的曲线，圆圈为新控制点。\\\\\n'
       '(a)～(c)为二次映射，(d)为线性映射；各组给定节点见正文，(c)保留给定的重节点表示。\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert all(s.count(e['replacement'])==1 for e in es)
f.write_text(s,encoding='utf-8');print('Grouped6.11 in a two-by-two layout before rational reparameterization; removed split continuation captions.')
