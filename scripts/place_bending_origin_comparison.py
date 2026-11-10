import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch11/fig_11_36.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*11\.30。[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='最后，我们指出，为了实现额外的形状控制，';assert s.count(anchor)==1
caption=r'图 11.30. 在同一原曲线、圆弧和交比$\lambda=2$下，仅改变弯曲中心的位置。'+'\\\\\n'+r'$O_1=(0,3)$为圆心，$O_2=(0,6/5)$位于对称轴上，$O_3=(-1,2)$偏离对称轴；三点均严格位于圆内。'+'\\\\\n'+r'曲线及两端刚体调整均由相应中心重新计算；线型与下方图例一一对应。'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.30 next to11.29 before surface extension, same comparison input/lambda.')
