"""Place9.38 directly after weighted/constrained fitting examples, before surfaces."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_46.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.38[。\.][^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{最小二乘曲面逼近}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.38. 二十一个代表性数据点的无约束三次最小二乘拟合，所有数据权重均为$1$。'+'\\\\\n'+
       r'十个控制点全部作为未知数求解，采用弦长参数及公式 (9.68)、(9.69) 的节点；虚线为求得的控制多边形，空心圆为数据点。'+'\\\\\n'+
       r'两端没有插值约束；在对应端参数处，曲线与首、末数据点的距离分别约为$0.00327$和$0.01636$，均不为零。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.38 to curve fitting examples before least-squares surface subsection;explicit free endpoints and actual residuals.')
