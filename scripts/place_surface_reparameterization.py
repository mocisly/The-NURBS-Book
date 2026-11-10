"""Group6.14's four grids before the endpoint-weight example."""
import re
import image_tex as p
d=p.load();es=[next(e for e in d['images'] if e['tex']=='image_tex/ch06/'+name) for name in ('fig_6_16.tex','fig_6_17.tex','fig_6_18.tex')]
assert all(e['applied'] for e in es)
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8')
for e in es:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.14\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
s,n=re.subn(r'(?m)^图 6\.14a 显示了原始表面；[^\n]+',
            '图 6.14a 显示原参数化下的等参数步长网格；(b)只改变 $u$ 参数，(c)只改变 $v$ 参数，(d)同时改变两个参数。曲面几何形状相同，而等参数步长线的空间分布发生变化。',s,count=1);assert n==1
s,n=re.subn(r'(?m)^图 6\.14c 在 [^\n]+\n','',s,count=1);assert n==1
anchor=r'现在假设 \(\mathbf{C}\left( u\right)\) 的末端权重不相等';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+es[0]['replacement']+
       '\n\\par\\vspace{.6\\baselineskip}\n\\begin{minipage}[c]{12.5cm}\n\\centering\n'+es[1]['replacement']+
       '\n\\end{minipage}\\hspace{.5cm}\n\\begin{minipage}[c]{12.5cm}\n\\centering\n'+es[2]['replacement']+
       '\n\\end{minipage}\n\\par\\smallskip\n图 6.14. 同一代表性三次$\\times$二次曲面的有理重参数化；四图共用控制点、几何形状与视角。\\\\\n'
       '(a)原参数化；(b)只改变 $u$；(c)只改变 $v$；(d)同时改变两个参数。\\\\\n'
       '每个方向均画11条等参数步长线；重参数化方向在新区间 $[1/2,3/5]$ 内取等步长，使用正文给定的分式线性映射。\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert all(s.count(e['replacement'])==1 for e in es)
f.write_text(s,encoding='utf-8');print('Grouped6.14 two-by-two; moved panel d out of the6.15 example and clarified equal parameter increments.')
