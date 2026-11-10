"""6.16: exact reflected knots/reversed controls and coincident uniform marker grids."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point,de_boor
from bspline_math import compose_affine,derivative,evaluate

root=Path(__file__).resolve().parents[1];data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/fig_6_20.tex')['applied']
U=(F(0),)*4+(F(3,10),F(13,20))+(F(1),)*4
P=((F(1),F(0)),(F(0),F(4)),(F(6),F(5)),(F(3),-F(1)),(F(9),-F(1)),(F(8),F(3)))
K=tuple(1-x for x in reversed(U));Q=tuple(reversed(P));old=segments(U,P,3);new=segments(K,Q,3)
checks=check(U,P,3,old)+check(K,Q,3,new)
for a,b in zip(old,reversed(new)):
    assert (a['a'],a['b'])==(1-b['b'],1-b['a'])
    assert all(compose_affine(c,F(1),-F(1))==d for c,d in zip(a['power'],b['power']))
for i in range(101):
    u=F(i,100);assert de_boor(U,P,3,u)==de_boor(K,Q,3,1-u)
plus=[de_boor(U,P,3,F(i,20)) for i in range(21)]
square=[de_boor(K,Q,3,F(i,20)) for i in range(21)];assert plus==list(reversed(square))
lines=['% Independent explicit representative cubic; nonsymmetric knots .3,.65 reflect to.35,.7.',
       '% Reversing controls and reflecting knots gives C_new(s)=C_old(1-s) coefficientwise.',
       '% Uniform original and reversed grids coincide as sets, with opposite traversal order.',
       r'\begin{tikzpicture}[book line,x=1.1cm,y=1.1cm]',r'\path[use as bounding box] (-1.3,-2.2) rectangle (10.5,6);',
       r'\draw[book grid] '+'--'.join(map(point,P))+';']
for a in plus:
    lines += [r'\begin{scope}[shift={'+point(a)+'}]',r'\draw[book grid] (-1.8pt,0)--(1.8pt,0) (0,-1.8pt)--(0,1.8pt);',r'\end{scope}']
for a in square:lines.append(r'\node[rectangle,draw,line width=.35pt,inner sep=1.4pt] at '+point(a)+' {};')
for i,(a,anchor) in enumerate(zip(P,('below left','above left','above','below','below right','above right'))):
    label=r'\mathbf P_'+str(i)+r'=\mathbf Q_'+str(5-i)
    lines.append(r'\draw '+point(a)+r' circle[radius=1.8pt] node['+anchor+r'=6pt] {$'+label+'$};')
arrows=[]
for u,sign,label,offset,anchor in [(F(3,20),1,r'\mathbf C(u)',(F(0),-F(7,5)),'below right'),
                                 (F(9,10),-1,r'\mathbf C(s)',(-F(9,10),F(1,10)),'above left')]:
    seg=next(s for s in old if s['a']<=u<=s['b']);C=de_boor(U,P,3,u)
    tangent=tuple(sign*evaluate(derivative(c),u) for c in seg['power']);length=sum(map(abs,tangent))
    base=tuple(x+y for x,y in zip(C,offset));tip=tuple(x+F(6,5)*t/length for x,t in zip(base,tangent))
    lines.append(r'\draw[book axis] '+point(base)+'--'+point(tip)+';')
    lines.append(r'\node['+anchor+r'=6pt] at '+point(base)+' {$'+label+'$};')
    arrows.append({'old_u':str(u),'traversal_sign':sign,'tangent':list(map(str,tangent))})
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch06/fig_6_20.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/curve-reversal-check.json').write_text(json.dumps({
    'figure':'6.16','representative_controls':[[str(x) for x in pt] for pt in P],
    'original_knots':list(map(str,U)),'reflected_knots':list(map(str,K)),
    'all_piecewise_power_coefficients_equal_under_one_minus_s':True,
    'exact_position_checks':101,'native_basis_checks':checks,
    'uniform_parameter_grids_exactly_coincident_in_reverse_order':True,
    'direction_arrows_are_translated_normalized_actual_tangents':arrows},indent=2)+'\n')
print(f'PASS:{checks} native checks,101 exact reverse-parameter identities,all global polynomial coefficients reflected exactly.')
