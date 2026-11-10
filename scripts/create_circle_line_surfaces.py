"""8.7: actual ruled NURBS between degree2/3/4 circular curves and straight lines."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import project,approximate
from surface_geometry import surface,verify_tensor
from polynomial_native import multiply
from bspline_math import add,compose_affine
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (10,11):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch08/fig_8_{n:02d}.tex')['applied']
def camera(p):
    x,y,z=p;return (4*(-F(39,50)*x+F(24,25)*y),4*(-x/2-F(3,10)*y+z))
D=10**40;n=isqrt(2*D*D);lo,hi=F(n,2*D),F(n+1,2*D);assert lo*lo<F(1,2)<hi*hi;w=(lo+hi)/2
P2=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0)]
H2=tuple((F(x)*a,F(y)*a,F(0),a) for i,(x,y) in enumerate(P2) for a in [w if i%2 else F(1)])
U2=(F(0),)*3+(F(1,4),)*2+(F(1,2),)*2+(F(3,4),)*2+(F(1),)*3
P3=[(1,0),(1,2),(-1,2),(-1,0),(-1,-2),(1,-2),(1,0)]
H3=tuple((F(x)*a,F(y)*a,F(0),a) for i,(x,y) in enumerate(P3) for a in [F(1) if i%3==0 else F(1,3)])
U3=(F(0),)*4+(F(1,2),)*3+(F(1),)*4
H4=tuple(tuple(map(F,h)) for h in [(3,0,0,3),(0,3,0,0),(-3,0,0,1),(0,-3,0,0),(3,0,0,3)])
U4=(F(0),)*5+(F(1),)*5
models=[('a',2,U2,H2,(1,0,2),(-1,0,2),w),('b',3,U3,H3,(F(5,4),0,2),(F(5,4),0,-2),F(1,3)),('c',4,U4,H4,(F(2,5),-F(1,4),-2),(F(2,5),-F(1,4),2),F(3,4))]
panels=[];reports=[];V=(F(0),F(0),F(1),F(1))
for label,p,U,H,A,B,lower in models:
    A=tuple(map(F,A));B=tuple(map(F,B))
    def line(u):
        if label=='c':return (F(2,5),-F(1,4),64*u**3-96*u**2+36*u-2)
        return tuple((1-u)*a+u*b for a,b in zip(A,B))
    # Greville control values reproduce an affine curve exactly in the circle's basis.
    L=tuple(line(sum(U[i+1:i+p+1])/p)+(F(1),) for i in range(len(H)))
    if label=='c':L=tuple((F(2,5),-F(1,4),F(z),F(1)) for z in (-2,7,0,-7,2))
    net=tuple(zip(H,L));tc=verify_tensor(U,V,p,1,net);ss=segments(U,H,p);nc=check(U,H,p,ss);bounds=[]
    for s in ss:
        X,Y,_,W=s['power'];res=add(add(multiply(X,X),multiply(Y,Y)),tuple(-x for x in multiply(W,W)))
        bound=sum(map(abs,compose_affine(res,s['a'],s['b']-s['a'])))/lower**2
        assert bound<F(1,10**37);bounds.append(str(bound))
    for i in range(21):
        u=F(i,20);hc=de_boor(U,H,p,u);C=project(hc);ll=line(u)
        assert de_boor(U,L,p,u)==ll+(F(1),) and hc[-1]>=lower
        for j in range(21):
            v=F(j,20);h=surface(U,V,p,1,net,u,v);P=project(h);den=(1-v)*hc[-1]+v
            assert h[-1]==den and den>0
            assert P==tuple(((1-v)*hc[-1]*c+v*l)/den for c,l in zip(C,ll))
    lines=[r'\begin{scope}',r'\path[use as bounding box] (-7.5,-12) rectangle (8.7,12);']
    for i in range(61):
        u=F(i,60);C=project(de_boor(U,H,p,u));ll=line(u)
        lines.append(r'\draw[book grid] '+point(camera(C))+'--'+point(camera(ll))+';')
    hh=tuple(camera(h[:3])+(h[-1],) for h in H)
    paths=[part for s in segments(U,hh,p) for part in approximate(s['bern'],F(1,100000))]
    lines.extend(cubic_path(part) for part in paths)
    lines.append(r'\draw '+point(camera(A))+'--'+point(camera(B))+';')
    for end,name,anchor in [((F(2),0,0),'x','below left'),((0,F(2),0),'y','right'),((0,0,F(27,10)),'z','above')]:
        lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    lines.extend([r'\node at (.6,-11.3) {('+label+')};',r'\end{scope}']);panels.append(lines)
    reports.append({'panel':label,'degrees':[p,1],'circle_homogeneous_controls':[[str(x) for x in h] for h in H],'circle_knots':list(map(str,U)),'line_endpoints':[list(map(str,A)),list(map(str,B))],'line_parameterization':'z=64u^3-96u^2+36u-2,quartic elevated controls -2,7,0,-7,2' if label=='c' else 'affine,exact Greville control values','circle_denominator_lower_bound':str(lower),'circle_residual_whole_span_bounds':bounds,'exact_tensor_checks':tc,'exact_projective_linear_ruling_checks':441,'native_curve_checks':nc,'generator_grid':'u=i/60','native_curve_screen_L1_error_cm':str(max(part['certified_l1_error'] for part in paths))})
for n,ll in [(10,panels[0]+[r'\begin{scope}[xshift=19cm]']+panels[1]+[r'\end{scope}']),(11,panels[2])]:
    (root/f'image_tex/ch08/fig_8_{n:02d}.tex').write_text('% Mathematical circle/line ruled surfaces; transparent wireframe,not outline tracing.\n'+r'\begin{tikzpicture}[book line]'+'\n'+'\n'.join(ll)+'\n'+r'\end{tikzpicture}'+'\n',encoding='utf-8')
(root/'image_tex/build/circle-line-surfaces-check.json').write_text(json.dumps({'figure':'8.7','representative_data_explicit':True,'models':reports},indent=2)+'\n')
print('PASS:three genuine circle/line surfaces,p=2/3/4,q=1;1323 tensor and projective-ruling checks;affine line reproduction and whole-span circle identities.')
