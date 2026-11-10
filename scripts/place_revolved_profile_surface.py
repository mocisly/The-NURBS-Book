"""Place8.9 after the revolution proof and before familiar special surfaces."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_13.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.9\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='几种常见的表面是旋转表面。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{34cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.9. 图8.8同一条生成曲线的旋转曲面。两图采用相同投影、比例及面板尺寸。'+'\\\\\n'+
       r'(a) $9\times6$控制网，首尾控制列重合，共48个不同的控制点；权重为圆权重与生成线权重的乘积。'+'\\\\\n'+
       r'(b) 实际曲面上的5条纬圆与8条子午线，分别取$v=j/4$和$u=i/8$；以透明线框显示。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.9 paired net/surface after tensor revolution proof.')
