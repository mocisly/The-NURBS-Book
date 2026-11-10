"""Fig6.1: exact representative cubic, genuine projection and point inversion."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from bspline_math import derivative,evaluate,add

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch06/fig_6_01.tex';assert not target.exists()
U=(F(0),)*4+(F(1),)*4
P=((F(0),F(-2)),(F(10,3),F(7)),(F(20,3),F(-7)),(F(10),F(1)))
ss=segments(U,P,3);checks=check(U,P,3,ss);power=ss[0]['power']
assert power==((F(0),F(10),F(0),F(0)),(F(-2),F(27),F(-69),F(45)))
ui=F(1,3);ubar=F(1,8);C=de_boor(U,P,3,ui)
T=tuple(evaluate(derivative(c),ui) for c in power);assert T==(F(10),F(-4))
normal=(F(4),F(10));Pa=tuple(c+F(3,20)*n for c,n in zip(C,normal));Pb=de_boor(U,P,3,ubar)
assert sum(t*(p-c) for t,p,c in zip(T,Pa,C))==0
assert sum(t*(p-c) for t,p,c in zip(T,Pb,C))!=0
# For y(u)-y(ui)=(u-ui)g(u), the exact distance difference factors as
# (u-ui)^2 [g(u)^2 +217-135u], which is >=82(u-ui)^2 on[0,1].
# This proves the illustrated foot is the UNIQUE global closest point.
def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    while len(c)>1 and not c[-1]:c.pop()
    return tuple(c)
g=(F(9),F(-54),F(45));H=add(mul(g,g),(F(217),F(-135)))
distance=(F(0),)
for polynomial,point_coordinate in zip(power,Pa):
    difference=add(polynomial,(-point_coordinate,));distance=add(distance,mul(difference,difference))
distance=add(distance,(-sum((a-b)**2 for a,b in zip(C,Pa)),))
assert distance==mul(mul((-ui,F(1)),(-ui,F(1))),H)
iteration=[];u=float(ui)
for j in range(8):
    curve=tuple(float(evaluate(c,u)) for c in power)
    first=tuple(float(evaluate(derivative(c),u)) for c in power)
    second=tuple(float(evaluate(derivative(derivative(c)),u)) for c in power)
    residual=tuple(x-float(y) for x,y in zip(curve,Pb))
    f=sum(a*b for a,b in zip(first,residual));fp=sum(a*b for a,b in zip(second,residual))+sum(a*a for a in first)
    iteration.append({'u':u,'squared_distance':sum(t*t for t in residual),'orthogonality_residual':f})
    if sum(t*t for t in residual)<1e-26:break
    u-=f/fp;assert 0<=u<=1
assert abs(u-float(ubar))<1e-12
lines=['% Exact representative cubic C(u)=(10u,-2+27u-69u^2+45u^3).',
       '% Projection foot globally certified, not merely a stationary point; inversion target lies exactly on curve.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.7,-3.3) rectangle (23,4);']
for j,target_point in enumerate((Pa,Pb)):
    lines.append(r'\begin{scope}[xshift='+str(12.3*j)+'cm]')
    lines.append(cubic_path(ss[0]))
    tip=tuple(c+F(19,50)*t for c,t in zip(C,T))
    lines.append(r'\draw[book axis] '+point(C)+'--'+point(tip)+r' node[above=5pt] {$\mathbf C^{\prime}(u_i)$};')
    lines.append(r'\draw[book axis] '+point(target_point)+'--'+point(C)+';')
    if j==0:
        a=tuple(c+F(1,40)*t for c,t in zip(C,T));b=tuple(x+F(1,40)*n for x,n in zip(a,normal));d=tuple(c+F(1,40)*n for c,n in zip(C,normal))
        lines.append(r'\draw[book grid] '+point(a)+'--'+point(b)+'--'+point(d)+';')
    lines.append(r'\draw '+point(C)+r' circle[radius=1.8pt];')
    lines.append(r'\draw '+point(target_point)+r' circle[radius=1.8pt];')
    lines.append(r'\node['+('above=6pt' if j==0 else 'left=6pt')+'] at '+point(target_point)+r' {$\mathbf P$};')
    lines.append(r'\node['+('below left=6pt' if j==0 else 'above right=6pt')+'] at '+point(C)+r' {$\mathbf C(u_i)$};')
    lines.append(r'\node at (5,-2.8) {('+chr(97+j)+')};')
    lines.append(r'\end{scope}')
lines.append(r'\end{tikzpicture}');target.parent.mkdir(exist_ok=True);target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/curve-projection-inversion-check.json').write_text(json.dumps({
    'figure':'6.1','representative_controls':[[str(x) for x in p] for p in P],
    'current_parameter':str(ui),'inverse_target_parameter':str(ubar),
    'current_curve_point':list(map(str,C)),'derivative':list(map(str,T)),
    'projection_point':list(map(str,Pa)),'inversion_point':list(map(str,Pb)),
    'projection_orthogonality_exact':True,'global_projection_distance_factorization_exact':True,
    'positive_quotient':'g(u)^2+217-135u >=82 on[0,1]','unique_global_projection_parameter':str(ui),
    'inversion_unique_because_x_equals_10u':True,'Newton_iterations':iteration,
    'native_checks':checks},indent=2)+'\n')
print('PASS:41 exact native checks; projection orthogonality+unique GLOBAL minimum certified; inversion target1/8 recovered by Newton.')
