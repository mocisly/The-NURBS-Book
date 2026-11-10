"""Place7.6 after its rational hyperbola domain explanation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_06.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.6\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='最后\n\n\\[';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{16cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.6. 双曲弧的有理参数化（式7.9）。\\\\\n'
       r'示例取 $a=b=1$；加号对应 $u=i/25$（$i=1,\ldots,19$），圆圈为 $u=0,4/5$。图示区间位于右支，且避开 $u=1$ 的奇点。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.6 after hyperbola parameter-domain explanation, before parabola formula.')
