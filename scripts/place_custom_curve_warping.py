import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch11/fig_11_24.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.21\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='表面变形类似于曲线变形。';assert s.count(anchor)==1
caption=r'图 11.21. 两种不同形状函数驱动的局部曲线变形，下方绘出实际使用的$f(t)$。'+'\\\\\n'+r'(a) 三峰形状函数；(b) 平顶形状函数。各段用端点斜率为零的三次Hermite函数连接，函数整体为$C^1$。'+'\\\\\n'+r'两例使用图11.19的同一抛物线，区间内五轮中点细化后按累积弦长应用式(11.48)，$d=3/5,W=(0,-1)$。'+'\\\\\n'+r'点线表示原曲线，方框表示区间端点；区间外的曲线完全不变，明确函数及控制数据见源码。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.21 before surface subsection, paired shape and actual resulting curve.')
