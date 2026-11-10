"""10.9beside both displayed anchor parameter sets, before rational skinning."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_12.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.9\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='现在我们考虑一些截面曲线为有理的情况';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{34cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.9. 改变截面定位参数后的蒙皮曲面，脊曲线及五条截面的形状与图 10.7 相同。'+'\\\\\n'+
       r'(a) $\widehat v=(0,0.35,0.5,0.62,1)$，$\widehat u=(0.5,0.5,0.5,0.5,0.5)$；'+'\\\\\n'+
       r'(b) $\widehat v=(0,0.25,0.5,0.78,1)$，$\widehat u=(0.5,0.3,0.5,0.9,0.5)$。'+'\\\\\n'+
       r'两例均按图 10.7 的带导数约束步骤重新计算插值参数、节点及控制网；粗线为实际给定截面。'+'\\\\\n'+
       r'定位保持截面形状，满足$C_k(\widehat u_k)=C_s(\widehat v_k)$；两图共用视角、坐标尺度、字号和线宽。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('10.9grouped immediatelyafter both printed parameter sets,allspine/profiledatareused;nointerruptionofrationaldiscussion.')
