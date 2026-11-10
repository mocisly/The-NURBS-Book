"""Place9.3 between its definition and the comparison discussion;remove duplicated OCR."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_03.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.3\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
duplicate='节点向量 - 参见公式 [9.5] 和 [9.8])；以及通过平均获得的向心参数和节点(点划线曲线和底部节点向量 - 参见公式 [9.6] 和 [9.8])。在图 9.5 中，请注意弦长和向心参数化曲线如何适应点间距的变化。'
assert s.count('\n'+duplicate)==1;s=s.replace('\n'+duplicate,'',1)
anchor='在图 9.4 中，展示了不同参数化的比较。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.3. 七点三次插值的代表性示例；虚线为求解所得的控制多边形。'+'\\\\\n'+
       r'弦长参数为$\bar u=(0,10/101,30/101,55/101,75/101,88/101,1)$，'+'\\\\\n'+
       r'平均节点向量为$U=(0,0,0,0,95/303,160/303,218/303,1,1,1,1)$。'+'\\\\\n'+
       r'下方圆圈表示数据参数，短刻线表示节点；四重端节点略微错开显示。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed9.3 after chord/averaging explanation,before parameter comparisons;removed duplicated OCR continuation.')
