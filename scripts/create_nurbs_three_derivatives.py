"""Fig4.7: exact rational cubic derivatives and the three stated display scales."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
from bspline_math import add,derivative,evaluate
from native_bspline import segments,check,de_boor,point,cubic_path
from rational_geometry import approximate,project
from nurbs46_data import K,P,homogeneous,rational

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch04/fig_4_07.tex';assert not target.exists()
w3=F(1,2);u0=F(1,2);scales=(F(2,5),F(2,25),F(3,100))
families=[];k,p,c=K,3,homogeneous(w3);exact=0
for order in range(4):
    segs=segments(k,c,p);exact+=check(k,c,p,segs);families.append((k,c,p,segs))
    if p:
        c=tuple(tuple(p*(c[i+1][d]-c[i][d])/(k[i+p+1]-k[i+1]) for d in range(3)) for i in range(len(c)-1))
        k,p=k[1:-1],p-1
def quotient_jet(u):
    h=[de_boor(k,c,p,u) for k,c,p,_ in families];jet=[]
    for order in range(4):
        jet.append(tuple((h[order][d]-sum(F(comb(order,i))*h[i][-1]*jet[order-i][d] for i in range(1,order+1)))/h[0][-1] for d in range(2)))
    return jet
def multiply(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,v in enumerate(a):
        for j,w in enumerate(b):out[i+j]+=v*w
    return tuple(out)
def scalar(a,c):return tuple(v*c for v in a)
comparisons=0
for seg in families[0][3]:
    A=seg['power'][:2];W=seg['power'][2];dW=derivative(W);symbolic=[A]
    # Independently differentiate A_k/W^(k+1) symbolically; this does not use
    # lower-order projected CK values from the algorithm above.
    for order in range(3):
        symbolic.append(tuple(add(multiply(derivative(a),W),scalar(multiply(a,dW),-(order+1))) for a in symbolic[-1]))
    us=[seg['a']+(seg['b']-seg['a'])*F(j,21) for j in range(21)]
    if seg['a']<=u0<seg['b']:us.append(u0)
    if seg['b']==1:us.append(F(1))
    for u in us:
        jet=quotient_jet(u);ww=evaluate(W,u);assert ww>0
        for order in range(4):
            assert jet[order]==tuple(evaluate(a,u)/ww**(order+1) for a in symbolic[order]);comparisons+=1
values=quotient_jet(u0)
assert values==[(F(250,49),F(180,49)),(F(27612,2401),F(-864,2401)),
                (F(5522256,117649),F(-8221824,117649)),(F(-170906976,5764801),F(-1188331776,5764801))]
assert values[0]==rational(u0,w3)[0]
lines=['% Fig4.7: same representative six controls and thirds cubic knots as Fig4.6.',
       '% w3=1/2, others1; derivatives evaluated exactly at u=1/2.',
       '% Three arrows scale Cprime by2/5, Csecond by2/25, Cthird by3/100, as the text states.',
       '% Recursive homogeneous derivatives + projected quotient recurrence independently checked against symbolic rational differentiation.',
       '% Native cubic curve paths are certified within0.0001cm; no scan outlines.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\path[use as bounding box] (-1.1,-4.5) rectangle (12.5,5.3);']
for i,p in enumerate(P):lines.append(r'\coordinate(P'+str(i)+') at '+point(p)+';')
lines.append(r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4)--(P5);')
paths=0;maximum=F(0)
for seg in families[0][3]:
    for a in approximate(seg['bern']):
        lines.append(cubic_path(a));paths+=1;maximum=max(maximum,a['certified_l1_error'])
for seg in families[0][3][:-1]:lines.append(r'\fill '+point(project(seg['bern'][-1]))+' circle[radius=1.5pt];')
endpoints=[]
for order,scale in enumerate(scales,1):
    end=tuple(values[0][d]+scale*values[order][d] for d in range(2));endpoints.append(end)
    anchor=['below right','below right','below left'][order-1]
    lines += [r'\draw[book axis] '+point(values[0])+'--'+point(end)+';',
              r'\node['+anchor+'=5pt] at '+point(end)+r' {$\mathbf C^{('+str(order)+r')}\!\left(\frac12\right)$};']
for i,pos in enumerate(['below left','below','above left','above','right','below right']):
    lines += [r'\node[book point] at (P'+str(i)+') {};',r'\node['+pos+'=5pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};']
lines += [r'\node[book point] at '+point(values[0])+' {};',r'\node at (10.3,4.4) {$w_3=\frac12$};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/nurbs-three-derivatives-check.json').write_text(json.dumps({
    'figure':'4.7','shared_controls':'nurbs46_data.py; same six-control example as4.6',
    'knots':list(map(str,K)),'w3':str(w3),'parameter':str(u0),
    'exact_homogeneous_checks_all_four_orders':exact,'quotient_vs_independent_symbolic_vectors':comparisons,
    'point_and_derivatives':[[str(v) for v in c] for c in values],
    'arrow_display_scales':list(map(str,scales)),'displayed_arrow_endpoints':[[str(v) for v in c] for c in endpoints],
    'native_cubic_curve_paths':paths,'maximum_certified_l1_curve_error_cm':str(maximum)},indent=2)+'\n')
print(f'PASS:{exact} homogeneous checks over four derivative orders,{comparisons} exact quotient/symbolic vector comparisons; three separately scaled arrows verified,{paths} native curve pieces.')
