"""Keep6.4 together after the complete tangent-inversion linear system."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_04.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.4\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\section{曲线和曲面的变换与投影}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{25cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n图 6.4. 曲面切向量反演：右侧参数曲线经曲面映射成为左侧的空间曲线。\\\\\n'
       r'在对应点，$\mathbf W=(du,dv)$ 映为 $\mathbf T=\mathbf S_u\,du+\mathbf S_v\,dv$；虚线为经过该点的等参线。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(ref)==1;f.write_text(s,encoding='utf-8')
print('Grouped6.4 after Eq6.11 and its solution; parameter-space/surface correspondence explained.')
