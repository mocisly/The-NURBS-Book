"""6.4: exact pushforward of a curved parameter-space path and inverse Gram solve."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
from projection_surface_data import BASE,partials
from surface_geometry import surface,isocurve,verify_tensor
from native_bspline import segments,check,cubic_path,point
from bspline_math import add,evaluate,derivative,compose_affine
from native_polynomial_drawing import paths

root=Path(__file__).resolve().parents[1]
target=root/'image_tex/ch06/fig_6_04.tex'
manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch06/fig_6_04.tex')['applied']

def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return tuple(out)
def compose(a,b):
    out=(F(0),)
    for c in reversed(a):out=add(mul(out,b),(c,))
    return out
def bernstein(power,a,b):
    local=[compose_affine(c,a,b-a) for c in power];n=max(map(len,local))-1
    return tuple(tuple(sum((c[k] if k<len(c) else 0)*F(comb(j,k),comb(n,k)) for k in range(j+1)) for c in local) for j in range(n+1))
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def times(a,s):return tuple(x*s for x in a)
def dot(a,b):return sum(x*y for x,y in zip(a,b))

# Entire curved path stays in the v>1/2 polynomial surface patch.
up=(F(9,20),-F(2,5),F(2,25));vp=(F(13,20),F(3,20),F(1,20))
u,v=up[0],vp[0];W=(up[1],vp[1]);P=surface(*BASE,u,v);Su,Sv=partials(u,v)
T=plus(times(Su,W[0]),times(Sv,W[1]))
g11,g12,g22=dot(Su,Su),dot(Su,Sv),dot(Sv,Sv);det=g11*g22-g12*g12
assert det>0
rhs=(dot(Su,T),dot(Sv,T))
recovered=((g22*rhs[0]-g12*rhs[1])/det,(g11*rhs[1]-g12*rhs[0])/det)
assert recovered==W
# Explicit graph patch: x=1-4v^2, y=-2+21u/5-3u^2/5+2u^3/5,
# z=2/5(1-33u^2/5+22u^3/5+2-4(v-1)^2).
xp=compose((F(1),F(0),-F(4)),vp)
yp=compose((-F(2),F(21,5),-F(3,5),F(2,5)),up)
zp=add(compose((F(1),F(0),-F(33,5),F(22,5)),up),compose((-F(2),F(8),-F(4)),vp))
zp=tuple(F(2,5)*x for x in zp);power=(xp,yp,zp)
assert tuple(evaluate(c,F(0)) for c in power)==P
assert tuple(evaluate(derivative(c),F(0)) for c in power)==T
for i in range(101):
    t=-F(4,5)+F(8,5)*F(i,100);a,b=evaluate(up,t),evaluate(vp,t)
    assert 0<a<1 and F(1,2)<b<1
    assert surface(*BASE,a,b)==tuple(evaluate(c,t) for c in power)
curve,certificate=paths([{'bern':bernstein(power,-F(4,5),F(4,5))}],tolerance=F(1,10000))
uvcurve=cubic_path({'bern':bernstein((up,vp),-F(4,5),F(4,5))},'book line')
lines=['% Exact tangent inversion on the representative surface used in6.3.',
       '% One polynomial parameter path and its certified polynomial surface image.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-5.3,-5.4) rectangle (17.7,8.5);',
       r'\begin{scope}[x={(-.81cm,-.54cm)},y={(.9cm,-.315cm)},z={(0cm,2.25cm)}]']
checks=verify_tensor(*BASE,steps=10)
for variable,vals in [('u',(F(0),F(1))),('v',(F(0),F(1)))]:
    for fixed in vals:
        K,p,Q=isocurve(*BASE,variable,fixed);ss=segments(K,Q,p);checks+=check(K,Q,p,ss)
        lines.extend(cubic_path(s) for s in ss)
for variable,fixed in [('u',v),('v',u)]:
    K,p,Q=isocurve(*BASE,variable,fixed);ss=segments(K,Q,p);checks+=check(K,Q,p,ss)
    lines.extend(cubic_path(s,'book grid,dashed') for s in ss)
lines.extend(curve)
for vec,label,anchor in [(Su,r'\mathbf S_u','below right'),(Sv,r'\mathbf S_v','above right'),(T,r'\mathbf T','above left')]:
    lines.append(r'\draw[book axis] '+point(P)+'--'+point(plus(P,vec))+r' node['+anchor+r'=5pt] {$'+label+'$};')
lines += [r'\draw '+point(P)+r' circle[radius=2pt] node[below left=5pt] {$\mathbf P$};',
          r'\draw[book axis] (0,0,0)--(5.3,0,0) node[below left=3pt] {$x$};',
          r'\draw[book axis] (0,0,0)--(0,6.3,0) node[right=3pt] {$y$};',
          r'\draw[book axis] (0,0,0)--(0,0,2.8) node[above=3pt] {$z$};',
          r'\end{scope}',r'\begin{scope}[xshift=10cm,yshift=.9cm,x=6cm,y=6cm]']
lines += [r'\draw[book grid] (0,0) rectangle (1,1);',
          r'\draw[book axis] (0,0)--(1.12,0) node[right=3pt] {$u$};',
          r'\draw[book axis] (0,0)--(0,1.12) node[above=3pt] {$v$};',uvcurve,
          r'\draw[book grid,dashed] '+point((u,0))+'--'+point((u,v))+'--'+point((0,v))+';',
          r'\node[below=4pt] at '+point((u,0))+r' {$\bar u$};',
          r'\node[left=4pt] at '+point((0,v))+r' {$\bar v$};',
          r'\draw[book axis] '+point((u,v))+'--'+point(plus((u,v),W))+r' node[above left=4pt] {$\mathbf W=(du,dv)$};',
          r'\draw '+point((u,v))+r' circle[radius=2pt] node[below left=5pt] {$(\bar u,\bar v)$};',r'\end{scope}',
          r'\draw[book axis] (11,-.5) .. controls (10,-1.6) and (8,-2.1) .. (6.4,-2.2) node[midway,below=6pt] {$D\mathbf S$};',
          r'\node at (11,-3.8) {$\mathbf T=\mathbf S_u\,du+\mathbf S_v\,dv$};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-tangent-inversion-check.json').write_text(json.dumps({
    'figure':'6.4','parameter_point':list(map(str,(u,v))),'P':list(map(str,P)),
    'Su':list(map(str,Su)),'Sv':list(map(str,Sv)),'W':list(map(str,W)),'T':list(map(str,T)),
    'gram_determinant':str(det),'exact_inverse_recovered':list(map(str,recovered)),
    'exact_chain_rule':True,'exact_surface_path_checks':101,'native_checks':checks,
    'surface_curve_certificate':certificate},indent=2)+'\n')
print(f'PASS:{checks} native checks,101 exact surface/path identities, exact chain rule and Gram inversion.')
