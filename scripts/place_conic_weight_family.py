"""Group7.12 after the weight/shoulder discussion with precise labels."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_12.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.12\.[^\n]*'
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.12. 同一代表性控制三角形下的圆锥弧族，$w_0=w_2=1$，$w_1=3,1,3/10,0,-3/10$。\\\\\n'
       r'圆圈标出各弧在 $u=1/2$ 处的肩点；$\mathbf S$ 为 $w_1=3/10$ 的肩点，$\mathbf M$ 为弦的中点。零权重产生弦段，负权重产生三角形外的互补弧。'+
       '\n\\end{minipage}\n\\end{center}')
s,n=re.subn(pattern,lambda m:block,s,count=1);assert n==1
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Grouped7.12 at weight/shoulder derivation with explicit zero/negative arc caption.')
