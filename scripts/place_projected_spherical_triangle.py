"""Keep8.18 beside planar-patch construction and before coefficient derivation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_23.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.18\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='显然，可以推导出计算';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{30cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.18. 球面三边角片与投影平面片$\mathbf S_2$；取$R=1$，投影圆弧以$\mathbf O=(0,0)$为圆心、半径$r=2$。'+'\\\\\n'+
       r'本例控制点为$\mathbf P_{0,1}=(2,0)$、$\mathbf P_{1,1}=(2,8/3)$、$\mathbf P_{2,1}=(-14/25,48/25)$，权重为$1,3/5,1$。'+'\\\\\n'+
       r'弦中点$\mathbf M=(18/25,24/25)$满足$\overrightarrow{\mathbf{OM}}\cdot\overrightarrow{\mathbf{OP}}_{1,1}=r^2$，反演系数为$25/9$。'+'\\\\\n'+
       r'平面片沿圆弧向原点作直线连接，次数为$2\times1$，$t=0$边界退化为一点；式(8.13)将其三条非退化边界映射为球面大圆弧$\mathbf C_1,\mathbf C_2,\mathbf C_3$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.18 after planar-patch/composition explanation,before power-coefficient derivation.')
