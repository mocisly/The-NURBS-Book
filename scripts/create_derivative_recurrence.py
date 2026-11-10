"""Create printed Fig2.8, using exact polynomial differentiation and recurrence."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import piece,evaluate,basis,expression,derivative,add

root=Path(__file__).resolve().parents[1]
target=root/'image_tex/ch02/fig_2_10.tex'
assert not target.exists()
# Same relative spacing 3:1:3:2 as Fig2.3; representative knots, not recovered data.
knots=tuple(F(k,5) for k in (0,3,4,7,9))
lines=['% Printed Fig2.8. Exact (2.7) derivative recurrence for a cubic basis.',
       '% Representative U=(0,3/5,4/5,7/5,9/5); relative spacing inferred from scan.',
       '% Generated from rational Cox-de Boor polynomial pieces; no traced geometry.',
       r'\begin{tikzpicture}',
       r'\begin{axis}[width=16cm,height=9cm,axis x line=middle,axis y line=left,',
       r'xmin=-.1,xmax=2.05,ymin=-1.5,ymax=1.9,',
       r'xtick={0,.6,.8,1.4,1.8},xticklabels={$u_i$,$u_{i+1}$,$u_{i+2}$,$u_{i+3}$,$u_{i+4}$},',
       r'ytick={-1,1},xlabel={$u$},axis line style={-{Stealth}},tick align=outside,clip=false]']
checks=0
for degree,index,deriv,style in [(2,0,False,'book grid'),(2,1,False,'book grid'),(3,0,False,'book line'),(3,0,True,'line width=.9pt')]:
    for span,(a,b) in enumerate(zip(knots,knots[1:])):
        c=piece(knots,index,degree,span)
        if deriv:
            c=derivative(c)
            q0=piece(knots,0,2,span);q1=piece(knots,1,2,span)
            via_rec=add(tuple(F(3)/(knots[3]-knots[0])*v for v in q0),
                        tuple(-F(3)/(knots[4]-knots[1])*v for v in q1))
            for k in range(41):
                x=a+F(k,41)*(b-a)
                assert evaluate(c,x)==evaluate(via_rec,x)
                checks+=1
        if any(c):
            lines.append(r'\addplot['+style+',no marks,samples=41,domain='+f'{float(a):.6f}:{float(b):.6f}'+'] {'+expression(c)+'};')

def value(i,p,x,d=False):
    x=F(str(x));span=next(s for s in range(4) if knots[s]<=x<knots[s+1])
    c=piece(knots,i,p,span)
    return float(evaluate(derivative(c) if d else c,x))

for name,x,y,tx,ty in [('q0',.5,value(0,2,.5),.2,.8),
                       ('c',.95,value(0,3,.95),.94,1.04),
                       ('q1',1.3,value(1,2,1.3),1.65,.7),
                       ('dc',1.3,value(0,3,1.3,True),1.65,-.95)]:
    label={'q0':r'N_{i,2}','q1':r'N_{i+1,2}','c':r'N_{i,3}','dc':r"N'_{i,3}"}[name]
    lines.append(r'\node ('+name+') at (axis cs:'+f'{tx},{ty}'+') {$'+label+'$};')
    lines.append(r'\draw[book grid,-{Stealth[length=4pt]}] ('+name+') -- (axis cs:'+f'{x},{y:.8f}'+');')
lines.extend([r'\end{axis}',r'\end{tikzpicture}'])
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/derivative-recurrence-check.json').write_text(json.dumps({
    'exact_polynomial_derivative_vs_recurrence_comparisons':checks,
    'knots':['0','3/5','4/5','7/5','9/5'],
    'native_source':'ch02/fig_2_10.tex'},indent=2)+'\n')
print(f'Created printed Fig2.8; {checks} exact derivative identity comparisons passed.')
