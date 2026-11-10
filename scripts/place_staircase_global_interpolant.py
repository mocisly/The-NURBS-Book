"""Complete9.44..47comparison before precision-driven approximation theory."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_56.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.47\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='也可以交换两个方向的拟合顺序';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{22cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.47. 同一数据集的$(2,3)$次全局插值面，使用弦长公共参数与平均节点。'+'\\\\\n'+
       r'全部八十一个数据点均被精确插值；视角、坐标尺度、线宽和字号与图 9.45、9.46 的拟合面一致。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
s=s.replace('426 曲线和曲面拟合 我们将方程(9.78)','我们将方程(9.78)',1)
f.write_text(s,encoding='utf-8')
print('Placed9.47withall81exact interpolation points beside9.44..46comparison;removed misplaced scan and OCR426page header.')
