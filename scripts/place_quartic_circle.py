"""Keep7.31 with its actual homogeneous quartic data in Ex7.9."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_39.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.31\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='Ex7.10 例子 Ex7.9 的四次圆的简单度提升得到';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 7.31. Ex7.9 的完整单位圆的有理四次 Bézier 表示，有限控制点为 $\mathbf Q_0=\mathbf Q_4=(1,0)$ 和 $\mathbf Q_2=(-3,0)$。'+'\\\\\n'+
       r'箭头表示两个非零无穷控制向量 $\overrightarrow{\mathbf Q}_1$ 和 $\overrightarrow{\mathbf Q}_3$ 的方向；闭合处的一阶导数相同。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed7.31 after quartic homogeneous controls and before quintic elevation example.')
