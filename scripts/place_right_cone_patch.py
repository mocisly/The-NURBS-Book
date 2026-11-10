"""Place8.6 with the collapsed-row cone construction, before revolution."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_09.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.6\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='我们再次强调，NURBS 曲面上的有规则线段';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{22cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.6. 直圆锥面片：将单位圆的270度圆弧与顶点$\mathbf P=(0,0,23/10)$相连，得到二次乘一次有理曲面。'+'\\\\\n'+
       r'细虚线为$7\times2$控制网；顶层控制点全部重合于顶点，且上下层对应权重相同。'+'\\\\\n'+
       r'实线为圆弧边界、两条端部母线与一条中间母线；采用透明线框表示，坐标投影和比例与图8.1--8.4相同。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8');print('Placed8.6 after cone construction and before equal-parameter warning.')
