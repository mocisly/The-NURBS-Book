"""Place6.5 after the complete affine-projection formula."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_05.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.5\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='图 6.6 显示了透视投影。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{19cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n图 6.5. 代表性三次 NURBS 曲线沿 $\\mathbf W$ 平行投影到由 $\\mathbf Q$、$\\mathbf N$ 确定的平面。\\\\\n'
       '实线为原曲线及其控制多边形，虚线为投影结果；节点和权重均保持不变。\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(ref)==1;f.write_text(s,encoding='utf-8')
print('Grouped6.5 after affine projection formulas6.14/6.15.')
