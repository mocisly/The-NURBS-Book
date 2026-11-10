"""Fig3.3: quadratic basis and curve, five matching polynomial intervals."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import piece,compose_affine,expression
from native_bspline import segments,check,number,point,cubic_path

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_03.tex'
assert not target.exists()
knots=(F(0),)*3+tuple(F(i,5) for i in range(1,5))+(F(1),)*3
controls=((0,0),(1,3),(5,F(7,2)),(3,-2),(9,-2),(7,F(3,2)),(10,2))
segs=segments(knots,controls,2);count=check(knots,controls,2,segs)
lines=['% Fig3.3: exact quadratic U=(0,0,0,1/5,2/5,3/5,4/5,1,1,1).',
       '% Representative controls: no numerical coordinates specified in text.',
       '% Exact quadratic pieces elevated to cubic native paths; no tracing.',
       r'\begin{tikzpicture}[book line]',
       r'\begin{axis}[at={(0,9.5cm)},anchor=south west,scale only axis,width=14cm,height=5.2cm,',
       r'axis lines=left,xmin=-.015,xmax=1.1,ymin=0,ymax=1.35,',
       r'xtick={0,.2,.4,.6,.8,1},xticklabels={$0$,$\frac15$,$\frac25$,$\frac35$,$\frac45$,$1$},',
       r'ytick={1},tick align=outside,axis line style={-{Stealth}},clip=false]',
       r'\pgfplotsinvokeforeach{.2,.4,.6,.8}{\draw[book grid] (axis cs:#1,0)--(axis cs:#1,1);}']
for i in range(7):
    for j,seg in enumerate(segs):
        a,b,s=seg['a'],seg['b'],seg['span'];c=piece(knots,i,2,s)
        if any(c): lines.append(r'\addplot[book line,no marks,samples=51,domain=0:1'+(',dashed' if j%2 else '')+'] ({'+number(a)+'+'+number(b-a)+'*x},{'+expression(compose_affine(c,a,b-a))+'});')
for i,x,y in [(0,0,1),(1,.133,.667),(2,.3,.75),(3,.5,.75),(4,.7,.75),(5,.867,.667),(6,1,1)]:
    pos='above right' if i==0 else 'above left' if i==6 else 'above'
    lines.append(r'\node['+pos+'=6pt] at (axis cs:'+f'{x},{y}'+') {$N_{'+str(i)+',2}$};')
lines += [r'\fill (axis cs:1,1) circle[radius=1.5pt];',
          r'\node[above left=3pt] at (axis cs:1.1,0) {$u$};',
          r'\pgfplotsinvokeforeach{-.008,.008,.992,1.008}{\draw[book grid] (axis cs:#1,-.025)--(axis cs:#1,.025);}',
          r'\end{axis}',r'\node at (6.8cm,8.3cm) {(a)};',
          r'\begin{scope}[xshift=2cm,yshift=3cm,x=1cm,y=1cm]']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4)--(P5)--(P6);')
for j,seg in enumerate(segs): lines.append(cubic_path(seg,'dashed' if j%2 else ''))
for seg in segs[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
lines.append(r'\foreach \i in {0,...,6} \node[book point] at (P\i) {};')
for i,pos in enumerate(['below left','above left','above right','below left','below right','above left','above right']):
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines += [r'\end{scope}',r'\node at (6.8cm,0cm) {(b)};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/quadratic-spans-check.json').write_text(json.dumps({'figure':'3.3','knots':list(map(str,knots)),
    'representative_controls':[[str(v) for v in p] for p in controls],
    'exact_recurrence_deboor_decasteljau_points':count,'C1_joins_verified':4,
    'knot_points':[[str(v) for v in s['bern'][-1]] for s in segs[:-1]]},indent=2)+'\n')
print(f'PASS: {count} exact comparisons and four C1 joins; created Fig3.3.')
