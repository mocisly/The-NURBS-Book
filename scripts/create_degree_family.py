"""Fig3.9: five degrees on the same polygon with the text's five knot vectors."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
from native_bspline import segments,check,point,cubic_path,number

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_09.tex'
assert not target.exists()
controls=((0,0),(F(-2,5),4),(5,4),(F(23,10),-2),(F(21,2),-2),(F(17,2),2))
families={};count=0
for p in range(1,6):
    knots=(F(0),)*(p+1)+tuple(F(i,6-p) for i in range(1,6-p))+(F(1),)*(p+1)
    segs=segments(knots,controls,p);count+=check(knots,controls,p,segs)
    families[p]=(knots,segs)
assert all(s['bern']==(controls[j],controls[j+1]) for j,s in enumerate(families[1][1]))
def bernstein(points,d):
    p=len(points)-1
    return '+'.join('('+number(q[d])+')*'+str(comb(p,i))+'*x^'+str(i)+'*(1-x)^'+str(p-i) for i,q in enumerate(points) if q[d]) or '0'
lines=['% Fig3.9: p=1..5, knot vectors exactly as listed after P3.7.',
       '% Same representative six-control polygon as Figs3.4 and3.5.',
       '% Native cubic paths or Bernstein polynomial plots; no image geometry traced.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\begin{axis}[at={(-.4cm,-2cm)},anchor=south west,scale only axis,width=10.9cm,height=6cm,',
       r'xmin=-.4,xmax=10.5,ymin=-2,ymax=4,axis lines=none,ticks=none,clip=false]']
for p in (4,5):
    for seg in families[p][1]:
        points=seg['bern']
        lines.append(r'\addplot[book line,no marks,samples=101,domain=0:1] ({'+bernstein(points,0)+'},{'+bernstein(points,1)+'});')
lines.append(r'\end{axis}')
for p in (2,3):
    for seg in families[p][1]: lines.append(cubic_path(seg))
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw (P0)--(P1)--(P2)--(P3)--(P4)--(P5);')
lines.append(r'\foreach \i in {0,...,5} \node[book point] at (P\i) {};')
for i,pos in enumerate(['below left','above left','above right','below left','below right','above']):
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
for p in range(1,6): lines.append(r'\node at (1.6,'+number(F(2)-F(p-1,2))+') {$p='+str(p)+'$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/degree-family-check.json').write_text(json.dumps({'figure':'3.9',
    'representative_controls':[[str(v) for v in q] for q in controls],
    'knots_by_degree':{str(p):list(map(str,v[0])) for p,v in families.items()},
    'exact_curve_comparisons':count,'degree1_equals_polygon':True,
    'same_controls_all_degrees':True,'simple_knot_continuities_verified':True},indent=2)+'\n')
print(f'PASS: {count} exact comparisons, all five text knot vectors and shared controls.')
