"""Place9.20 after G1construction,before C1reparameterization and knot removal."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_24.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.20\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='内部节点的选择不会影响曲线的形状，仅影响参数化。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.20. 六个代表性数据点的$G^1$连续二次插值；$\mathbf R_1,\ldots,\mathbf R_5$为相邻有向切线的交点。'+'\\\\\n'+
       r'第$k$段由二次Bézier控制点$(\mathbf Q_{k-1},\mathbf R_k,\mathbf Q_k)$定义，各连接处切线方向一致。'+'\\\\\n'+
       r'数据点以带中心点的圆圈标记，空心圆为切线交点；取$\bar u_k=k/5$，内部节点均为双重。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.20 immediately after G1construction,before C1parameterization;rejoined control/knot definitions.')
