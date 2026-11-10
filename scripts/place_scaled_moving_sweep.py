"""10.13beside its scaling function, before spatial trajectories/Frenet frames."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex') for n in (18,19)];assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.13\.[^\n]*'
    s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='前两个例子使用了平面轨迹曲线。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+'\\par\\vspace{.5cm}\n'+entries[1]['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.13. 截面通过原点时，不缩放与分段线性缩放的扫掠比较。'+'\\\\\n'+
       r'(a) 沿用图 10.12 的轨迹和截面形状，将截面平移到$C(1/2)=0$，空心点标出原点；'+'\\\\\n'+
       r'(b) 单位缩放；(c) 使用正文给出的四个缩放控制向量和节点$0,0,0.3,0.7,1,1$。'+'\\\\\n'+
       r'两例均按A10.2，在相同的七个近似等弧长位置放置截面，再分别计算插值参数与三次蒙皮。'+'\\\\\n'+
       r'粗线为实际插值的截面，虚线为参考轨迹；截面与轨迹在七个放置点相交，整条轨迹未作精确插值约束。'+'\\\\\n'+
       r'三个子图共用视角、坐标尺度、字号与线宽，以显示缩放带来的实际形状变化。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('10.13ABCgroup followscompleteprintedscalingdefinition,before3Dexamples;Frenetdiscussionand10.26rejoined.')
