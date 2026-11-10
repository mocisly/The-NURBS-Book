"""Place9.53after the three construction steps with its complete explanation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_63.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.53\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='有三种特殊情况需要不同处理:';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.53. 局部圆锥拟合的代表性构造，取端点$(0,0),(6,0)$与切线交点$R=(3,4)$，箭头表示单位端切向。'+'\\\\\n'+
       r'三条虚线分别插值三个内部数据点；按公式 (9.92) 平均肩点参数得到$s=1/2,w=1$，实线为$C(u)=(6u,8u(1-u))$。'+'\\\\\n'+
       r'$M$为弦中点，$S=C(1/2)$；显示的$Q_i^{\prime}=C(3/5)$为$Q_i$的唯一最近点，误差线段与曲线切向精确正交。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.53afterall3conicfitsteps,beforeexceptions;captionexplicitrepresentativegeometry/actualshoulderaverage/uniqueclosestprojection/unitTsTe.')
