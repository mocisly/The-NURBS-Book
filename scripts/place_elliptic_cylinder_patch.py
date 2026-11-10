"""Keep8.4 at the end of extrusion, alongside the elliptical-cylinder explanation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_04.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.4\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\section{规则曲面}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{28cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.4. 将开放椭圆弧沿其平面法向平移得到的椭圆柱面片；截线由三个有理二次段组成，平移方向为一次。'+'\\\\\n'+
       r'实线为曲面边界，细虚线为两层同权重控制网；投影和坐标比例与图8.2、8.3相同。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.4 after elliptical extrusion explanation and before ruled-surface section.')
