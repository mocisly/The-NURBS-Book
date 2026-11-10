"""Fig3.2: exact cubic basis pieces and their matching native Bezier segments."""
from fractions import Fraction as F
from pathlib import Path
from math import comb
import json
from bspline_math import piece,evaluate,derivative,compose_affine,expression,basis

root=Path(__file__).resolve().parents[1]
target=root/'image_tex/ch03/fig_3_02.tex'
assert not target.exists(), 'Do not overwrite a reviewed drawing'
knots=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
controls=((0,0),(4,0),(4,4),(8,4),(10,0),(7,-3),(4,F(-3,2)))
spans=range(3,7)
curves={}
beziers={}
checks=0
for s in spans:
    a,b=knots[s:s+2]
    polys=[piece(knots,i,3,s) for i in range(7)]
    curves[s]=tuple(tuple(sum((polys[i][k] if k<len(polys[i]) else 0)*controls[i][d] for i in range(7)) for k in range(4)) for d in range(2))
    local=[compose_affine(c,a,b-a) for c in curves[s]]
    beziers[s]=tuple(tuple(sum((local[d][k] if k<len(local[d]) else 0)*F(comb(j,k),comb(3,k)) for k in range(j+1)) for d in range(2)) for j in range(4))
    for k in range(101):
        t=F(k,101);u=a+(b-a)*t
        weights=[evaluate(c,u) for c in polys]
        assert weights==[basis(knots,i,3,u) for i in range(7)]
        assert min(weights)>=0 and sum(weights)==1
        q=[list(pt) for pt in beziers[s]]
        for r in range(3):
            q=[[q[i][d]*(1-t)+q[i+1][d]*t for d in range(2)] for i in range(len(q)-1)]
        assert tuple(q[0])==tuple(evaluate(c,u) for c in curves[s])
        checks+=1
for s in range(3,6):
    u=knots[s+1]
    for d in range(2):
        left,right=curves[s][d],curves[s+1][d]
        for order in range(3):
            assert evaluate(left,u)==evaluate(right,u)
            left,right=derivative(left),derivative(right)
knot_points=[tuple(evaluate(c,knots[s+1]) for c in curves[s]) for s in range(3,6)]
assert knot_points==[(F(14,3),F(3)),(F(23,3),F(10,3)),(F(107,12),F(-1,12))]
assert beziers[3][0]==controls[0] and beziers[6][3]==controls[-1]
def n(x):
    x=F(x)
    return f'{float(x):.9f}'.rstrip('0').rstrip('.') if x.denominator!=1 else str(x.numerator)
def pt(p): return '('+','.join(map(n,p))+')'
lines=[
    '% Fig3.2: cubic basis U=(0,0,0,0,1/4,1/2,3/4,1,1,1,1).',
    '% Control coordinates are representative (not specified by text/scan).',
    '% Exact Cox-de Boor polynomials -> cubic Bezier controls; no contour tracing.',
    '% All basis pieces and curve pieces use the same alternating span styles.',
    r'\begin{tikzpicture}[book line]',
    r'\begin{axis}[at={(0,11cm)},anchor=south west,scale only axis,width=14cm,height=5.2cm,',
    r'axis lines=left,xmin=-.015,xmax=1.1,ymin=0,ymax=1.35,',
    r'xtick={0,.25,.5,.75,1},xticklabels={$0$,$\frac14$,$\frac12$,$\frac34$,$1$},',
    r'ytick={1},tick align=outside,axis line style={-{Stealth}},clip=false]',
    r'\pgfplotsinvokeforeach{.25,.5,.75}{\draw[book grid] (axis cs:#1,0)--(axis cs:#1,1);}'
]
for i in range(7):
    for s in spans:
        c=piece(knots,i,3,s)
        if not any(c): continue
        a,b=knots[s:s+2]
        style=',dashed' if (s-3)%2 else ''
        lines.append(r'\addplot[book line,no marks,samples=51,domain=0:1'+style+'] ({'+n(a)+'+'+n(b-a)+'*x},{'+expression(compose_affine(c,a,b-a))+'});')
lines += [
    r'\node[above right=4pt] at (axis cs:0,1) {$N_{0,3}$};',
    r'\node[above left=4pt] at (axis cs:1,1) {$N_{6,3}$};',
    r'\fill (axis cs:1,1) circle[radius=1.5pt];',
    r'\node[above left=3pt] at (axis cs:1.1,0) {$u$};',
    r'\node[above=4pt] at (axis cs:.112,.6) {$N_{1,3}$};',
    r'\node[above=4pt] at (axis cs:.888,.6) {$N_{5,3}$};',
    r'\node (n2) at (axis cs:.33,.87) {$N_{2,3}$};',
    r'\draw[book grid,-{Stealth[length=4pt]}] (n2.south)--(axis cs:.277,.595);',
    r'\node (n3) at (axis cs:.555,.94) {$N_{3,3}$};',
    r'\draw[book grid,-{Stealth[length=4pt]}] (n3.south)--(axis cs:.51,.665);',
    r'\node (n4) at (axis cs:.67,.87) {$N_{4,3}$};',
    r'\draw[book grid,-{Stealth[length=4pt]}] (n4.south)--(axis cs:.723,.595);',
    r'\pgfplotsinvokeforeach{-.008,.008,.992,1.008}{\draw[book grid] (axis cs:#1,-.025)--(axis cs:#1,.025);}',
    r'\end{axis}',
    r'\node at (6.8cm,9.8cm) {(a)};',
    r'\begin{scope}[xshift=2cm,yshift=4cm,x=1cm,y=1cm]'
]
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+pt(p)+';')
lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4)--(P5)--(P6);')
for s in spans:
    q=beziers[s]
    lines.append(r'\draw'+('[dashed]' if (s-3)%2 else '')+' '+pt(q[0])+' .. controls '+pt(q[1])+' and '+pt(q[2])+' .. '+pt(q[3])+';')
for p in knot_points: lines.append(r'\fill '+pt(p)+' circle[radius=1.7pt];')
lines.append(r'\foreach \i in {0,...,6} \node[book point] at (P\i) {};')
for i,pos in enumerate(['below left','below','above left','above right','right','below','below left']):
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines += [r'\end{scope}',r'\node at (6.8cm,0cm) {(b)};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/piecewise-curve-check.json').write_text(json.dumps({
    'figure':'3.2','knots':list(map(str,knots)),
    'representative_controls':[[str(v) for v in p] for p in controls],
    'exact_piece_vs_recurrence_and_decasteljau_points':checks,
    'C2_joins_verified':3,'knot_points':[[str(v) for v in p] for p in knot_points],
    'endpoint_interpolation':True},indent=2)+'\n')
print(f'PASS: {checks} exact basis/curve comparisons, C2 joins, all knot points and endpoints.')
