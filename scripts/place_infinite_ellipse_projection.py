"""Place7.24 with the infinite-control discussion, restore broken algorithm prose."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_29.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.24。[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'现在假设 \({\mathbf{P}}_{1}\left( {\overrightarrow{\mathbf{P}}}_{1}\right)\) 是无限的';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{19cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 7.24. 由端点、平行端切线和曲线上点 $\mathbf P$ 确定的 $180^\circ$ 椭圆弧。'+'\\\\\n'+
       r'$\mathbf P\mathbf Q\parallel\overrightarrow{\mathbf P}_1\parallel\mathbf T_0$；由式 (7.41) 可恢复非零无穷控制向量 $\overrightarrow{\mathbf P}_1$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
s,n=re.subn(r'我们利用\s+在 Intersect3DLines','我们利用在 Intersect3DLines',s,count=1);assert n==1
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.24 before infinite-control derivation; rejoined algorithm introduction previously split by bitmap.')
