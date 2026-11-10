import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch11/fig_11_37.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*11\.31\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='最后，我们指出，为了实现额外的形状控制，';assert s.count(anchor)==1
caption=r'图 11.31. 将含有两个拐点的代表性三次曲线向抛物线$B:y=3-x^2/8$弯曲，取$\lambda=1$。'+'\\\\\n'+r'方框标出原曲线的弯曲区间$[1/8,7/8]$；区间内控制点沿射线映射，两端按正文作刚体调整。'+'\\\\\n'+r'虚线为目标抛物线，两条实线为前后曲线；原来的两个拐点精确定位，修改后逐段曲率分子严格为负。'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.31 moved beside circular examples, before surface bending. Restored split cylinder-axis sentence.')
