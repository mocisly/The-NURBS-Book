"""Place 7.20 beside Ex7.5 and correct its two verified homogeneous signs."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_23.tex');assert e['applied']
f=p.ROOT/'chapter/7.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*7\.20\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
start=s.index('Ex7.5 使用四个控制点');end=s.index('Ex7.6 使用七点方形',start)
part=s[start:end]
for i,old,new in [(1,r'{-\frac{1}{2},\frac{1}{2},\frac{1}{2}}',r'{\frac{1}{2},\frac{1}{2},\frac{1}{2}}'),(2,r'{\frac{1}{2},\frac{1}{2},\frac{1}{2}}',r'{-\frac{1}{2},\frac{1}{2},\frac{1}{2}}')]:
    lines=part.splitlines();matches=[j for j,line in enumerate(lines) if line.startswith(r'{\mathbf{Q}}_{'+str(i)+r'}^{w}')];assert len(matches)==1
    j=matches[0];assert lines[j].count(old)==1;lines[j]=lines[j].replace(old,new);part='\n'.join(lines)+'\n'
block=('\\begin{center}\n\\begin{minipage}{32cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n图 7.20. 图7.15的半圆（$r=1$）在$u=1/2$处插入一次节点，得到四个有限控制点及权重$\\{1,1/2,1/2,1\\}$。\\\\\n'+
       r'(a) 控制多边形与等参数步长采样点 $u=i/40$；形状和参数化保持不变；(b) 对应的四个有理基函数。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s[:start]+part+block+s[end:];assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8');print('Placed7.20 after Ex7.5 data; corrected exact Boehm Q1/Q2 x signs.')
