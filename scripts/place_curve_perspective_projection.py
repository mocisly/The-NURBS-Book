"""Place6.6 after both projected-control and projected-weight derivations."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_06.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.6\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='图 6.7 显示了 NURBS 曲面的平行投影。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{20cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n图 6.6. 代表性闭合三次 NURBS 曲线从视点 $\\mathbf E$ 透视投影到平面。\\\\\n'
       '实线为原曲线及控制多边形，虚线为投影结果；点线射线汇聚于视点，投影控制点和新权重由式(6.17)、(6.18)同时确定。\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(ref)==1;f.write_text(s,encoding='utf-8')
print('Grouped6.6 after projected controls and weights6.17-6.21.')
