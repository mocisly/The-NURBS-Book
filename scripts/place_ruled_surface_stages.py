"""Keep the five stages together immediately after the ruled construction."""
import re
import image_tex as p
d=p.load(); entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch08/fig_8_{n:02d}.tex') for n in (5,6,7,8)]
f=p.ROOT/'chapter/8.tex'; s=f.read_text(encoding='utf-8')
for e in entries:
    assert e['applied']
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.5\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1); assert n==1,e['tex']
orphan=r'\(1/2,1/2,7/{10},3/4,3/4,1,1,1,1\}\) .'
assert orphan in s;s=s.replace(orphan,'',1)
anchor='一般锥体也是一个有规则的曲面。';assert s.count(anchor)==1
block=r'''\begin{center}
\begin{minipage}{30cm}
\vspace*{.6\baselineskip}
\centering
'''+entries[0]['replacement']+r'''
\par\medskip
'''+entries[1]['replacement']+r'''
\par\medskip
\begin{minipage}{14.3cm}\centering
'''+entries[2]['replacement']+r'''
\end{minipage}\hfill
\begin{minipage}{14.3cm}\centering
'''+entries[3]['replacement']+r'''
\end{minipage}
\par\smallskip
图 8.5. 两条曲线之间的直纹曲面构造，各子图采用相同投影和比例。\\
(a) 二次与三次输入曲线，分别含6个控制点；全部权重取1。节点向量为\\
\(U^1=\{0,0,0,\tfrac14,\tfrac12,\tfrac34,1,1,1\}\)，
\(U^2=\{0,0,0,0,\tfrac3{10},\tfrac7{10},1,1,1,1\}\)。\\
(b) 第一条曲线升为三次，控制点数变为10；(c) 两条曲线细化到共同节点向量，各有12个控制点。\\
\(U=\{0,0,0,0,\tfrac14,\tfrac14,\tfrac3{10},\tfrac12,\tfrac12,\tfrac7{10},\tfrac34,\tfrac34,1,1,1,1\}\)。\\
(b)、(c)的细虚线为前一步控制多边形；升阶和细化均保持曲线及其参数化不变。\\
(d) \(12\times2\)控制网；(e) 三次乘一次曲面，直母线连接两条边界上相同参数\(u=i/30\)的点。
\end{minipage}
\end{center}

'''
s=s.replace(anchor,block+anchor,1)
for e in entries:assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8');print('Placed all five8.5 stages before cone construction; removed split OCR caption.')
