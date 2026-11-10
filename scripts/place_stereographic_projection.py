"""Keep8.17 beside equation8.13 before the circle-correspondence properties."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_22.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.17\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='在此投影下，我们有以下对应关系:';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{28cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.17. 式(8.13)的立体投影：北极$(0,0,2R)$、球面点$(x,y,z)$和平面点$(u,v,0)$共线。'+'\\\\\n'+
       r'本例取$R=1$、$(u,v)=(1,2)$，映射点为$(4/9,8/9,10/9)$，严格满足$x^2+y^2+(z-1)^2=1$。'+'\\\\\n'+
       r'球面采用透明线框显示等参数圆。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
bad=r'众所周知的立体投影 \(\textit{projection (see [Coxe67; DoCa76]) yields a rational parametric representation of}\) 球体'
assert s.count(bad)==1;s=s.replace(bad,'立体投影（见[Coxe67; DoCa76]）给出该球面的有理参数表示',1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.17 after map formula/collinearity explanation,before circle correspondence properties.')
