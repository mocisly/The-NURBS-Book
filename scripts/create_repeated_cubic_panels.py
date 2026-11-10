"""Printed Fig2.10: exact cubic basis functions with multiple knots."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import piece,evaluate,derivative,expression,basis

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch02/fig_2_12.tex'
assert not target.exists(), 'Refuse to overwrite an existing drawing'
knots=(0,0,0,0,2,4,4,6,6,6,8,8,8,8);spans=(3,4,6,9)
checks=0
for span in spans:
    a,b=knots[span:span+2]
    for k in range(41):
        x=F(a)+F(k,41)*(b-a)
        values=[];slopes=[]
        for i in range(10):
            c=piece(knots,i,3,span);y=evaluate(c,x)
            assert y==basis(knots,i,3,x)
            values.append(y);slopes.append(evaluate(derivative(c),x));checks+=1
        assert min(values)>=0 and sum(values)==1 and sum(slopes)==0
for left,right,knot,continuity in [(3,4,2,2),(4,6,4,1),(6,9,6,0)]:
    for i in range(10):
        a,b=piece(knots,i,3,left),piece(knots,i,3,right)
        for order in range(continuity+1):
            assert evaluate(a,F(knot))==evaluate(b,F(knot))
            a,b=derivative(a),derivative(b)
jumps={i:[evaluate(derivative(piece(knots,i,3,s)),F(6)) for s in (6,9)] for i in (5,6,7)}
assert jumps=={5:[-F(3,2),F(0)],6:[F(3,2),-F(3,2)],7:[F(0),F(3,2)]}

def value(i,x,d=False):
    x=F(str(x));s=next(s for s in spans if knots[s]<=x<knots[s+1])
    c=piece(knots,i,3,s)
    return float(evaluate(derivative(c) if d else c,x))

lines=['% Printed Fig2.10: exact functions for U=(0,0,0,0,2,4,4,6,6,6,8,8,8,8).',
       '% U inferred from labeled supports and knot multiplicities in original.',
       '% Native rational Cox-de Boor polynomial expressions; no traced coordinates.',
       '% Dashed vertical at6 is a guide, not part of a derivative graph.',r'\begin{tikzpicture}']
for d in (False,True):
    shift=0 if d else 11
    height='9cm' if d else '5.8cm'
    yrange='ymin=-1.85,ymax=2.05,ytick={-1,1}' if d else 'ymin=0,ymax=1.45,ytick={1}'
    lines += [r'\begin{scope}[yshift='+str(shift)+'cm]',
              r'\begin{axis}[scale only axis,width=14cm,height='+height+',',
              r'axis x line=middle,axis y line=left,xmin=-.3,xmax=9.4,'+yrange+',',
              r'xtick={0,2,4,6,8},'+(r'xticklabels={0,2,{},{},8},' if d else '')+
              r'xlabel={$u$},tick align=outside,axis line style={-{Stealth}},clip=false]']
    for i in range(10):
        for span in spans:
            a,b=knots[span:span+2];c=piece(knots,i,3,span)
            if d: c=derivative(c)
            if not any(c): continue
            shorten=''
            if not d and i==9 and b==8: shorten=',shorten >=1.5pt'
            if d and i in (5,6) and b==6: shorten=',shorten >=1.5pt'
            if d and i in (6,7) and a==6: shorten=',shorten <=1.5pt'
            lines.append(r'\addplot[book line,no marks,samples=41,domain='+f'{a}:{b}'+shorten+'] {'+expression(c)+'};')
    lines += [r'\pgfplotsinvokeforeach{-.09,-.03,.03,4.055,5.945,6.055,7.91,7.97,8.03}{',
              r'\draw[book grid] (axis cs:#1,-.025)--(axis cs:#1,.025);}']
    if not d:
        for i in range(4):
            y,x=max((value(i,F(k,100)),k/100) for k in range(800))
            lines.append(r'\node[above=5pt] at (axis cs:'+f'{x:.5f},{y:.8f}'+') {$N_{'+f'{i},3'+'}$};')
        leaders=[(4,4.4,4.3,.93),(5,5.2,5.25,1.12),(7,6.7,7.05,.86),(8,7.7,8.65,.28)]
        for i,x,tx,ty in leaders:
            lines += [r'\node (bas'+str(i)+') at (axis cs:'+f'{tx},{ty}'+') {$N_{'+f'{i},3'+'}$};',
                      r'\draw[book grid,-{Stealth[length=4pt]}] (bas'+str(i)+')--(axis cs:'+f'{x},{value(i,x):.8f}'+');']
        lines += [r'\node[above=5pt] at (axis cs:6,1) {$N_{6,3}$};',
                  '% Right endpoint follows P2.8/FindSpan: N9,3(8)=1.',
                  r'\fill (axis cs:8,1) circle[radius=1.5pt];',
                  r'\node[above=5pt] at (axis cs:8,1) {$N_{9,3}$};']
    else:
        lines += [r'\node[above=3pt] at (axis cs:4,0) {$4$};',
                  r'\node[below right=4pt] at (axis cs:6,0) {$6$};',
                  r'\draw[book grid,dashed] (axis cs:6,-1.5)--(axis cs:6,1.5);',
                  r'\draw (axis cs:6,1.5) circle[radius=1.5pt];',
                  r'\draw (axis cs:6,-1.5) circle[radius=1.5pt];']
        positions=[(0,.15,.6,-1.65),(1,.15,.7,1.75),(2,1.2,1.65,.72),
                   (3,2.8,2.8,.85),(4,3.9,3.8,1.25),(5,4.9,4.8,.92),
                   (6,5.8,5.45,1.8),(6,6.15,6.75,-1.65),
                   (7,6.5,7.05,.95),(8,7.8,8.55,-1.65),(9,7.85,8.55,1.75)]
        for j,(i,x,tx,ty) in enumerate(positions):
            lines += [r'\node (der'+str(j)+') at (axis cs:'+f'{tx},{ty}'+r") {$N'_{"+f'{i},3'+'}$};',
                      r'\draw[book grid,-{Stealth[length=4pt]}] (der'+str(j)+')--(axis cs:'+f'{x},{value(i,x,True):.8f}'+');']
    lines += [r'\end{axis}',r'\node at (7cm,-.9cm) {'+('(b)' if d else '(a)')+'};',r'\end{scope}']
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/repeated-cubic-check.json').write_text(json.dumps({
    'knots':knots,'exact_recurrence_comparisons':checks,
    'partition_positive_and_derivative_sum_zero':True,
    'continuity_at_2_4_6':['C2','C1','C0'],
    'derivative_limits_at_6':{i:list(map(float,v)) for i,v in jumps.items()}},indent=2)+'\n')
print(f'Created {target}; {checks} exact comparisons passed.')
