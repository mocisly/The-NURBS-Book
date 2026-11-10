"""7.24: exact oblique half ellipse with a nonzero zero-weight control vector."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point,cubic_path
from rational_geometry import approximate,evaluate,project
from polynomial_native import multiply
from bspline_math import add
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch07/fig_7_29.tex')['applied']
P0=(F(0),F(0));P2=(F(6),F(0));v=(F(1),F(3));H=(P0+(F(1),),v+(F(0),),P2+(F(1),));L=(H[0],(F(0),F(0),F(0)),H[2]);u=F(2,5)
P=project(evaluate(H,u));Q=project(evaluate(L,u));f=2*u*(1-u)/((1-u)**2+u*u)
assert P==(F(36,13),F(36,13)) and Q==(F(24,13),F(0));assert tuple((x-y)/f for x,y in zip(P,Q))==v
# Affine image of the upper unit semicircle, x=3-3*cos(t)+sin(t),y=3*sin(t).
X=(F(0),F(2),F(4));Y=(F(0),F(6),-F(6));W=(F(1),-F(2),F(2))
A=add(add(X,tuple(-3*x for x in W)),tuple(-x/3 for x in Y));A=tuple(x/3 for x in A);B=tuple(y/3 for y in Y)
identity=add(add(multiply(A,A),multiply(B,B)),tuple(-x for x in multiply(W,W)));assert all(x==0 for x in identity)
for i in range(101):
    t=F(i,100);h=evaluate(H,t);c=project(h);q=project(evaluate(L,t));factor=2*t*(1-t)/((1-t)**2+t*t)
    assert h[-1]>=F(1,2) and c==tuple(x+factor*y for x,y in zip(q,v))
    assert ((c[0]-3-c[1]/3)/3)**2+(c[1]/3)**2==1 and c[1]>=0
left2=sum((x-y)**2 for x,y in zip(P0,Q));right2=sum((x-y)**2 for x,y in zip(Q,P2));assert left2/right2==(u/(1-u))**4
paths=approximate(H,F(1,200000));T0=tuple(2*x for x in v);T2=tuple(-2*x for x in v)
lines=['% Exact oblique upper half ellipse, H0(0,0,1),H1(1,3,0),H2(6,0,1).',
       '% ((x-3-y/3)/3)^2+(y/3)^2=1; W>=1/2; nonzero infinite vector.',
       r'\begin{tikzpicture}[book line,x=2.1cm,y=2.1cm]',r'\path[use as bounding box] (-.8,-2.6) rectangle (7.1,3.7);',
       r'\draw[book grid,dashed] '+point(P0)+'--'+point(P2)+';',r'\draw[book grid,dashed] '+point(Q)+'--'+point(P)+';']
lines.extend(cubic_path(s) for s in paths)
for base,tan,label in [(P0,T0,r'\mathbf T_0'),(P2,T2,r'\mathbf T_2')]:
    end=tuple(x+F(3,10)*y for x,y in zip(base,tan));anchor='left' if base==P0 else 'right'
    lines.append(r'\draw[book axis] '+point(base)+'--'+point(end)+r' node[pos=.7,'+anchor+r'=7pt] {$'+label+'$};')
for q,label,anchor in [(P0,r'\mathbf P_0','below left'),(P2,r'\mathbf P_2','below right'),(P,r'\mathbf P','above left'),(Q,r'\mathbf Q','below')]:
    lines.append(r'\draw '+point(q)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$'+label+'$};')
for a,b,label in [(P0,Q,r'u^2'),(Q,P2,r'(1-u)^2')]:
    mid=tuple((x+y)/2 for x,y in zip(a,b));lines.append(r'\node[above=6pt] at '+point(mid)+' {$'+label+'$};')
lines += [r'\node[below=7pt] at (5.4,-1.8) {$\mathbf T_2\parallel-\overrightarrow{\mathbf P}_1$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_29.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/infinite-ellipse-projection-check.json').write_text(json.dumps({'figure':'7.24','homogeneous_controls':[[str(x) for x in h] for h in H],'u':str(u),'P':list(map(str,P)),'Q':list(map(str,Q)),'recovered_infinite_vector':list(map(str,v)),'exact_ellipse_polynomial_identity_coefficients':list(map(str,identity)),'exact_parallel_projection_and_ellipse_checks':101,'distance_ratio_exact':True,'endpoint_tangents':[list(map(str,T0)),list(map(str,T2))],'denominator_lower_bound':'1/2','native_L1_error':str(max(s['certified_l1_error'] for s in paths))},indent=2)+'\n')
print('PASS:exact ellipse polynomial identity,101parallel-projection checks,nonzero infinite vector recovered by7.41 and chord ratio exact.')
