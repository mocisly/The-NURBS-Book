"""Put9.7 beside its collinearity discussion,repair endpoint row in neighboring example."""
import re
from fractions import Fraction as F
from global_interpolation_data import interpolate
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_07.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.7\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='图 9.7 显示了全局插值器无法处理共线点集的情况。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.7. 包含连续共线数据点的全局三次插值，采用十三个代表性数据点。'+'\\\\\n'+
       r'实线为弦长参数与平均节点下求解的插值曲线；虚线为连接数据点的折线参考。'+'\\\\\n'+
       r'曲线通过全部数据点，但在共线数据段之间仍出现偏离，说明全局插值不自动保持局部直线性。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,anchor+block,1)
# The clamped endpoint basis row is (0,0,0,0,1),not the OCR all-zero row.
U,P=interpolate(tuple(tuple(map(F,q)) for q in [(0,0),(3,4),(-1,4),(-4,0),(-4,-3)]),tuple(map(F,['0','5/17','9/17','14/17','1'])))
assert U[4]==F(28,51)
old=r'0 & 0 & 0 & 0 & 0 \end{matrix}';assert s.count(old)==1
s=s.replace(old,r'0 & 0 & 0 & 0 & 1 \end{matrix}',1)
f.write_text(s,encoding='utf-8')
print('Moved9.7 before Ex9.1 and identified actual/global-vs-data styles;repaired exact clamped endpoint matrix row.')
