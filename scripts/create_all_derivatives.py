"""Printed Fig2.11: cubic basis and its first three derivatives."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import piece,evaluate,derivative,expression,basis

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch02/fig_2_13.tex'
assert not target.exists()
# No numeric data in text: representative local spacings match the schematic.
knots=tuple(F(k,5) for k in (0,4,12,21,27))

def derive(c,k):
    for _ in range(k): c=derivative(c)
    return c

def recursive(i,p,k,x):
    if not k: return basis(knots,i,p,x)
    if k>p: return F(0)
    return (F(p,knots[i+p]-knots[i])*recursive(i,p-1,k-1,x)
            -F(p,knots[i+p+1]-knots[i+1])*recursive(i+1,p-1,k-1,x))

checks=0
for span in range(4):
    a,b=knots[span:span+2];c=piece(knots,0,3,span)
    for order in range(4):
        dc=derive(c,order)
        for k in range(41):
            x=a+F(k,41)*(b-a)
            assert evaluate(dc,x)==recursive(0,3,order,x);checks+=1
    assert not any(derive(c,4))
for span in range(3):
    for order in range(3):
        assert evaluate(derive(piece(knots,0,3,span),order),knots[span+1])==evaluate(derive(piece(knots,0,3,span+1),order),knots[span+1])

def value(x,order):
    x=F(str(x));span=next(s for s in range(4) if knots[s]<=x<knots[s+1])
    return float(evaluate(derive(piece(knots,0,3,span),order),x))

third=[derive(piece(knots,0,3,s),3)[0] for s in range(4)]
lines=['% Printed Fig2.11: N_i3 and nonzero derivatives, computed exactly.',
       '% Representative local knots (0,4/5,12/5,21/5,27/5); scan has no numeric data.',
       '% Dashed verticals are jump guides for the piecewise-constant third derivative.',
       r'\begin{tikzpicture}',
       r'\begin{axis}[scale only axis,width=14cm,height=8cm,',
       r'axis x line=middle,axis y line=left,xmin=-.35,xmax=6.2,ymin=-1.2,ymax=1.35,',
       r'xtick={0,.8,2.4,4.2,5.4},xticklabels=\empty,ytick={-1,1},',
       r'xlabel={$u$},axis line style={-{Stealth}},tick align=outside,clip=false]']
for order in range(4):
    style='book line' if order<2 else 'line width=.55pt'
    for span in range(4):
        a,b=knots[span:span+2];c=derive(piece(knots,0,3,span),order)
        shorten=',shorten <=1.5pt,shorten >=1.5pt' if order==3 else ''
        lines.append(r'\addplot['+style+',no marks,samples=41,domain='+f'{float(a):.6f}:{float(b):.6f}'+shorten+'] {'+expression(c)+'};')
        if order==3:
            for endpoint in (a,b):
                lines.append(r'\draw (axis cs:'+f'{float(endpoint):.6f},{float(c[0]):.8f}'+') circle[radius=1.5pt];')
for j,x in enumerate(knots):
    lo=third[j-1] if j else F(0);hi=third[j] if j<4 else F(0)
    lines.append(r'\draw[book grid,dashed] (axis cs:'+f'{float(x):.6f},{float(lo):.8f}'+')--(axis cs:'+f'{float(x):.6f},{float(hi):.8f}'+');')
for x,label,anchor in [(0,'u_i','below left'),(.8,'u_{i+1}','below right'),(2.4,'u_{i+2}','below left'),(4.2,'u_{i+3}','below left'),(5.4,'u_{i+4}','below right')]:
    lines.append(r'\node['+anchor+'=4pt] at (axis cs:'+f'{x},0'+') {$'+label+'$};')
labels=[(0,2.5,2.85,.25),(1,3.4,3.5,-1.02),(2,4.5,5.3,.55),(3,3.3,3.45,1.08)]
for order,x,tx,ty in labels:
    prime="'"*order
    lines += [r'\node (d'+str(order)+') at (axis cs:'+f'{tx},{ty}'+') {$N'+prime+r'_{i,3}$};',
              r'\draw[book grid,-{Stealth[length=4pt]}] (d'+str(order)+')--(axis cs:'+f'{x},{value(x,order):.8f}'+');']
lines += [r'\end{axis}',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/all-derivatives-check.json').write_text(json.dumps({
    'representative_knots':list(map(str,knots)),
    'exact_derivative_recurrence_checks':checks,'C2_at_all_interior_knots':True,
    'fourth_derivative_zero_in_every_span':True,
    'third_derivative_values':list(map(str,third))},indent=2)+'\n')
print(f'{checks} exact checks passed; third derivative levels: {third}')
