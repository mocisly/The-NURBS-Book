"""Place9.42 alongside the previous point/derivative constraint cases."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_50.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.42\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{最小二乘曲面逼近}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.42. 与图 9.40 使用相同的数据、节点、位置约束和端导数，仅将两个内部导数改为$\mathbf D_7=\mathbf D_{13}=(14,0)$。'+'\\\\\n'+
       r'所有未约束点的权重恢复为$1$；四个方框点及其导数仍被精确满足，内部两处切向现为水平方向。'+'\\\\\n'+
       r'箭头统一按导数的$1/10$绘制；曲线、控制多边形和数据标记的坐标尺度与前图一致。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.42 to curve-fitting comparisons;documented final horizontal internal derivatives14,0 and unit weights.')
