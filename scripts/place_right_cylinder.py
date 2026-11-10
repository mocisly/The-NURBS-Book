"""Place8.3 beside its actual tensor control net and formula8.3."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_03.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.3\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='通过平移由算法 A7.1 和 A7.3 计算出的控制点';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{28cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.3. 将 Ex7.2 的九点方形 NURBS 圆沿其平面法向平移所得的直圆柱面，表示次数为 $2\times1$。'+'\\\\\n'+
       r'细虚线为外接控制网；两端圆和两条轮廓母线用实线表示。两层圆控制点的权重相同。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);s=s.replace('右圆柱体','直圆柱体');assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.3 after its tensor-product equation/control weights and before elliptical extrusion discussion.')
