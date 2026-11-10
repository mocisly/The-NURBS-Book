"""Fig4.13: genuinely rational bicubic surface and exact first/second jets."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import piece
from native_bspline import segments,check,cubic_path,point
from rational_geometry import approximate,project
from surface_geometry import surface,isocurve,verify_tensor
from rational_surface_partials import jets,derived_net
from nurbs412_data import K,P as BASE

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch04/fig_4_15.tex';assert not target.exists()
P=tuple(tuple((x,F(2,3)*y,z) for x,y,z in row) for row in BASE)
H=tuple(tuple(tuple((4 if (i,j)==(2,2) else 1)*c for c in P[i][j])+((F(4) if (i,j)==(2,2) else F(1)),) for j in range(5)) for i in range(5))
u0,v0=F(3,4),F(1,4);values=jets(K,K,3,3,H,u0,v0)

# Independent bivariate polynomial differentiation of A/W on every knot patch.
def add(a,b):
    r=dict(a)
    for k,c in b.items():r[k]=r.get(k,F(0))+c
    return {k:c for k,c in r.items() if c}
def scale(a,s):return {k:c*s for k,c in a.items() if c*s}
def mul(a,b):
    r={}
    for (i,j),c in a.items():
        for (k,l),d in b.items():r[i+k,j+l]=r.get((i+k,j+l),F(0))+c*d
    return {k:c for k,c in r.items() if c}
def diff(a,axis):
    return {((i-1,j) if axis==0 else (i,j-1)):c*(i if axis==0 else j) for (i,j),c in a.items() if (i if axis==0 else j)}
def ev(a,u,v):return sum(c*u**i*v**j for (i,j),c in a.items())
def rational_diff(a,s,W,axis):return add(mul(diff(a,axis),W),scale(mul(a,diff(W,axis)),-s)),s+1
verified=0
for su in (3,4):
    for sv in (3,4):
        polys=[{} for _ in range(4)]
        for i in range(5):
            for j in range(5):
                B={(a,b):c*d for a,c in enumerate(piece(K,i,3,su)) for b,d in enumerate(piece(K,j,3,sv)) if c*d}
                polys=[add(poly,scale(B,H[i][j][d])) for d,poly in enumerate(polys)]
        W=polys[-1];quotients={}
        for r,s in values:
            forms=[]
            for A in polys[:-1]:
                power=1
                for axis,n in ((0,r),(1,s)):
                    for _ in range(n):A,power=rational_diff(A,power,W,axis)
                forms.append((A,power))
            quotients[r,s]=forms
        for a in (F(1,4),F(1,2),F(3,4)):
            for b in (F(1,4),F(1,2),F(3,4)):
                u=K[su]+a*(K[su+1]-K[su]);v=K[sv]+b*(K[sv+1]-K[sv]);J=jets(K,K,3,3,H,u,v)
                assert ev(W,u,v)>=1
                for key,forms in quotients.items():
                    assert J[key]==tuple(ev(A,u,v)/ev(W,u,v)**power for A,power in forms);verified+=1
        if su==4 and sv==3:
            for key,forms in quotients.items():assert values[key]==tuple(ev(A,u0,v0)/ev(W,u0,v0)**power for A,power in forms)
assert derived_net(*derived_net(K,K,3,3,H,0),1)==derived_net(*derived_net(K,K,3,3,H,1),0)
tensor=verify_tensor(K,K,3,3,H,10)
lines=['% Fig4.13: representative bicubic rational dome, 5x5 controls, w22=4 and other weights=1.',
       '% K=(0,0,0,0,1/2,1,1,1,1); control coordinates documented in geometry report.',
       '% Exact quotient partials at (u,v)=(3/4,1/4); first arrows scaled 1/2, second arrows 1/3.',
       '% Native certified rational isocurves; no raster outlines.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-6cm,y=-4.5cm) rectangle (canvas cs:x=7cm,y=6cm);',
       r'\draw[book axis] (0,0,0)--(5.3,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis] (0,0,0)--(0,6,0) node[right=4pt] {$y$};',
       r'\draw[book axis] (0,0,0)--(0,0,5.3) node[above=4pt] {$z$};']
exact=paths=0;error=F(0)
for var in ('u','v'):
    fixed=v0 if var=='u' else u0
    for t in sorted(set([F(i,5) for i in range(6)]+[fixed])):
        k,d,c=isocurve(K,K,3,3,H,var,t);ss=segments(k,c,d);exact+=check(k,c,d,ss)
        style='book line,dashed' if t==fixed else ('book line' if t in (0,1) else 'book grid')
        for seg in ss:
            for a in approximate(seg['bern'],F(1,15000)):
                lines.append(cubic_path(a,style));paths+=1;error=max(error,F(3,2)*a['certified_l1_error'])
origin=values[0,0]
for key,anchor,label in [((1,0),'right',r'\mathbf S_u'),((0,1),'above right',r'\mathbf S_v'),((2,0),'right',r'\mathbf S_{uu}'),((1,1),'below right',r'\mathbf S_{uv}'),((0,2),'below left',r'\mathbf S_{vv}')]:
    divisor=2 if sum(key)==1 else 3;end=tuple(origin[d]+values[key][d]/divisor for d in range(3))
    lines.append(r'\draw[book axis] '+point(origin)+'--'+point(end)+';')
    external={(1,0):(r'(canvas cs:x=5.8cm,y=2.9cm)','right'),(1,1):(r'(canvas cs:x=0cm,y=-3.8cm)','below'),(0,2):(r'(canvas cs:x=-5.2cm,y=-.7cm)','left')}
    if key in external:
        pos,anchor=external[key]
        lines.append(r'\draw[book grid] '+point(end)+'--'+pos+' node['+anchor+'=5pt] {$'+label+'$};')
    else:lines.append(r'\node['+anchor+'=5pt] at '+point(end)+' {$'+label+'$};')
lines.append(r'\fill '+point(origin)+' circle[radius=1.6pt];')
for u,v,label,pos,anchor in [(u0,F(0),r'u=\frac34',r'(canvas cs:x=-3.6cm,y=.6cm)','left'),(F(1),v0,r'v=\frac14',r'(canvas cs:x=3.8cm,y=-3.6cm)','right')]:
    h=surface(K,K,3,3,H,u,v)
    lines.append(r'\draw[book grid] '+point(project(h))+'--'+pos+' node['+anchor+'=4pt] {$'+label+'$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/nurbs-surface-partials-check.json').write_text(json.dumps({
    'figure':'4.13','representative_surface':True,'degrees':[3,3],'knots':list(map(str,K)),
    'controls':[[list(map(str,p)) for p in row] for row in P],'weights':'w22=4, all other weights1',
    'global_denominator_lower_bound':'1','tensor_vs_nested_deboor_points':tensor,
    'rational_derivative_net_vs_independent_symbolic_quotient_comparisons':verified,
    'mixed_homogeneous_derivative_nets_commute':True,'selected_parameter':['3/4','1/4'],
    'point_and_partials':{str(k):list(map(str,v)) for k,v in values.items()},
    'first_derivative_display_scale':'1/2','second_derivative_display_scale':'1/3',
    'exact_homogeneous_isocurve_checks':exact,'native_paths':paths,'maximum_certified_projected_l1_error_cm':str(error)},indent=2)+'\n')
print(f'PASS: {verified} independent exact rational derivative comparisons, {tensor} tensor points, {exact} curve checks; {paths} native paths.')
