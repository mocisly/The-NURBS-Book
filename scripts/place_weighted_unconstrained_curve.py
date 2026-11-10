"""Keep9.39 next to9.38 and reconnect the surface approximation introduction."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_47.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.39\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
assert s.count('420 曲线和曲面拟合')==1;s=s.replace('420 曲线和曲面拟合','',1)
s,n=re.subn('我们的最小二乘曲线方案。\\s+非常简单','我们的最小二乘曲线方案。该方案非常简单',s,count=1);assert n==1
anchor=r'\subsection{最小二乘曲面逼近}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.39. 与图 9.38 使用相同的数据、参数、节点和十个控制点，仅将$w_4^q,\ldots,w_7^q$由$1$改为$100$。'+'\\\\\n'+
       r'四个被加权点的同参数平方误差和从约$0.09771$减至$0.002868$，曲线被明显拉向顶部数据；这些数据仍是加权逼近项。'+'\\\\\n'+
       r'两端保持无约束，端参数处的距离分别约为$0.03516$、$0.01865$，均不为零；实线、虚线及空心圆的含义与图 9.38 相同。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.39 after9.38;removed OCR420header and rejoined surface approximation explanation.')
