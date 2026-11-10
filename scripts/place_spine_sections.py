"""10.4 beside spine definition; document shared data and normal-plane anchors."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_07.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.4\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='每条截面曲线的方向使其平面';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{24cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.4. 用于基于脊曲线蒙皮的一组代表性数据：脊曲线$C_s(v)$和五条局部截面$C_k(u)$。'+'\\\\\n'+
       r'方框标出脊参数$\widehat v_k=0,0.25,0.5,0.78,1$以及截面参数$\widehat u_k=1/2$。'+'\\\\\n'+
       r'脊曲线取五次多项式、截面取共同节点上的三次B样条；各局部截面以中点为原点。'+'\\\\\n'+
       r'所选数据记录于源码，后续定位与蒙皮对比图沿用此组数据。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('10.4placed after both positioning parameter sets and before normal-plane paragraph;shared representative data caption.')
