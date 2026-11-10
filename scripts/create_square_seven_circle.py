"""7.21: two exact inserted semicircles and their seven rational basis graphs."""
from fractions import Fraction as F
from pathlib import Path
import json
from native_bspline import segments,check,de_boor,point
from bspline_math import add,evaluate,derivative
from polynomial_native import multiply
from rational_geometry import project
from native_rational_basis import graphs

root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_24.tex')['applied']
U=(F(0),)*3+(F(1,4),)+(F(1,2),)*2+(F(3,4),)+(F(1),)*3
P=tuple(tuple(map(F,q)) for q in [(1,0),(1,1),(-1,1),(-1,0),(-1,-1),(1,-1),(1,0)])
W=tuple(map(F,[1,F(1,2),F(1,2),1,F(1,2),F(1,2),1]))
H=tuple(tuple(w*x for x in p)+(w,) for p,w in zip(P,W));ss=segments(U,H,2);nc=check(U,H,2,ss)
cert=[]
for s in ss:
    X,Y,Z=s['power'];res=add(add(multiply(X,X),multiply(Y,Y)),tuple(-x for x in multiply(Z,Z)))
    assert all(x==0 for x in res);cert.append({'interval':list(map(str,(s['a'],s['b']))),'exact_circle_polynomial_identity':True})
assert ss[0]['power']==ss[1]['power'] and ss[2]['power']==ss[3]['power']
def derivatives(s,u):
    h=[evaluate(c,u) for c in s['power']];dh=[evaluate(derivative(c),u) for c in s['power']];ddh=[evaluate(derivative(derivative(c)),u) for c in s['power']]
    v=tuple((dh[k]*h[-1]-h[k]*dh[-1])/h[-1]**2 for k in range(2))
    a=tuple(ddh[k]/h[-1]-h[k]*ddh[-1]/h[-1]**2-2*dh[k]*dh[-1]/h[-1]**2+2*h[k]*dh[-1]**2/h[-1]**3 for k in range(2))
    return v,a
assert derivatives(ss[1],F(1,2))[0]==derivatives(ss[2],F(1,2))[0]
assert derivatives(ss[1],F(1,2))[1]!=derivatives(ss[2],F(1,2))[1]
assert derivatives(ss[-1],F(1))[0]==derivatives(ss[0],F(0))[0]
for i in range(201):
    u=F(i,200);h=de_boor(U,H,2,u);assert h[-1]>=F(1,2)
    R=[de_boor(U,tuple((w*F(k==j),) for k,w in enumerate(W)),2,u)[0]/h[-1] for j in range(7)]
    assert min(R)>=0 and sum(R)==1 and project(h)==tuple(sum(r*p[k] for r,p in zip(R,P)) for k in range(2))
    assert sum(x*x for x in project(h))==1
lines=['% Exact Ex7.6 seven-control square circle; no contour tracing.',r'\begin{tikzpicture}[book line]',r'\begin{scope}[x=4cm,y=4cm]',
       r'\path[use as bounding box] (-1.85,-1.85) rectangle (1.95,1.65);',
       r'\draw[book axis,book grid] (-1.5,0)--(1.5,0) node[right=4pt] {$x$};',
       r'\draw[book axis,book grid] (0,-1.35)--(0,1.4) node[above=4pt] {$y$};',
       r'\draw[book grid] '+'--'.join(map(point,P))+';']
for i in range(80):
    if i%40==0:continue
    C=project(de_boor(U,H,2,F(i,80)))
    lines += [r'\begin{scope}[shift={'+point(C)+'}]',r'\draw (-1.5pt,0)--(1.5pt,0) (0,-1.5pt)--(0,1.5pt);',r'\end{scope}']
for i,(p,anchor) in enumerate(zip(P[:6],['below right','above right','above left','above left','below left','below right'])):
    label=r'\mathbf P_0=\mathbf P_6' if i==0 else r'\mathbf P_'+str(i)
    lines.append(r'\draw '+point(p)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$'+label+'$};')
lines += [r'\node at (0,-1.6) {(a)};',r'\end{scope}',r'\begin{scope}[xshift=10.2cm,yshift=-1.9cm]',
          r'\path[use as bounding box] (-.6,-1.9) rectangle (13.1,5.1);',r'\draw[book axis] (-.1,0)--(12.7,0) node[right=4pt] {$u$};',
          r'\draw[book axis] (0,0)--(0,4.7);',r'\node[left=5pt] at (0,4) {$1$};']
basis,proofs=graphs(U,W);lines+=basis
for i,u in enumerate([F(0),F(3,16),F(5,16),F(1,2),F(11,16),F(13,16),F(1)]):
    h=de_boor(U,H,2,u);v=de_boor(U,tuple((w*F(k==i),) for k,w in enumerate(W)),2,u)[0]/h[-1]
    anchor='above right' if i==0 else 'above left' if i==6 else 'above'
    lines.append(r'\node['+anchor+r'=6pt] at '+point((12*u,4*v))+' {$R_{'+str(i)+r',2}$};')
for u,label,m in [(F(0),'0',3),(F(1,4),r'\tfrac14',1),(F(1,2),r'\tfrac12',2),(F(3,4),r'\tfrac34',1),(F(1),'1',3)]:
    for k in range(m):
        x=12*u+F(7,100)*(F(k)-F(m-1,2));lines.append(r'\draw[book grid] '+point((x,-F(1,10)))+'--'+point((x,F(1,10)))+';')
    lines.append(r'\node[below=6pt] at '+point((12*u,-F(1,10)))+' {$'+label+'$};')
lines += [r'\node at (6,-1.55) {(b)};',r'\end{scope}',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_24.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/square-seven-circle-check.json').write_text(json.dumps({'figure':'7.21','controls':[[str(x) for x in q] for q in P],'weights':list(map(str,W)),'knots':list(map(str,U)),'native_checks':nc,'exact_partition_curve_and_circle_checks':201,'circle_polynomial_certificates':cert,'unchanged_global_quadratic_on_each_semicircle':True,'projected_C1_not_C2_at_half':True,'closure_C1':True,'denominator_lower_bound':'1/2','native_basis_graph_certificates':proofs},indent=2)+'\n')
print('PASS:four exact circle identities,201circle/partition checks,C1closure and half join,7certified rational bases.')
