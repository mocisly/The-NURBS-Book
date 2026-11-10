import re
import image_tex as p
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/ch11/fig_11_32.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*11\.26\.[^\n]*'
caption=r'图 11.26. 向与原曲线不相交的直线$L:-4x+3y=1$作局部正交投影。'+'\\\\\n'+r'(a) 代表性原曲线及控制多边形；(b) 对$[u_s,u_e]=[1/8,1/2]$内局部细化后的控制点作投影，得到精确直线段。'+'\\\\\n'+r'点线为原曲线；所选区间外的全部多项式段严格不变，简单节点保留原有光滑过渡。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}';s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8');print('11.26 same-sizeAB group before surface flattening introduction.')
