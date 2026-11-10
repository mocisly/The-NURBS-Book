"""Keep9.24's paired corner-flag examples with the local polynomial discussion."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_30.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.24\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{局部有理二次曲线插值}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{23cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.24. 同一组十个代表性数据点的 Akima 局部二次插值，仅改变拐角标志。'+'\\\\\n'+
       r'(a) 不保留拐角，各二次段均$G^1$连接；(b) 保留拐角，$(2,0)$、$(6,0)$处的水平与竖直数据段精确相交，其余连接仍为$G^1$。'+'\\\\\n'+
       r'两图使用相同的坐标尺度；空心圆为数据点，顶部的两段抛物线在同一切向下平滑连接。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.24 after9.23, before local rational interpolation.')
