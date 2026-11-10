"""Group6.13's three panels and replace truncated knot/weight lists by exact values."""
from fractions import Fraction as F
import json
import image_tex as p
d=p.load();es=[next(e for e in d['images'] if e['tex']=='image_tex/ch06/'+name) for name in ('fig_6_14.tex','fig_6_15.tex')]
assert all(e['applied'] for e in es)
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8')
start=s.index('图 6.13a 到');end=s.index('表面公式是相似的。',start);old=s[start:end]
assert all(old.count(e['replacement'])==1 for e in es)
report=json.loads((p.ROOT/'image_tex/build/rational-reparameterization-check.json').read_text(encoding='utf-8'))
def tex(x):
    x=F(x)
    if x.denominator==1:return str(x.numerator)
    sign='-' if x<0 else '';return sign+r'\frac{'+str(abs(x.numerator))+'}{'+str(x.denominator)+'}'
def listing(xs):return r'\left\{'+','.join(map(tex,xs))+r'\right\}'
text=('图 6.13 展示同一代表性六点控制多边形上的三组有理重参数化。原三次曲线的节点向量为\n\n'
      r'\['+'\n'+r'U=\{0,0,0,0,\tfrac3{10},\tfrac7{10},1,1,1,1\}.'+'\n'+r'\]'+'\n\n'
      '(a)、(b)的原权重均为一，(c)的原权重为 $\\{1,1/2,2,3,1/2,1\\}$。三组均保持控制点不变，并将节点映射到新的参数区间。由式(6.57)得到的新节点及权重如下，使用精确分数表示：\n\n')
formulas=[r'\frac{2u+1}{3u+2}',r'\frac{2u}{3u+1}',r'\frac{2u-1}{3u+2}']
for panel,formula in zip(report['panels'],formulas):
    letter=panel['panel'];K=panel['new_knots'];W=panel['new_weights']
    text+='('+letter+') $g(u)='+formula+r'$, $s\in['+tex(K[0])+','+tex(K[-1])+']$。\n\n'
    text+=r'\['+'\n'+r'\begin{aligned}'+'\n'+r'S_{'+letter+'}&='+listing(K)+r',\\'+'\n'+r'\bar W_{'+letter+'}&='+listing(W)+'.\n'+r'\end{aligned}'+'\n'+r'\]'+'\n\n'
text+=('\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'
       '\\begin{minipage}[c]{12cm}\n\\centering\n'+es[0]['replacement']+'\n\\end{minipage}\\hspace{.6cm}\n'
       '\\begin{minipage}[c]{24cm}\n\\centering\n'+es[1]['replacement']+'\n\\end{minipage}\n'
       '\\par\\smallskip\n图 6.13. 三组分式线性映射下的有理重参数化；相同控制点构成的多边形保持不变。\\\\\n'
       r'$+$ 表示原区间内的等步长 $u$ 采样，$\square$ 表示各自新区间内的等步长 $s$ 采样，步长均为对应区间长度的 $1/20$。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s[:start]+text+s[end:];assert all(s.count(e['replacement'])==1 for e in es)
f.write_text(s,encoding='utf-8');print('Grouped6.13 in one consistent row; replaced three truncated knot/weight lists by exact computed fractions.')
