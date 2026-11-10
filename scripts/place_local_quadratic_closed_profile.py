"""Place9.25 with the polynomial examples and reconnect the cubic speed condition."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_31.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.25\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{局部有理二次曲线插值}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{30cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.25. 二十一个代表性鞋底数据点的闭合分段抛物线插值；空心圆为数据点。'+'\\\\\n'+
       r'用周期延拓的弦向量计算 Akima 切向，再按公式 (9.34)—(9.44) 构造二次曲线段；每个数据点均被插值，首尾位置与切向精确满足$G^1$闭合条件。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.25 after9.24;removed scan interrupting Eq9.46 speed explanation.')
