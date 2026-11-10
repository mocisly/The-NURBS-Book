"""Place8.7 entirely within the ruled-surface section with explicit representative data."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch08/fig_8_{n:02d}.tex') for n in (10,11)]
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    assert e['applied'];pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.7\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1,e['tex']
anchor=r'\section{旋转曲面}';assert s.count(anchor)==1
block=r'''\begin{center}
\begin{minipage}{36cm}
\vspace*{.6\baselineskip}
\centering
'''+entries[0]['replacement']+r'''
\par\medskip
'''+entries[1]['replacement']+r'''
\par\smallskip
图 8.7. 圆与直线之间的直纹曲面；以下为说明不同参数对应关系而选取的代表性数据。\\
三个圆均为$xy$平面内的单位圆，起点为$(1,0,0)$；圆表示依次为二次、三次和四次，曲面次数为$2\times1$、$3\times1$和$4\times1$。\\
(a) 九点二次圆与横向直线$\mathbf L(u)=(1-2u,0,2)$；(b) 两段三次半圆与竖直直线$\mathbf L(u)=(5/4,0,2-4u)$。\\
(c) 例7.9的四次圆与往返参数化的竖直直线$\mathbf L(u)=(2/5,-1/4,64u^3-96u^2+36u-2)$。\\
每幅图的细直线均连接$u=i/60$处的圆点和直线点；实线为两条边界，所有子图采用相同投影、坐标比例及透明线框。\\
上述次数指NURBS的参数次数，直母线上的有理参数与空间线性插值参数一般不同。
\end{minipage}
\end{center}

'''
s=s.replace(anchor,block+anchor,1)
for e in entries:assert s.count(e['replacement'])==1
s=s.replace('一些由直线和圆定义的奇异有规则曲面','一些由直线和圆定义的直纹曲面')
f.write_text(s,encoding='utf-8');print('Placed8.7 all three examples before revolution,with explicit representative data and parameter-degree terminology.')
