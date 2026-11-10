"""Place7.11 after its barycentric definitions, before the implicit derivation."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_11.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.11\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='使用恒等式';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.11. 有理二次Bézier曲线的局部斜坐标系。\\\\\n'
       r'代表性控制点取 $(0,0),(4,5),(8,0)$，权重为 $1,1/2,1$。在 $u=2/5$ 处，$\alpha=9/19,\ \beta=4/19$；两段箭头依次给出 $\alpha\mathbf S$ 和 $\beta\mathbf T$，到达 $\mathbf C(u)$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.11 directly after7.24, before oblique implicit equation derivation.')
