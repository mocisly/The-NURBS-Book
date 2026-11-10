"""Place9.26 after the shoulder-weight recipe, keeping cubic derivation intact."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_32.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.26\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='在计算 \\({\\mathbf{R}}_{k}\\) 的特殊情况下的识别';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.26. 非等腰控制三角形的角平分线与肩点权重构造；两端权重为$1$。'+'\\\\\n'+
       r'选取边长$13/2,15/2,7$的代表性三角形；$\mathbf S_1,\mathbf S_2$分别位于$\mathbf M\mathbf R_k$的$7/20,7/22$处。'+'\\\\\n'+
       r'其平均点$\mathbf S$位于$147/440$处，故$w_k=147/293$；实际有理二次曲线满足$\mathbf C(1/2)=\mathbf S$。实心小点为肩点，引线用于区分三个邻近标注。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.26 immediately after shoulder-weight step e, before exceptional rational cases.')
