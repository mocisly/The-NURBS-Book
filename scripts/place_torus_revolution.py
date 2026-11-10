"""Keep the torus next to its offset-circle construction, outside algorithmA8.1."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_14.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.10\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'通过围绕 \(z\) 轴旋转一个端点位于';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{34cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.10. 将$xz$平面内以$(8/5,0,0)$为圆心、半径为$1/2$的圆绕$z$轴旋转，得到大半径$R=8/5$、管半径$r=1/2$的环面。'+'\\\\\n'+
       r'曲面为二次乘二次；细虚线为$9\times9$控制网，两个方向首尾控制列均重合，共64个不同控制点，权重按两组圆权重相乘。'+'\\\\\n'+
       r'实线为参数值$i/12$处的12条纬圆和12条子午圆，采用透明线框；坐标投影与比例沿用图8.8。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.10 after torus construction,before sphere and algorithm.')
