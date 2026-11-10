"""Draw printed Fig2.9 from the clamped cubic knot vector read from its axes."""
from pathlib import Path
from fractions import Fraction as F
from bspline_math import piece,evaluate,derivative,expression

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch02/fig_2_11.tex'
assert not target.exists()
knots=(0,0,0,0,2,4,6,8,8,8,8)
lines=['% Printed Fig2.9: cubic functions and their first derivatives.',
       '% U=(0,0,0,0,2,4,6,8,8,8,8), inferred from axis/supports in original.',
       '% Exact rational Cox-de Boor polynomials; check_cubic_basis.py validates geometry.',
       r'\begin{tikzpicture}']

def value(i,x,d=False):
    x=F(str(x));s=next(s for s in (3,4,5,6) if knots[s]<=x<knots[s+1])
    c=piece(knots,i,3,s)
    return float(evaluate(derivative(c) if d else c,x))

for d in (False,True):
    shift=0 if d else 9
    height='7cm' if d else '5cm'
    yrange='ymin=-1.75,ymax=1.95,ytick={-1,1}' if d else 'ymin=0,ymax=1.35,ytick={1}'
    lines += [r'\begin{scope}[yshift='+str(shift)+'cm]',
              r'\begin{axis}[scale only axis,width=14cm,height='+height+',',
              r'axis x line=middle,axis y line=left,xmin=-.3,xmax=9.2,'+yrange+',',
              r'xtick={0,2,4,6,8},'+(r'xticklabels={0,2,{},{},8},' if d else '')+r'xlabel={$u$},tick align=outside,axis line style={-{Stealth}},clip=false]']
    for i in range(7):
        for span in (3,4,5,6):
            c=piece(knots,i,3,span)
            if d: c=derivative(c)
            if not any(c): continue
            a,b=knots[span:span+2]
            shorten=',shorten >=1.5pt' if not d and i==6 and b==8 else ''
            lines.append(r'\addplot[book line,no marks,samples=41,domain='+f'{a}:{b}'+shorten+'] {'+expression(c)+'};')
    # Endpoint multiplicities (4) are encoded by clustered short ticks.
    lines += [r'\pgfplotsinvokeforeach{-.09,-.03,.03,7.91,7.97,8.03}{',
              r'\draw[book grid] (axis cs:#1,-.025)--(axis cs:#1,.025);}']
    if not d:
        for i in range(7):
            # Label a sampled maximum, without altering the analytic curve.
            candidates=[(value(i,F(k,100)),k/100) for k in range(800)]
            y,x=max(candidates)
            lines.append(r'\node[above=5pt] at (axis cs:'+f'{x:.5f},{y:.8f}'+') {$N_{'+f'{i},3'+'}$};')
        lines.append('% Right endpoint follows P2.8/FindSpan: N6,3(8)=1.')
        lines.append(r'\fill (axis cs:8,1) circle[radius=1.5pt];')
        # Final endpoint follows the book's clamped endpoint convention.
        lines.append(r'\node[above=5pt] at (axis cs:8,1) {$N_{6,3}$};')
        # N6 maximum search approaches8; replace that duplicate label with exact-limit label.
        lines=[line for line in lines if not ('N_{6,3}' in line and '7.99000' in line)]
    else:
        lines.append(r'\node[above=3pt] at (axis cs:4,0) {$4$};')
        lines.append(r'\node[above=5pt] at (axis cs:6,0) {$6$};')
        positions=[(0,.15,.55,-1.5),(1,.15,.85,1.7),(2,1.2,1.65,.7),
                   (3,3,3.1,.6),(4,4.8,5.3,.6),(5,7.7,7.1,-1.5),(6,7.85,7.75,1.7)]
        for i,x,tx,ty in positions:
            y=value(i,x,True)
            lines += [r'\node (lab'+str(i)+') at (axis cs:'+f'{tx},{ty}'+r") {$N'_{"+f'{i},3'+'}$};',
                      r'\draw[book grid,-{Stealth[length=4pt]}] (lab'+str(i)+')--(axis cs:'+f'{x},{y:.8f}'+');']
    lines += [r'\end{axis}',r'\node at (7cm,-.9cm) {'+('(b)' if d else '(a)')+'};',r'\end{scope}']
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(target)
