"""Refresh early8.1's natural-width reference and place it in the bilinear section."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_01.tex');assert e['applied'] and e['compiled']==e['reviewed']==p.signature(e)
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8');old=e['replacement'];old_signature=p.signature(e)
pattern=r'\\begin\{center\}\s*'+re.escape(old)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.1\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
e['options']=r'max width=\linewidth';e['replacement']=r'\BookFigure[max width=\linewidth]{ch08/fig_8_01.tex}';assert p.signature(e)==old_signature
anchor=r'\section{一般圆柱体}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{30cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.1. 式 (8.1) 的双线性曲面；两个参数方向的等参数线均为直线，两图采用相同投影和比例。'+'\\\\\n'+
       r'(a) 四个角点位于平面 $\Pi$ 内；(b) 单位立方体两条不平行面对角线之间的插值形成双曲抛物面。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);s,n=re.subn(r'^336 常见曲面的构造\s*$','',s,count=1,flags=re.M);assert n==1
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');p.save(d)
print('Placed refined8.1 before extrusion section at natural font size,updated existing applied reference consistently,removed scanned page header.')
