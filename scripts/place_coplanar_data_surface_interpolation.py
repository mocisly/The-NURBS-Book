"""9.18 belongs to global surface interpolation;clarify local vs whole-data coplanarity."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_22.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.18\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='在图 9.18 中演示了无法处理共面的数据。';assert s.count(anchor)==1
description='图 9.18 表明，含有局部共面数据的网格经过全局插值后，相应区域不一定保持平坦；若全部数据都在同一平面上，线性插值系统仍会保持该平面。'
block=('\n\n\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.18. 局部共面数据的全局双三次插值，采用$5\times5$代表性数据。'+'\\\\\n'+
       r'(a) 二十四点位于$z=0$，中心点抬高至$z=6/5$；(b) 曲面通过全部二十五点，但在共面数据之间出现波动。'+'\\\\\n'+
       r'参数为$\bar u_i=\bar v_i=i/4$，节点向量$U=V=(0,0,0,0,1/2,1,1,1,1)$；两幅图使用相同的视角和尺度。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,description+block,1);f.write_text(s,encoding='utf-8')
print('Moved9.18 beside global coplanar-subset discussion;distinguished local flatness failure from entire-data plane preservation.')
