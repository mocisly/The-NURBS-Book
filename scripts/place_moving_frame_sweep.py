"""10.12all three panels after their explanation and before10.13 scaling data."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex') for n in (16,17)];assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.12\.[^\n]*'
    s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='图 10.13a-10.13c 显示了截面曲线通过原点的扫掠示例';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{35cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+'\\par\\vspace{.5cm}\n'+entries[1]['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.12. 同一条平面轨迹与同一截面的两种移动标架扫掠。'+'\\\\\n'+
       r'(a) 代表性五次PH轨迹、七点三次截面和起始方向$B_0=(0,0,1)$；截面不经过原点。'+'\\\\\n'+
       r'(b) A10.2：放置七个近似等弧长截面，以$q=3$及式(10.8)的参数进行蒙皮；'+'\\\\\n'+
       r'(c) A10.1：继承轨迹的五次节点向量，在十个节点平均参数处放置截面并插值。'+'\\\\\n'+
       r'两例以$K=6$为输入下限；(c)由轨迹的十个控制点要求增加截面数。粗线为实际插值的截面，虚线为参考轨迹。'+'\\\\\n'+
       r'所选截面及两个近似曲面均满足$z\geq0.3$，轨迹位于$z=0$，因此轨迹不属于任何一个曲面。'+'\\\\\n'+
       r'三图共用视角、坐标尺度、字号与线宽；代表性控制点、精确标架和插值参数均记录于源码。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('10.12ABCgroup aftermethodexplanation/before10.13scaling;restoredscalingcontrolsandknotsascontinuousdefinition.')
