"""7.23: exact conic, tangent data and central projection P1-P-Q."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point,cubic_path
from rational_geometry import approximate,evaluate,project
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_28.tex')['applied']
P0=(F(0),F(0));P1=(F(2),F(4));P2=(F(5),F(1));w=F(3,5);u=F(2,5)
H=tuple(tuple(ww*x for x in p)+(ww,) for p,ww in zip((P0,P1,P2),(F(1),w,F(1))))
P=project(evaluate(H,u));L=tuple(tuple(ww*x for x in p)+(ww,) for p,ww in zip((P0,P1,P2),(F(1),F(0),F(1))))
Q=project(evaluate(L,u));assert P==(F(172,101),F(164,101)) and Q==(F(20,13),F(4,13))
assert (P1[0]-P[0])*(Q[1]-P[1])==(P1[1]-P[1])*(Q[0]-P[0])
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
v=tuple(x-y for x,y in zip(P1,P));a=tuple(x-y for x,y in zip(P,P0));b=tuple(x-y for x,y in zip(P,P2))
recovered=((1-u)**2*dot(a,v)+u*u*dot(b,v))/(2*u*(1-u)*dot(v,v));assert recovered==w
left2=sum((x-y)**2 for x,y in zip(P0,Q));right2=sum((x-y)**2 for x,y in zip(Q,P2));assert left2/right2==(u/(1-u))**4
T0=tuple(2*w*(x-y) for x,y in zip(P1,P0));T2=tuple(2*w*(x-y) for x,y in zip(P2,P1))
for i in range(101):
    t=F(i,100);c=project(evaluate(H,t));ll=project(evaluate(L,t))
    assert (c[0]-P1[0])*(ll[1]-P1[1])==(c[1]-P1[1])*(ll[0]-P1[0])
paths=approximate(H,F(1,200000))
lines=['% Representative exact rational conic: P0(0,0),P1(2,4),P2(5,1),w1=3/5,u=2/5.',
       '% Central projection and equations7.37-7.39 verified exactly, not traced.',
       r'\begin{tikzpicture}[book line,x=2.1cm,y=2.1cm]',r'\path[use as bounding box] (-.7,-1) rectangle (7,4.7);',
       r'\draw[book grid,dashed] '+point(P0)+'--'+point(P1)+'--'+point(P2)+'--cycle;',
       r'\draw[book grid,dashed] '+point(P1)+'--'+point(Q)+';']
lines.extend(cubic_path(s) for s in paths)
end0=tuple(x+F(2,5)*v for x,v in zip(P0,T0));end2=tuple(x+F(2,5)*v for x,v in zip(P2,T2))
lines += [r'\draw[book axis] '+point(P0)+'--'+point(end0)+r' node[pos=.65,left=7pt] {$\mathbf T_0$};',
          r'\draw[book axis] '+point(P2)+'--'+point(end2)+r' node[pos=.55,above right=6pt] {$\mathbf T_2$};']
for p,label,anchor in [(P0,r'\mathbf P_0','below left'),(P1,r'\mathbf P_1','above right'),(P2,r'\mathbf P_2','above right'),(P,r'\mathbf P','above left'),(Q,r'\mathbf Q','below')]:
    lines.append(r'\draw '+point(p)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$'+label+'$};')
for a,b,label in [(P0,Q,r'u^2'),(Q,P2,r'(1-u)^2')]:
    mid=tuple((x+y)/2 for x,y in zip(a,b));lines.append(r'\node[above=6pt] at '+point(mid)+' {$'+label+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch07/fig_7_28.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/conic-point-construction-check.json').write_text(json.dumps({'figure':'7.23','representative_controls':[[str(x) for x in p] for p in (P0,P1,P2)],'weight':str(w),'u':str(u),'point_P':list(map(str,P)),'point_Q':list(map(str,Q)),'recovered_weight_equation7_39':str(recovered),'distance_ratio_equation7_38_exact':True,'central_projection_identity_checks':101,'exact_endpoint_tangents':[list(map(str,T0)),list(map(str,T2))],'native_L1_error':str(max(s['certified_l1_error'] for s in paths))},indent=2)+'\n')
print('PASS:101exact central-projection identities, chord distance ratio, recovered weight3/5 and endpoint tangents.')
