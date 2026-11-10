"""Place7.15 after its exact semicircle formulas and shoulder discussion."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_15.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.15\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='请注意，无限控制点和零权重之间是有区别的。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{20cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.15. 通过使用无穷控制点定义的半圆。\\\\\n'
       r'两条细箭头为同一向量 $\overrightarrow{\mathbf P}_1=(0,r)$；其齐次控制点为 $(0,r,0)$。方框标出肩点 $\mathbf C(1/2)=(0,r)$，虚线为该点处的水平切线。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.15 after exact semicircle and shoulder derivation, before zero-weight distinction.')
