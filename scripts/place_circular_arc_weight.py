"""Move7.13 beside its circle-weight proof, before the infinite-control section."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_13.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.13[。.][^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='本节中的许多材料可以追溯到';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.13. 小于$180^\\circ$圆弧的二次有理Bézier表示。\\\\\n'
       r'代表性等腰控制三角形取 $e=3,f=5$，故 $w_1=e/f=3/5$。肩点满足 $|\mathbf{MS}|/|\mathbf{SP}_1|=3/5$，$\mathbf P_2\mathbf S$ 为 $\angle\mathbf P_1\mathbf P_2\mathbf M$ 的平分线。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.13 after7.33, before infinite-control section; standardized caption punctuation.')
