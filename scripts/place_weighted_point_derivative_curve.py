"""Place9.41 beside its constrained baseline, keeping A9.7surface prose together."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_49.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.41\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{最小二乘曲面逼近}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.41. 沿用图 9.40 的数据、节点、四个位置及四个导数约束，仅将$w_5^q,w_{15}^q$改为$100$。'+'\\\\\n'+
       r'这两个被加权点的同参数平方误差和由约$0.2780$减至$0.02482$；全部精确约束保持成立，其他点的权重仍为$1$。'+'\\\\\n'+
       r'权重标注以细引线指向对应数据点；方框、导数箭头与控制多边形的含义及尺度均与图 9.40 相同。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.41 after constrained baseline9.40;shared8hardconstraints and onlytwochanged weights documented.')
