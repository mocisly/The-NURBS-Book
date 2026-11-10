"""10.14all panels beside 3D example, restoring projected-normal construction prose."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex') for n in (20,21)];assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.14\.[^\n]*'
    s,n=re.subn(pat,'',s,count=1);assert n==1
s=s.replace('482 高级表面构造技术','',1)
join=r'\({\mathbf{B}}_{i}\) ，';s=re.sub(re.escape(join)+r'\s*然后使用插值',lambda _:join+'然后使用插值',s,count=1)
anchor='截面曲线的位置和大小，以及轨迹的形状';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+'\\par\\vspace{.5cm}\n'+entries[1]['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.14. 三维轨迹下的移动标架扫掠，两个结果使用相同截面和常量缩放$(3/5,3/5,1)$。'+'\\\\\n'+
       r'(a) 代表性空间三次轨迹、过原点的截面和起始正交方向；所选连续正交标架记录于源码；'+'\\\\\n'+
       r'(b) A10.2，以七个截面进行三次蒙皮，虚线为未施加精确约束的参考轨迹；'+'\\\\\n'+
       r'(c) A10.1，继承轨迹节点向量并插值十一个截面，实线轨迹严格满足$S(1/2,v)=T(v)$。'+'\\\\\n'+
       r'细线为真实等参数曲线，较粗的横向曲线为给定截面；三图统一投影、尺度、字号和线宽。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('10.14group follows3Dtrajectoryexample/beforeoffsetexamples,wholeTidentityexplicit;projectednormalproserestored/OCR482removed.')
