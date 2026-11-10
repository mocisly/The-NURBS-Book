"""Place9.27 with rational interpolation, away from the cubic derivation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_33.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.27\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{局部三次曲线插值}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.27. 代表性机械轮廓的局部有理二次插值；空心圆为输入数据点。'+'\\\\\n'+
       r'外边界由十三点构造，保留底部两个直角及共线段；每个圆孔仅用四个圆周点和周期 Akima 切向构造。'+'\\\\\n'+
       r'曲线段的端权重为$1$，各四分之一圆段取中间权重$\sqrt2/2$，因此圆弧和两个圆孔在数学上被精确再现。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.27 at end of local rational interpolation;reconnected cubic Eq9.48 derivation.')
