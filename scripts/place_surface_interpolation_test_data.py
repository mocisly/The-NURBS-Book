"""Place9.15 data before subsequent parameterization/degree comparisons."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_17.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.15\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'图 \({9.16}\mathrm{a} - {9.16}\mathrm{c}\) 中展示了具有不同参数化和节点向量的表面。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.15. 用于后续曲面插值比较的$4\times4$代表性数据；虚线仅连接相邻数据点。'+'\\\\\n'+
       r'取$x_i=(-2,-3/4,3/4,2)$、$y_j=(-2,-1/2,3/4,2)$，高度$z_{i,j}=h_i+a_i g_j$，'+'\\\\\n'+
       r'其中$h=(3,3,0,0)$、$a=(1,3/2,1/2,0)$、$g=(0,1/5,1/10,0)$，保留小幅横向起伏。'+'\\\\\n'+
       r'后续参数化与次数比较均使用这一组数据，并在各比较图中统一三维视角和尺度。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.15 data before parameterization comparisons,with exact representative input documented.')
