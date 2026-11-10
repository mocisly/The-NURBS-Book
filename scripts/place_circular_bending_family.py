import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch11/fig_11_35.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*11\.29。[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='最后，我们指出，为了实现额外的形状控制，';assert s.count(anchor)==1
caption=r'图 11.29. 同一曲线和圆弧弯曲目标下，交比$\lambda=1/2,1,2,5$的实际比较。'+'\\\\\n'+r'原曲线为代表性抛物线，圆心$O=(0,3)$、半径2；中部$[1/4,3/4]$按式(11.58)映射。'+'\\\\\n'+r'两端控制点按正文规定作旋转和平移，使未弯曲区段自然衔接；点线为原曲线，虚线为目标圆弧。'+'\\\\\n'+r'圆弧交点、交比与外部刚体变换逐点核验；当$\lambda=1$时映射控制点位于圆上，曲线近似圆弧。'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.29 before variable-lambda paragraph/surface extension, with complete rigid motion.')
