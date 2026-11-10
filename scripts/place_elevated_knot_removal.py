"""Place5.36 with the shortcut derivation, out of algorithm A5.9."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch05/fig_5_51.tex');assert e['applied']
f=p.ROOT/'chapter/5.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.36\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
caption=(r'图 5.36. 四次曲线升为五次后移除三个冗余节点，曲线保持不变。'
         '\\\\\n'+r'代表性示例取$u_c=0$、$u_d=1/2$、$u_e=1$；$u_d$的重数由五降为二。'
         '\\\\\n'+r'细实线和空心圆表示两个五次Bézier段；虚线、点线表示局部恢复过程，方点表示所标的新控制点。')
block='\\begin{center}\n\\begin{minipage}{18.8cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n'
anchor='算法 A5.9 通过计算';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
assert s.count(ref)==1;f.write_text(s,encoding='utf-8');print('Moved5.36 from the algorithm to the local shortcut derivation; clarified elevated degree and multiplicities.')
