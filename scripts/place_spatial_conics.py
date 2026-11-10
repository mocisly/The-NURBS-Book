"""Group7.10 at the spatial-conic formulas with a precise basis caption."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_10.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.10\.[^\n]*'
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.10. 三维空间中的代表性椭圆、抛物线和双曲线。\\\\\n'
       r'三类曲线位于同一平面，共用原点 $\mathbf O$ 与正交单位基 $\mathbf X,\mathbf Y$；基向量箭头按单位长度绘制，虚线为局部坐标轴的延长线。'+
       '\n\\end{minipage}\n\\end{center}')
s,n=re.subn(pattern,lambda m:block,s,count=1);assert n==1
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Grouped7.10 at spatial formulas with orthonormal-frame caption.')
