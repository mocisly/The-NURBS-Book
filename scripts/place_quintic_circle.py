"""Place7.32 with Ex7.10 and state its exact elevation/rotation convention."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_40.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.32\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
old='Ex7.10 例子 Ex7.9 的四次圆的简单度提升得到'
new=r'Ex7.10 将 Ex7.9 的四次圆进行一次升阶，再将平面坐标顺时针旋转 $90^\circ$，并把所有齐次坐标统一乘以 $5/3$，得到'
assert s.count(old)==1;s=s.replace(old,new,1)
anchor='Chou [Chou95] 证明了仅使用正权重';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 7.32. Ex7.10 的完整单位圆的有理五次 Bézier 表示；六个控制点均有限，权重为 $\{5,1,1,1,1,5\}$。'+'\\\\\n'+
       r'控制多边形、曲线与坐标轴采用相同几何比例；闭合点为 $\mathbf R_0=\mathbf R_5=(0,-1)$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed7.32 after quintic data; specified clockwise90deg and common5/3 homogeneous scale needed for stated controls.')
