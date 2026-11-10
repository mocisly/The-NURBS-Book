"""Keep8.14 with its implicit equation and affine construction."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_18.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.14\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='图 8.15b 显示了一个椭圆抛物面。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.14. 将单位球的控制点按$F=(1,3/4,9/5)$缩放所得的椭球；权重及节点向量均不变，半轴分别为$a=1$、$b=3/4$、$c=9/5$。'+'\\\\\n'+
       r'细虚线为$9\times5$控制网，仍有26个不同控制点；实线为15条纬椭圆和12条子午半椭圆，采用透明线框。'+'\\\\\n'+
       r'每个相同参数位置严格满足$\overline{\mathbf S}(u,v)=\operatorname{diag}(a,b,c)\mathbf S(u,v)$；坐标投影与比例沿用图8.11。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.14 immediately after ellipsoid equation/construction,before paraboloid.')
