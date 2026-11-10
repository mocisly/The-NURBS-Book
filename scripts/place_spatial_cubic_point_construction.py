"""Place9.55afterits3geometry steps;distinguish auxiliary points fromcurvepoints."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_67.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.55[。.][^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
old=r'事实证明，存在一条唯一的三次贝塞尔曲线通过 \(\mathbf{P}\) 、 \({\mathbf{P}}_{c}\) ，并且 \({\mathbf{P}}_{d}\) 可以按如下方式构造'
new=r'在满足后述拟合条件时，可唯一确定插值点\(\mathbf P\)的三次 Bézier 曲线；\(\mathbf P_c\)与\(\mathbf P_d\)是辅助构造点，可按如下方式得到'
assert s.count(old)==1;s=s.replace(old,new,1)
anchor='方程 (9.100) 现在得出';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.55. 非共面三次 Bézier 曲线的代表性构造，取$P_0=(4,0,0)$、$P_1=(4,4,0)$、$P_2=(0,3,0)$、$P_3=(0,0,4)$。'+'\\\\\n'+
       r'平面$\pi:x+z=4$；$P_c=(2,0,2)$、$P_d=(2,3/2,2)$为辅助点，$P=C(1/2)=(2,21/8,1/2)$为曲线插值点。'+'\\\\\n'+
       r'按单位端切向$T_s=(0,1,0)$、$T_e=(0,-3/5,4/5)$计算，$a=3/2$、$b=-15/8$精确恢复$\alpha=4$、$\beta=-5$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
for header in ('442 曲线和曲面拟合','444 曲线和曲面拟合'):s=s.replace(header,'',1)
f.write_text(s,encoding='utf-8');print('Placed9.55afterplane/intersectionsteps,explicitactualcoordinates;fixedfalsecurve-throughauxiliarypointwording,removedOCR442/444.')
