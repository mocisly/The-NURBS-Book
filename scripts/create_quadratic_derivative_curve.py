"""Second original piece of Fig3.16: exact quadratic first-derivative curve."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point,cubic_path
from cubic_derivative_data import q,dc,at,verify

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_17.tex'
assert not target.exists()
report=verify()
lines=['% Printed Fig3.16(b), second original piece; source index17 is not Fig3.17.',
       '% Q controls computed from Fig3.16(a), Eq3.4, exact same underlying data.',
       '% Quadratic derivative with a corner at3/5, interpolating Q3.',
       '% Coordinates shown at1/3 scale as stated in text; native paths, no tracing.',
       r'\begin{tikzpicture}[book line,x=.3333333333cm,y=.3333333333cm]',
       r'\draw[book axis] (0,0)--(20,0) node[right=4pt] {$x$};',
       r'\draw[book axis] (0,0)--(0,12) node[above=4pt] {$y$};']
for i,p in enumerate(q): lines.append(r'\coordinate (Q'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] '+'--'.join('(Q'+str(i)+')' for i in range(6))+';')
for i in range(6): lines.append(r'\draw[book grid,-{Stealth[length=5pt]}] (0,0)--(Q'+str(i)+');')
for seg in dc: lines.append(cubic_path(seg))
v=at(dc,F(1,5))
lines += [r'\draw[book axis,dashed] (0,0)--'+point(v)+';',
          r"\node at (4.5,5) {$\mathbf C'\!\left(\frac15\right)$};",
          r'\foreach \i in {0,...,5} \node[book point] at (Q\i) {};']
for seg in dc[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
for i,pos in enumerate(['above right','right','left','below right','below right','above right']):
    lines.append(r'\node['+pos+'=5pt] at (Q'+str(i)+r') {$\mathbf Q_{'+str(i)+'}$};')
lines += [r'\node at (10,-12) {(b)};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
report['source17_is_printed_panel']='3.16(b)'
(root/'image_tex/build/quadratic-derivative-curve-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: shared exact derivative identity, quadratic corner and full1/3-scaled Q geometry; created3.16b.')
