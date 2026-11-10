"""Place6.15 beside6.58 and state the exact cube-root mapping before rounded lists."""
from fractions import Fraction as F
from decimal import Decimal,localcontext
import json,re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch06/fig_6_19.tex');assert e['applied']
f=p.ROOT/'chapter/6.tex';s=f.read_text(encoding='utf-8');ref=e['replacement']
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*6\.15\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
report=json.loads((p.ROOT/'image_tex/build/equal-endpoint-weights-check.json').read_text(encoding='utf-8'))
def rounded(x):
    x=F(x)
    with localcontext() as ctx:
        ctx.prec=60;value=format(Decimal(x.numerator)/Decimal(x.denominator),'.4f').rstrip('0').rstrip('.')
    return value
def listing(xs):return r'\{'+','.join(map(rounded,xs))+r'\}'
start=s.index('选择的新区间为');end=s.index('我们在第 4 章中给出了例子',start)
text=('选择的新区间为 $[c,d]=[1/10,4/5]$。将式(6.58)中的分子与分母同除以 $\\sqrt[3]{2}$，得到精确映射\n\n'
      r'\['+'\n'+r'r=\sqrt[3]{\frac52},\qquad g(u)=\frac{\frac1{10}+\left(\frac45r-\frac1{10}\right)u}{1+(r-1)u}.'+'\n'+r'\]'+'\n\n'
      '由式(6.57)计算权重，再作共同归一化，得到以下新节点和权重（内项显示四位小数）：\n\n'
      r'\['+'\n'+r'U^{\prime}\simeq '+listing(report['new_knots'])+r',\qquad W^{\prime}\simeq '+listing(report['new_weights'])+'.\n'+r'\]'+'\n\n'
      '两端权重等于1是精确等式：未归一化的端权重分别为 $2$ 和 $5/r^3=2$。控制点和曲线形状均保持不变。\n\n')
text+=('\\begin{center}\n\\begin{minipage}{18cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n图 6.15. 按式(6.58)重参数化，使两端权重归一化为一。\\\\\n'
       r'$+$ 为 $u=i/20$ 的曲线点，$\square$ 为新区间 $[1/10,4/5]$ 内等步长 $s$ 的曲线点；控制多边形保持不变。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s[:start]+text+s[end:];assert s.count(ref)==1
f.write_text(s,encoding='utf-8');print('Placed6.15 at its endpoint-weight example; exact cube-root map and properly marked rounded data.')
