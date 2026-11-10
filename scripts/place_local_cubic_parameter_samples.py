"""Place9.30 with the cubic parameterization discussion."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_36.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.30\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\subsection{局部双三次曲面插值}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.30. 给定七个代表性数据点及单位切向的局部$C^1$三次插值，展示近似弧长参数化的效果。'+'\\\\\n'+
       r'六段的$\alpha$依次为$2,3,2,3/2,4,2$，归一化数据参数为$(0,4/29,10/29,14/29,17/29,25/29,1)$。'+'\\\\\n'+
       r'“$+$”是在$u=j/58$处计算的五十九个实际样本，七个数据点加画圆圈；数据点及各段参数中点的速度精确为$29/2$，其他位置的速度仍可变化，因此样本并非严格等弧长。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.30 from bicubic Eq9.55 to local cubic parameterization discussion.')
