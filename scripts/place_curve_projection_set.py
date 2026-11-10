"""Keep6.2 with curve projection, before introducing surface projection."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_02.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.2\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
caption=(r'图 6.2. 一组点到代表性分段三次NURBS曲线的最近投影，各权重为一。'
         '\\\\\n'+r'细线表示采样点与最近曲线点的连线；光滑段上的投影沿法线方向，端点及$u=7/10$处的$C^0$转角允许多条连线汇聚。')
block='\\begin{center}\n\\begin{minipage}{22.4cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n'
anchor='点反演和表面的投影是类似的。形成向量函数';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
assert s.count(ref)==1;f.write_text(s,encoding='utf-8');print('Placed6.2 beside curve-projection discussion; distinguished smooth normals from endpoint/C0 fans.')
