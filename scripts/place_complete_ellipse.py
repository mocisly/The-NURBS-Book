"""Return7.28 to the end of the ellipse reconstruction, before higher-order circles."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_36.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.28\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\section{高阶圆}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{23cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 7.28. 从给定 Bézier 椭圆弧（实线）恢复完整椭圆的九点 NURBS 表示（虚线）。'+'\\\\\n'+
       r'$\mathbf P_i$ 为给定弧的控制点，$\mathbf Q_i$ 为恢复出的矩形控制多边形；给定控制三角形用细虚线表示。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed7.28 after complete-ellipse reconstruction and before higher-order circles.')
