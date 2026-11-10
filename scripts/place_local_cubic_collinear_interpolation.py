"""Keep9.31 adjacent to9.30 and its local cubic explanation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_37.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.31\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{局部双三次曲面插值}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.31. 与图 9.7 完全相同的十三个数据点，改用 Akima 切向与公式 (9.47)、(9.50)—(9.54) 的局部三次插值。'+'\\\\\n'+
       r'左侧与中间的竖直共线段、右侧的水平共线段均由直线三次段精确表示；全部数据点被插值，内部连接满足$C^1$连续。图形采用与图 9.7 相同的坐标尺度。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.31 from bicubic surface introduction to end of local cubic comparison.')
