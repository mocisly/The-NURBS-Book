"""Keep6.8 by the definition of composition, and join the interrupted weight item."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_08.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.8\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\(\mathbf{C}\left( s\right)\) 在几何上与';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n图 6.8. 曲线重参数化：$s\\in[c,d]$ 先经严格递增的 $f$ 映到 $u\\in[a,b]$，再经 $\\mathbf C$ 映到同一曲线点。\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
pattern=r'(\\item 末端权重的修改:.*?) 是 NURBS\s*\\end\{itemize\}\s*在曲线中，有时(.*?)\n\n\\section\*\{示例\}'
s,n=re.subn(pattern,lambda m:m[1]+' 是 NURBS 曲线，有时'+m[2]+'\n\\end{itemize}\n\n'+r'\section*{示例}',s,count=1,flags=re.S)
assert n==1 and s.count(ref)==1;f.write_text(s,encoding='utf-8')
print('Placed6.8 after composition definition and joined the weight-modification bullet split by old scan.')
