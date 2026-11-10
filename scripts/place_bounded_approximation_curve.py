"""Place9.2 next to endpoint-constrained approximation,before the fitting discussion."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_02.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.2\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='拟合中有许多微妙之处';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.2. 满足误差界和端点约束的近似曲线，采用代表性示例$\mathbf C(t)=(8t,25t/2-12t^2)$，$m=8$。'+'\\\\\n'+
       r'每个数据点到曲线的最短距离均小于$E=1/2$，两端点满足$e_0=e_m=0$；图中取$i=6$，$e_i$为$\mathbf Q_i$沿法线投影到曲线的距离。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed9.2 after approximation/error-bound definition,before general fitting discussion.')
