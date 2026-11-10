"""Place7.14 at its decomposition explanation, before the terminology note/example."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_14.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.14\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='我们在此警告读者';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{22cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.14. 带有无穷控制向量$\\overrightarrow{\\mathbf P}_2=(4,2)$的代表性三次NURBS曲线。\\\\\n'
       r'实线为 $\mathbf C(u)$，虚线为仅含有限控制点贡献的 $\overline{\mathbf C}(u)$；所示 $u=3/10$ 处的差向量为 $f(u)\overrightarrow{\mathbf P}_2$。'+'\\\\\n'
       r'两条细箭头表示同一控制向量；点线连接有限控制点 $\mathbf P_1,\mathbf P_3$。虚线曲线在两个内节点处分别接触 $\mathbf P_1\mathbf P_3$ 与 $\mathbf P_3\mathbf P_4$。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8');print('Placed7.14 after infinite-control decomposition and finite-edge discussion, before example7.1.')
