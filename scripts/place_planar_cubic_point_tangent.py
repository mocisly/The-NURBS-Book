"""Place9.56byEq9.107/108and repair the verified beta-increment sign9.110."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_68.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.56\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='方程 (9.107) 涉及点约束';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.56. 平面三次 Bézier 曲线的点与切向约束，取控制点$(0,0),(3,4),(6,4),(9,0)$。'+'\\\\\n'+
       r'在$u=1/2$处，de Casteljau 二级点$P_0^2=(3,3)$、$P_1^2=(6,3)$与$P=(9/2,3)$共线，严格确定中间切向$T_p=(1,0)$。'+'\\\\\n'+
       r'单位端切向为$T_s=(3/5,4/5)$、$T_e=(3/5,-4/5)$；公式 (9.107)、(9.108) 的兼容最小二乘系统精确给出$\alpha=5,\beta=-5$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
old=r'{\mathbf{T}}_{s} - \Delta {\beta }_{k}{B}_{2,3}';new=r'{\mathbf{T}}_{s} + \Delta {\beta }_{k}{B}_{2,3}'
assert s.count(old)==1;s=s.replace(old,new,1)
f.write_text(s,encoding='utf-8');print('Placed9.56afterpoint/tangent equations;exactdeCasteljaucaption;9.110beta increment correctedPLUSconsistentwith9.95anddefinitions,3independent exactcounterchecks.')
