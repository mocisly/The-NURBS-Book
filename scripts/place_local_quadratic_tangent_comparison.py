"""Move9.23 out of the rational-weight list to its local quadratic discussion."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_29.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.23\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{局部有理二次曲线插值}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.23. 同一组七个代表性数据点的局部二次插值；(a) 贝塞尔三点切向估计，(b) Akima 五点切向估计。'+'\\\\\n'+
       r'两图使用相同数据$(0,0),(1,0),(5/2,0),(4,2),(11/2,0),(7,0),(8,0)$；曲线按公式 (9.34)—(9.44) 构造，空心圆为数据点。'+'\\\\\n'+
       r'(b) 两侧共线数据段被精确再现；(a) 相邻上升、下降弦会改变共线段端部的切向，产生轻微下凹。所有二次段在连接处均满足$G^1$连续。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.23 after local quadratic examples and before rational interpolation;rejoined rational-weight enumeration.')
