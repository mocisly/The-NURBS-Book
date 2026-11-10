"""Pair7.18 before the positive-denominator and subsequent insertion derivation."""
import re
import image_tex as p
d=p.load();ee=[next(e for e in d['images'] if e['tex']==f'image_tex/ch07/fig_7_{i}.tex') for i in (20,21)]
assert all(e['applied'] for e in ee)
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
for e in ee:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.18[。.][^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='负权重通常是不受欢迎的，因为我们失去了凸包属性';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{30cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'
       '\\begin{minipage}{14cm}\\centering\n'+ee[0]['replacement']+
       '\n\\end{minipage}\\hfill\n\\begin{minipage}{14cm}\\centering\n'+ee[1]['replacement']+
       '\n\\end{minipage}\n\\par\\smallskip\n'
       r'图 7.18. 使用负权重 $\{1,-1/2,1\}$ 的 $240^\circ$ 圆弧，两图使用 Ex7.4 的同一组控制点。'+'\\\\\n'
       r'(a) 控制多边形和等参数步长采样 $u=i/40$；(b) 三个有理基函数，$R_{1,2}$ 的最小值为 $-1$，$R_{0,2}$ 和 $R_{2,2}$ 的最大值为 $4/3$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
for e in ee:assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8');print('Paired7.18 by original negative-weight data, before denominator/insertion discussion.')
