"""First original piece of Fig3.16: exact cubic and five tangent vectors."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point,cubic_path
from cubic_derivative_data import controls,curve,at,verify

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_16.tex'
assert not target.exists()
report=verify()
parameters=(F(0),F(1,5),F(2,5),F(3,5),F(1));labels=('0',r'\frac15',r'\frac25',r'\frac35','1')
lines=['% Printed Fig3.16(a), first of two original image pieces.',
       '% Exact caption knots; representative controls recorded in cubic_derivative_data.py.',
       '% Tangent arrows at1/3 length, consistent with the text. Native cubic paths, no tracing.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\draw[book axis] (0,0)--(8.2,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,0)--(0,4.4) node[above=4pt] {$y$};']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] '+'--'.join('(P'+str(i)+')' for i in range(7))+';')
for seg in curve: lines.append(cubic_path(seg))
for u,label in zip(parameters,labels):
    a=at(curve,u);v=at(curve,u,1);b=tuple(x+y/3 for x,y in zip(a,v))
    lines += [r'\draw[book axis'+(',dashed' if u==F(1,5) else '')+'] '+point(a)+'--'+point(b)+';',
              r'\node['+('above right' if u in (0,F(1,5),1) else 'right')+'=5pt] at '+point(b)+r" {$\mathbf C'\!\left("+label+r'\right)$};']
lines.append(r'\foreach \i in {0,...,6} \node[book point] at (P\i) {};')
for seg in curve[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
lines.append(r'\node[book point] at '+point(at(curve,F(1,5)))+' {};')
for i,pos in enumerate(['below left','above right','above','above right','below left','below left','right']):
    gap='14pt' if i==2 else '4pt'
    lines.append(r'\node['+pos+'='+gap+'] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines += [r'\node at (4.5,-2.5) {(a)};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/cubic-derivative-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(f"PASS: {report['exact_curve_checks']} exact curve checks and derivative identity; Fig3.16a created.")
