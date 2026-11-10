"""Fig3.8: same ten controls, ninth-degree Bezier vs quadratic B-spline."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
from native_bspline import segments,check,point,cubic_path,number

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_08.tex'
assert not target.exists()
controls=((0,0),(1,F(3,2)),(F(3,2),0),(3,3),(5,F(27,10)),(6,-3),(8,0),(9,F(-3,2)),(11,2),(12,F(5,4)))
high=(F(0),)*10+(F(1),)*10
low=(F(0),)*3+tuple(F(i,8) for i in range(1,8))+(F(1),)*3
high_segs=segments(high,controls,9);low_segs=segments(low,controls,2)
count=check(high,controls,9,high_segs)+check(low,controls,2,low_segs)
assert high_segs[0]['bern']==controls
def bernstein(d):
    return '+'.join('('+number(p[d])+')*'+str(comb(9,i))+'*x^'+str(i)+'*(1-x)^'+str(9-i) for i,p in enumerate(controls) if p[d])
lines=['% Fig3.8: identical representative ten-control polygon in both panels.',
       '% (a) ninth-degree Bezier; (b) quadratic, seven internal knots i/8.',
       '% High-degree curve evaluated directly in stable Bernstein form, no outline tracing.',
       r'\begin{tikzpicture}[book line]',
       r'\begin{axis}[at={(0,9cm)},anchor=south west,scale only axis,width=12cm,height=6cm,',
       r'xmin=0,xmax=12,ymin=-3,ymax=3,axis lines=none,ticks=none,clip=false]',
       r'\addplot[book line,no marks,samples=241,domain=0:1] ({'+bernstein(0)+'},{'+bernstein(1)+'});']
pos=['below left','above left','below right','above left','above right','below','above left','below right','above','below right']
for i,p in enumerate(controls): lines.append(r'\coordinate (A'+str(i)+') at (axis cs:'+','.join(map(number,p))+');')
lines.append(r'\draw[book grid] '+'--'.join('(A'+str(i)+')' for i in range(10))+';')
for i in range(10): lines += [r'\node[book point] at (A'+str(i)+') {};',r'\node['+pos[i]+'=4pt] at (A'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};']
lines += [r'\end{axis}',r'\node at (6cm,8cm) {(a)};',r'\begin{scope}[x=1cm,y=1cm,yshift=3cm]']
for i,p in enumerate(controls): lines.append(r'\coordinate (B'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] '+'--'.join('(B'+str(i)+')' for i in range(10))+';')
for seg in low_segs: lines.append(cubic_path(seg))
for i in range(10): lines += [r'\node[book point] at (B'+str(i)+') {};',r'\node['+pos[i]+'=4pt] at (B'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};']
lines += [r'\end{scope}',r'\node at (6cm,-1cm) {(b)};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/degree-comparison-check.json').write_text(json.dumps({'figure':'3.8',
    'representative_controls':[[str(v) for v in p] for p in controls],
    'high_degree':9,'low_degree':2,'high_knots':list(map(str,high)),'low_knots':list(map(str,low)),
    'exact_curve_checks':count,'identical_control_polygons':True,'high_curve_equals_bernstein':True,
    'low_C1_joins':7},indent=2)+'\n')
print(f'PASS: {count} exact curve checks, identical polygons, Bernstein equivalence and quadratic C1 joins.')
