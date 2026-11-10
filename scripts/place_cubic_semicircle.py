"""Keep7.29 with Ex7.7's degree-elevated data."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_37.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.29\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='示例 Ex7.8 示例 Ex7.4 中给出的弧';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{20cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 7.29. Ex7.7 的半圆经一次升阶后的有理三次 Bézier 表示，四个控制点均为有限点，权重为 $\{1,1/3,1/3,1\}$。'+'\\\\\n'+
       r'曲线形状与原参数化保持不变；坐标比例与前面的单位圆图一致。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed7.29 after Ex7.7 elevated controls and before Ex7.8.')
