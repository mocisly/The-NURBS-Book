"""Fig5.42: invariant cubic refinement permits a certified quadratic fit."""
from pathlib import Path
from fractions import Fraction as F
from math import ceil,sqrt
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from bspline_math import derivative,evaluate
from knot51_data import insert
from spline_degree_reduction import reduce_spline

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_63.tex';assert not target.exists()
U=(F(0),)*4+(F('.3'),)*2+(F('.5'),)*2+(F('.7'),)*2+(F(1),)*4
P=tuple(tuple(map(F,pt)) for pt in [(0,0),(3,0),(3,4),(0,4),(0,8),(8,8),(8,4),(5,4),(5,0),(8,0)])
Kc,Qc,coarse=reduce_spline(U,P,3)
K,R=U,P
for t in ('.15','.15','.4','.4','.5','.6','.6','.85','.85'):K,R,_=insert(K,R,3,F(t))
assert K==(F(0),)*4+tuple(F(t) for t in ('.15','.15','.3','.3','.4','.4','.5','.5','.5','.6','.6','.7','.7','.85','.85'))+(F(1),)*4
Kr,Qr,refined=reduce_spline(K,R,3);assert len(P)==10 and len(R)==19 and len(Qr)==11
ss=segments(U,P,3);fine=segments(K,R,3);checks=check(U,P,3,ss)+check(K,R,3,fine)
for s in fine:
    old=next(o for o in ss if o['a']<=s['a'] and o['b']>=s['b']);assert old['power']==s['power']
invariance=0
for i in range(401):
    u=F(i,400);assert de_boor(U,P,3,u)==de_boor(K,R,3,u);invariance+=1
for k,q in [(Kc,Qc),(Kr,Qr)]:checks+=check(k,q,2,segments(k,q,2))
# On a coarse span, any quadratic annihilates these four weighted samples.
# Therefore ||-C(0)+2C(1/4)-2C(3/4)+C(1)|| / 6 is a rigorous
# lower bound for EVERY quadratic approximation on that span.
abscissae=(F(0),F(1,4),F(3,4),F(1));weights=(-1,2,-2,1)
assert all(sum(w*t**k for t,w in zip(abscissae,weights))==0 for k in range(3))
lower=[]
for s in ss:
    samples=[de_boor(U,P,3,s['a']+(s['b']-s['a'])*t) for t in abscissae]
    D=tuple(sum(w*pt[d] for pt,w in zip(samples,weights)) for d in range(2))
    lower.append(sum(x*x for x in D)/36)
bound=F(refined['certified_whole_curve_L1_error_bound']);tol=F(ceil(bound*100),100)
lower_squared=max(lower)
print('Refined certified upper:',float(bound),'universal coarse lower:',sqrt(float(lower_squared)),'TOL:',float(tol),flush=True)
assert lower_squared>tol**2
quad=segments(Kr,Qr,2);left=next(s for s in quad if s['b']==F('.5'));right=next(s for s in quad if s['a']==F('.5'))
assert all(evaluate(a,F('.5'))==evaluate(b,F('.5')) for a,b in zip(left['power'],right['power']))
assert any(evaluate(derivative(a),F('.5'))!=evaluate(derivative(b),F('.5')) for a,b in zip(left['power'],right['power']))
lines=['% Representative cubic; exact invariant refinement and certified quadratic fit.',
       '% Coarse-space failure proven for ANY quadratic via an annihilating four-point functional.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.8,-1.3) rectangle (20.3,8.8);']
for j,controls in enumerate((P,R)):
    lines.append(r'\begin{scope}[xshift='+str(j*11.5)+'cm]')
    for pt in controls:
        assert F('-.7')<=pt[0]<=F('8.7') and F('-.6')<=pt[1]<=F('8.6')
    lines.append(r'\draw[book grid] '+'--'.join(map(point,controls))+';')
    for s in ss:lines.append(cubic_path(s))
    if j:
        for pt in Qr:assert F('-.7')<=pt[0]<=F('8.7') and F('-.6')<=pt[1]<=F('8.6')
        lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,Qr))+';')
        for s in quad:lines.append(cubic_path(s,'book line,dashed'))
        for pt in Qr:lines.append(r'\node[rectangle,draw,inner sep=1.5pt] at '+point(pt)+' {};')
    for pt in controls:lines.append(r'\draw '+point(pt)+r' circle[radius=1.7pt];')
    lines.append(r'\node at (4,-.75) {('+chr(97+j)+r') $p='+(r'3,\quad N=10' if j==0 else r'2,\quad N=11')+'$};')
    lines.append(r'\end{scope}')
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/refined-degree-reduction-check.json').write_text(json.dumps({
    'figure':'5.42','original_knots':list(map(str,U)),'refined_knots':list(map(str,K)),
    'quadratic_knots':list(map(str,Kr)),'representative_controls':[[str(x) for x in pt] for pt in P],
    'refined_controls':[[str(x) for x in pt] for pt in R],'quadratic_controls':[[str(x) for x in pt] for pt in Qr],
    'coarse_reduction':coarse,'refined_reduction':refined,'chosen_tolerance':str(tol),
    'every_coarse_quadratic_uniform_error_lower_bound_squared':str(lower_squared),
    'coarse_impossibility_proof':'four weights(-1,2,-2,1) at local t(0,1/4,3/4,1) annihilate all quadratics; vector norm /6 lower-bounds uniform Euclidean error',
    'refined_whole_parameter_L1_upper_bound':str(bound),'strict_coarse_lower_above_tolerance_and_refined_upper_below_tolerance':True,
    'native_checks':checks,'exact_refinement_invariance_points':invariance,
    'quadratic_curve_at_half_is_C0_but_not_C1':True,'original_curve_C1_at_half':True},indent=2)+'\n')
print(f'PASS:{checks} native checks,{invariance} refinement comparisons; universal coarse quadratic obstruction, refined fit withinTOL; midpoint tangent break verified.')
