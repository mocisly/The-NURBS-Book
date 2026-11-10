"""Place9.44 next to the four-surface comparison, before internal constraints."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_52.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.44\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='当然，可以先拟合';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{25cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.44. 曲面逼近的代表性阶梯数据，$9\times9$网格包含八十一个不同的点。'+'\\\\\n'+
       r'取$X_i=Y_i=-2+i/2$，$z_{i,j}=H_i+H_j+B_iB_j/10$，$i,j=0,\ldots,8$；'+'\\\\\n'+
       r'$H=(1,1,1,1/2,1/2,1/2,0,0,0)$，$B=(0,0,0,1,1,1,0,0,0)$。'+'\\\\\n'+
       r'实心点与邻接虚线直接由这些坐标构造；后续图 9.45—9.47 统一使用同一数据集。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.44 after surface-fit overview and before internal constraint paragraph;shared81point formula documented.')
