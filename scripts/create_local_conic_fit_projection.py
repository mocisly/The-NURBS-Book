"""9.53: exact shoulder averaging and a certified global closest conic point."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from rational_geometry import approximate,evaluate,project
from native_bspline import point,cubic_path
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_63.tex')['applied']
A=(F(0),F(0));B=(F(6),F(0));R=(F(3),F(4));M=(F(3),F(0));S=(F(3),F(2));Ts=(F(3,5),F(4,5));Te=(F(3,5),-F(4,5))
assert sum(x*x for x in Ts)==sum(x*x for x in Te)==1
assert R==tuple(a+5*t for a,t in zip(A,Ts))==tuple(b-5*t for b,t in zip(B,Te))
u=F(3,5);foot=(6*u,8*u*(1-u));normal=(F(4),F(15));k=-F(5,2)
delta=(-F(133,120)-F(12,25)*k)/(k*k-F(1769,576));assert delta>0
Qi=tuple(a+delta*n for a,n in zip(foot,normal))
def H(w):return (A+(F(1),),tuple(w*x for x in R)+(w,),B+(F(1),))
def infer(q):
    lr=q[1]/4;lb=(q[0]-3*lr)/6;la=1-lr-lb;square=la*lb
    nr=isqrt(square.numerator);dr=isqrt(square.denominator);assert nr*nr==square.numerator and dr*dr==square.denominator
    rt=F(nr,dr);w=lr/(2*rt);ratio=lb/rt;t=ratio/(1+ratio)
    assert la>0 and lb>0 and lr>0 and 0<t<1 and project(evaluate(H(w),t))==q
    return w,w/(1+w),t
w3,s3,t3=infer(Qi);s1=F(2,5);s2=F(3,2)-s1-s3;assert 0<s2<1
weights=(s1/(1-s1),s2/(1-s2),w3)
data=(project(evaluate(H(weights[0]),F(1,4))),project(evaluate(H(weights[1]),F(2,5))),Qi)
recovered=tuple(infer(q) for q in data);s=sum(x[1] for x in recovered)/3;w=s/(1-s)
assert s==F(1,2) and w==1 and project(evaluate(H(w),F(1,2)))==S
assert project(evaluate(H(w),u))==foot
tangent=(F(6),8-16*u);assert sum((a-b)*t for a,b,t in zip(Qi,foot,tangent))==0
# Half derivative of squared distance factors as(t-u)*(128t²-576t/5+c).
# For C=(6t,8t(1-t)), coefficients are128,-192,100+16Qiy.
quad=(F(128),-F(576,5),F(100)+16*Qi[1]-F(1728,25))
disc=quad[1]**2-4*quad[0]*quad[2];assert disc<0 and quad[0]>0
assert -(6*Qi[0]+8*Qi[1])==-u*quad[2]
assert quad[1]-u*quad[0]==-192 and quad[2]-u*quad[1]==100+16*Qi[1]
out=['% Three actual point-interpolating conics;mean shoulder s=1/2;fitted w1parabola;exact globalclosestfoot.',r'\begin{tikzpicture}[book line,x=3cm,y=3cm]',r'\path[use as bounding box] (-.6,-1.5) rectangle (7.4,4.6);']
def line(a,b,style='book grid'):return r'\draw['+style+'] '+point(a)+'--'+point(b)+';'
out.extend([line(A,R),line(R,B),line(A,B),line(M,R)])
native=[]
for weight in weights+(w,):
    ss=approximate(H(weight),F(1,100000));assert max(s['certified_l1_error'] for s in ss)<=F(1,100000)
    out.extend(cubic_path(s,'book grid,dashed' if weight!=w else '') for s in ss)
    native.append(dict(weight=str(weight),pieces=len(ss),certified_native_L1_error='1e-5',positive_denominator_lower_bound=str(min(F(1),weight))))
out.append(line(Qi,foot))
T=(F(15,150),-F(4,150));N=(F(4,150),F(15,150))
right_angle=(tuple(a+b for a,b in zip(foot,T)),tuple(a+b+c for a,b,c in zip(foot,T,N)),tuple(a+b for a,b in zip(foot,N)))
out.append(r'\draw[book grid] '+'--'.join(map(point,right_angle))+';')
for q,name,anchor in [(A,r'\mathbf Q_{k_s}','below left'),(B,r'\mathbf Q_{k_e}','above right'),(R,r'\mathbf R','above'),(M,r'\mathbf M','below'),(Qi,r'\mathbf Q_i','above right'),(foot,r'\mathbf Q^{\prime}_i','above left')]:
    out.extend([r'\draw '+point(q)+r' circle[radius=2.4pt];',r'\node['+anchor+r'=6pt] at '+point(q)+' {$'+name+'$};'])
out.extend(r'\draw '+point(q)+r' circle[radius=2.4pt];' for q in data[:2])
out.extend([r'\draw '+point(S)+r' ++(-2.2pt,-2.2pt) rectangle ++(4.4pt,4.4pt);',r'\node[left=7pt] at '+point(S)+r' {$\mathbf S$};'])
out.extend([line(tuple(F(9,10)*x for x in Ts),tuple(F(19,10)*x for x in Ts),'book grid,book axis'),r'\node[left=7pt] at '+point(tuple(F(19,10)*x for x in Ts))+r' {$\mathbf T_s$};',line(B,tuple(b+t for b,t in zip(B,Te)),'book grid,book axis'),r'\node[right=7pt] at '+point(tuple(b+t for b,t in zip(B,Te)))+r' {$\mathbf T_e$};',r'\end{tikzpicture}'])
(root/'image_tex/ch09/fig_9_63.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report=dict(figure='9.53',representative_triangle=[list(map(str,p)) for p in (A,R,B)],unit_endpoint_tangents=[list(map(str,Ts)),list(map(str,Te))],gamma_start='5',gamma_end='-5',data=[list(map(str,p)) for p in data],point_interpolating_weights=[str(x[0]) for x in recovered],individual_shoulder_parameters=[str(x[1]) for x in recovered],mean_shoulder_parameter=str(s),fitted_weight=str(w),mean_formula_and_midpoint_exact=True,displayed_projected_parameter=str(u),displayed_point=list(map(str,Qi)),exact_closest_point=list(map(str,foot)),normal_orthogonality_exact=True,closest_point_global_unique_proof='squared-distance derivative=(t-3/5)*positive quadratic;quadratic leading coefficient128>0,discriminant<0',quadratic_coefficients=list(map(str,quad)),quadratic_discriminant=str(disc),native_conics=native,coordinate_scale='3cm',font_rescaling=False)
(root/'image_tex/build/local-conic-fit-projection-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.53:exact3conicinterpolants/shouldermean.5/fittedw1;Qi normal anduniqueGLOBALclosestfootprovedbypositivequadratic;allnativeerrors<=1e-5.')
