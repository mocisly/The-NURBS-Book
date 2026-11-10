"""Keep both8.15 panels together beside the paraboloid scaling example."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch08/fig_8_{n:02d}.tex') for n in (19,20)]
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    assert e['applied'];pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.15\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1,e['tex']
orphan='如果控制点存储在 350 常见曲面的构造中';assert s.count(orphan)==1;s=s.replace(orphan,'',1)
anchor='通过将缩放因子应用于三维控制点';assert s.count(anchor)==1
block=r'''\begin{center}
\begin{minipage}{27cm}
\vspace*{.6\baselineskip}
\centering
'''+entries[0]['replacement']+r'''
\par\medskip
'''+entries[1]['replacement']+r'''
\par\smallskip
图 8.15. 旋转抛物面及其非均匀缩放；两图采用相同投影、坐标比例与等参数位置。\\
(a) 将二次抛物线$r(v)=3v/2$、$z(v)=9v^2/4$绕$z$轴旋转，得到$x^2+y^2=z$的有限曲面片。\\
(b) 将(a)的控制点按$F=(3/2,3/4,1)$缩放，得到$x^2/(3/2)^2+y^2/(3/4)^2=z$，权重及节点均不变。\\
两者均为二次乘二次，细虚线为$9\times3$控制网，各有17个不同控制点；顶点控制层退化为一个点。\\
实线为$v=j/16$处的16条平行截线和$u=i/8$处的8条抛物线子午线，采用透明线框。
\end{minipage}
\end{center}

'''
s=s.replace(anchor,block+anchor,1)
for e in entries:assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8');print('Placed8.15a/b together after paraboloid scaling description;removed orphan scanned-page text.')
