"""Finish9.38..43curve comparisons before least-squares surface approximation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_51.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.43\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{最小二乘曲面逼近}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.43. 沿用图 9.42 的全部精确约束，仅将$w_4^q$、$w_{16}^q$分别改为$50$、$20$。'+'\\\\\n'+
       r'这两点的同参数平方误差分别由约$0.3155,0.1345$降至$0.006941,0.005468$；四个位置及四个导数约束仍被精确满足。'+'\\\\\n'+
       r'权重以细引线标注；水平内部导数、端导数及箭头的$1/10$比例均与图 9.42 相同，其余数据权重为$1$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.43 after9.42;rejoined A9.7surface fitting and Tempcontrol-array explanation.')
