"""Keep8.11 beside its polar explanation and restore uninterruptedA8.1."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_15.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.11\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='我们现在提出一个算法，该算法通过任意角度';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{28cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.11. 将半径$3/2$的五点二次半圆绕$z$轴旋转所得的球面，表示次数为$2\times2$。'+'\\\\\n'+
       r'细虚线为$9\times5$控制网，权重为圆与半圆权重的乘积；两极各有9个重合控制点，整个网共有26个不同控制点。'+'\\\\\n'+
       r'实线为$v=i/12$的11条纬圆与$u=i/12$的12条子午半圆，采用透明线框；极点处纬圆退化为点，球面的几何法线仍存在。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.11 after sphere/pole discussion and before general revolution algorithm.')
