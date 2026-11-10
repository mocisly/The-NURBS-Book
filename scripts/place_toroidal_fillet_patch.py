"""Place8.13 with revolution/fillet explanation,before nonuniform scaling."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_17.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.13\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\section{曲面的非均匀缩放}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.13. 用于圆角过渡的环面片，表示次数为$2\times2$；细虚线为实际的$3\times3$控制网。'+'\\\\\n'+
       r'本例大半径为2、管半径为$3/5$，管截圆中心高度为$6/5$；绕$z$轴截取90度，截圆取180度至270度的四分之一圆弧。'+'\\\\\n'+
       r'截线在内侧边界与圆柱相切，在下侧边界与水平面相切；实线为边界，细线为等参数线，采用透明线框。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.13 before scaling section,beside fillet explanation.')
