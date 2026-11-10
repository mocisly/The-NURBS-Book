"""Place9.40 next to9.38/39 and the weighted/constrained fitting definitions."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_48.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.40\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{最小二乘曲面逼近}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.40. 相同二十一个数据点的受约束三次拟合，方框点$\mathbf Q_0,\mathbf Q_7,\mathbf Q_{13},\mathbf Q_{20}$及其一阶导数均作为精确约束。'+'\\\\\n'+
       r'取$\mathbf D_0=\mathbf D_{20}=(0,14)$、$\mathbf D_7=\mathbf D_{13}=(10,-10)$；所有箭头统一按真实导数的$1/10$绘制。'+'\\\\\n'+
       r'其余点的权重均为$1$；十八阶 KKT 方程组同时满足四个位置、四个导数约束，并最小化其余数据的平方误差。虚线为实际控制多边形。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.40 to constrained curve fitting examples after9.39;all8hard constraints and arrow scale documented.')
