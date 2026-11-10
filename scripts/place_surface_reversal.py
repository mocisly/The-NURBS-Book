"""Keep6.17 with reversal formulas, outside the following power-basis derivation."""
import re
import image_tex as p
d=p.load();es=[next(e for e in d['images'] if e['tex']=='image_tex/ch06/'+name) for name in ('fig_6_21.tex','fig_6_22.tex')]
assert all(e['applied'] for e in es)
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8')
for e in es:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.17\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor=r'\section{B-spline 和分段幂基形式之间的转换}';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{28cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+es[0]['replacement']+
       '\n\\par\\vspace{.7\\baselineskip}\n'+es[1]['replacement']+
       '\n\\par\\smallskip\n图 6.17. 同一曲面反向后，同一几何点处的偏导向量与法向量。\\\\\n'
       r'(a)原参数化；(b)$s=1-u$，$\mathbf S_s=-\mathbf S_u$；(c)$t=1-v$，$\mathbf S_t=-\mathbf S_v$。'+'\\\\\n'
       r'两种单向反转均使法向变为 $-\mathbf N$；虚线等参线经过同一点。'+'\\\\\n'
       '各图一阶偏导箭头均画为原长的 $1/2$，法向箭头均画为原长的 $1/8$。\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
assert s.count('\n266 高级几何算法\n')==1;s=s.replace('\n266 高级几何算法\n','\n',1)
assert all(s.count(e['replacement'])==1 for e in es)
f.write_text(s,encoding='utf-8');print('Grouped6.17 before power-basis section, explicit vector display factors, removed its OCR header interruption.')
