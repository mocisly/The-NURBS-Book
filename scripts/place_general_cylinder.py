"""Keep8.2 directly with extrusion formula8.2 and its paired controls."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_02.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.2\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='右圆柱体是通过将 NURBS 圆沿';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{30cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.2. 一般圆柱面 $\mathbf S(u,v)=\mathbf C(u)+vd\mathbf W$：将代表性闭合 NURBS 轮廓沿单位方向 $\mathbf W$ 平移距离 $d$。'+'\\\\\n'+
       r'$u=\bar u$ 为直母线，$v=\bar v$ 为平移后的截线。采用透明线框；细虚线为控制网，中间虚线闭合曲线为一条等 $v$ 截线。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.2 after exact extrusion control-net construction and before circular cylinder example.')
