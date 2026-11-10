"""Place6.20's three stages together and restore the exact inverse recurrence."""
import re
from fractions import Fraction as F
from math import comb
from inverse_knot_projection import solve
import image_tex as p

for degree in range(1,9):
    n=degree+1
    M=tuple(tuple(F((-1)**(i-j)*comb(degree,j)*comb(degree-j,i-j)) if i>=j else F(0) for j in range(n)) for i in range(n))
    I=tuple(tuple(F(i==j) for j in range(n)) for i in range(n))
    MI=solve(M,I)
    assert all(MI[j][k]==-sum(M[j][i]*MI[i][k] for i in range(k,j))/M[j][j] for k in range(n) for j in range(k+1,n))
d=p.load();ee=[next(e for e in d['images'] if e['tex']==f'image_tex/ch06/fig_6_{i}.tex') for i in (26,27)]
assert all(e['applied'] for e in ee)
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8')
for e in ee:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.20\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='给定 \\({M}_{p}\\) ，';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'
       '\\begin{minipage}{11.6cm}\\centering\n'+ee[0]['replacement']+
       '\n\\end{minipage}\\hfill\n\\begin{minipage}{24.4cm}\\centering\n'+ee[1]['replacement']+
       '\n\\end{minipage}\n\\par\\smallskip\n'
       r'图 6.20. 同一条代表性分段三次曲线的三种表示：'+'\\\\\n'
       r'(a) 全局参数的分段幂基；(b) 转换得到的三段 Bézier 表示，两个内节点均为三重；(c) 精确去除多余节点后的七控制点表示。'+'\\\\\n'
       r'参数分点为 $0,3/10,3/5,1$；前一接点恰为 $C^2$ 连续，后一接点恰为 $C^1$ 连续，故最终分别保留单节点和双节点。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
pattern=r'\\\[\s*\{M\}_\{p\}\^\{-1\}\\left\( \{j,k\}\\right\).*?\\tag\{6\.95\}\s*\\\]'
correct=r'''\[
M_p^{-1}(j,k)=\begin{cases}
0, & 0\le j<k,\\
1/M_p(k,k), & j=k,\\
-\dfrac{\sum_{i=k}^{j-1}M_p(j,i)M_p^{-1}(i,k)}{M_p(j,j)}, & k<j\le p.
\end{cases} \tag{6.95}
\]'''
s,n=re.subn(pattern,lambda m:correct,s,count=1,flags=re.S);assert n==1
s=s.replace('274 高级几何算法\n','',1)
s=s.replace('其次数为 \\(\\left( {3 \\times  2}\\right)\\) 曲面。','其次数为 \\(\\left( {3 \\times  2}\\right)\\)。',1)
for e in ee:assert s.count(e['replacement'])==1
f.write_text(s,encoding='utf-8')
print('Placed6.20 three stages together; repaired6.95 inverse recurrence after exact degree1..8 verification.')
