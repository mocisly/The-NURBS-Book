"""Correct Ex7.8 using exact elevation and place its actual240degree arc beside it."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_38.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.30\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
start=s.index('示例 Ex7.8 示例 Ex7.4 中给出的弧');end=s.index('以下的四阶和五阶完整圆构造',start)
old=s[start:end];assert r'\frac{1}{6}' in old and r'{{2a}, - 3}' in old
corrected=(r'示例 Ex7.8 对 Ex7.4 的 $240^\circ$ 圆弧进行一次升阶，得到三次表示（见图7.30）：'+'\n\n'+
    r'\[ U=\{0,0,0,0,1,1,1,1\} \]'+'\n\n'+
    r'\[ \{\mathbf Q_i^w\}=\left\{(a,\tfrac12,1),\ (\tfrac a3,-\tfrac12,0),\ (-\tfrac a3,-\tfrac12,0),\ (-a,\tfrac12,1)\right\},\qquad a=\frac{\sqrt3}{2}. \]'+'\n\n'+
    r'因此权重为 $\{1,0,0,1\}$。两个内部齐次控制点的权重为零，空间部分非零，分别表示无穷控制向量 $\overrightarrow{\mathbf Q}_1=(a/3,-1/2)$ 和 $\overrightarrow{\mathbf Q}_2=(-a/3,-1/2)$。升阶保持圆弧的形状和原参数化；若要求所有控制点有限且权重为正，可继续升阶。'+'\n\n')
block=('\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 7.30. Ex7.4 的 $240^\circ$ 单位圆弧经一次升阶后的有理三次 Bézier 表示。'+'\\\\\n'+
       r'两个内部控制点为非零无穷控制向量，箭头表示其方向；曲线及参数化与升阶前相同。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s[:start]+corrected+block+s[end:];assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Corrected Ex7.8 from inconsistent finite data to exact elevated H controls and weights1,0,0,1; placed actual240circle immediately after example.')
