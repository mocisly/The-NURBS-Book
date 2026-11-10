"""Place9.19 beside its defining vector blends,before tangent estimation schemes."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_23.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.19\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='方程 (9.29) 不使用参数';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.19. 局部插值的弦向量、切向混合向量及导数估计，采用五个代表性数据点。'+'\\\\\n'+
       r'取公式 (9.31) 的$\alpha_k=21/47$，并令$\Delta\bar u_k=2/5$、$\Delta\bar u_{k+1}=7/10$，'+'\\\\\n'+
       r'公式 (9.29)、(9.28) 分别给出$\mathbf V_k=(732/235,6/47)$、$\mathbf D_k=(276/47,42/47)$，所有箭头按同一坐标尺度绘制。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.19 beside Eq9.28/29;rejoined later corner-choice paragraph and bullet list.')
