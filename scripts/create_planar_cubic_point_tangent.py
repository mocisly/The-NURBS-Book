"""9.56: exact deCasteljau tangent and compatible point/tangent LS equations."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point,segments,check,cubic_path,de_boor
from inverse_knot_projection import solve
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_68.tex')['applied']
P0=(F(0),F(0));P1=(F(3),F(4));P2=(F(6),F(4));P3=(F(9),F(0));controls=(P0,P1,P2,P3)
Ts=(F(3,5),F(4,5));Te=(F(3,5),-F(4,5));Tp=(F(1),F(0));alpha=F(5);beta=-F(5);t=s=F(1,2)
def add(a,b,c=F(1)):return tuple(x+c*y for x,y in zip(a,b))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
L1=tuple(tuple(s*x+t*y for x,y in zip(a,b)) for a,b in zip(controls,controls[1:]));L2=tuple(tuple(s*x+t*y for x,y in zip(a,b)) for a,b in zip(L1,L1[1:]));P=tuple(s*x+t*y for x,y in zip(*L2))
assert L2==((3,3),(6,3)) and P==(F(9,2),F(3)) and add(P0,Ts,alpha)==P1 and add(P3,Te,beta)==P2
assert cross(Tp,add(L2[1],L2[0],-1))==0
A=[(3*s*s*t*Ts[d],3*s*t*t*Te[d]) for d in range(2)]
rhs=[P[d]-(s**3+3*s*s*t)*P0[d]-(t**3+3*s*t*t)*P3[d] for d in range(2)]
A.append((s*(s-2*t)*cross(Tp,Ts),t*(2*s-t)*cross(Tp,Te)));rhs.append(2*s*t*cross(Tp,add(P0,P3,-1)))
G=tuple(tuple(sum(row[i]*row[j] for row in A) for j in range(2)) for i in range(2));R=tuple((sum(row[i]*v for row,v in zip(A,rhs)),) for i in range(2))
solution=solve(G,R);assert tuple(x[0] for x in solution)==(alpha,beta) and all(row[0]*alpha+row[1]*beta==v for row,v in zip(A,rhs))
assert G[0][0]>0 and G[0][0]*G[1][1]-G[0][1]**2>0
U=(F(0),)*4+(F(1),)*4;ss=segments(U,controls,3);nc=check(U,controls,3,ss)
tests=[]
for da,db in [(F(1,3),F(1,5)),(-F(2,7),F(1,6)),(F(4,9),-F(2,5))]:
    changed=(P0,add(P1,Ts,da),add(P2,Te,db),P3);delta=add(de_boor(U,changed,3,t),P,-1)
    correct=tuple(da*3*s*s*t*x+db*3*s*t*t*y for x,y in zip(Ts,Te));wrong=tuple(da*3*s*s*t*x-db*3*s*t*t*y for x,y in zip(Ts,Te))
    assert delta==correct and sum(x*x for x in correct)!=sum(x*x for x in wrong)
    tests.append(dict(delta_alpha=str(da),delta_beta=str(db),exact_vector_identity_with_plus=True,incorrect_minus_gives_different_norm=True))
out=['% Exact planar cubic,deCasteljauu1/2,secondlevelpoints(3,3)/(6,3),P(4.5,3),unitTsTeTp.',r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-.6,-1.5) rectangle (10,4.7);']
out.extend([r'\draw[book grid,dashed] '+'--'.join(map(point,controls))+';',r'\draw[book grid,dashed] '+'--'.join(map(point,L1))+';',r'\draw[book grid,dashed] '+'--'.join(map(point,L2))+';'])
out.extend(cubic_path(piece) for piece in ss)
out.extend([r'\draw[book grid] '+point(P)+'--(7.3,3);',r'\draw[book grid,book axis] (7.3,3)--(8.3,3) node[right=6pt] {$\mathbf T_p$};',r'\draw[book grid,book axis] '+point(add(P0,Ts,F(9,10)))+'--'+point(add(P0,Ts,F(19,10)))+r' node[left=7pt] {$\mathbf T_s$};',r'\draw[book grid,book axis] '+point(P3)+'--'+point(add(P3,Te))+r' node[right=6pt] {$\mathbf T_e$};'])
for i,(q,anchor) in enumerate([(P0,'below left'),(P1,'above left'),(P2,'above right'),(P3,'right')]):
    out.extend([r'\draw '+point(q)+r' circle[radius=2.3pt];',r'\node['+anchor+r'=6pt] at '+point(q)+r' {$\mathbf P_'+str(i)+'$};'])
for i,(q,anchor) in enumerate(zip(L2,('above left','above right'))):
    out.extend([r'\draw '+point(q)+r' circle[radius=2pt];',r'\node['+anchor+r'=7pt] at '+point(q)+r' {$\mathbf P^{2}_'+str(i)+'$};'])
out.extend([r'\draw '+point(P)+r' circle[radius=2.3pt];',r'\node[below=7pt] at '+point(P)+r' {$\mathbf P$};',r'\end{tikzpicture}'])
(root/'image_tex/ch09/fig_9_68.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report=dict(figure='9.56',representative_controls=[list(map(str,q)) for q in controls],u='1/2',first_decasteljau_level=[list(map(str,q)) for q in L1],second_decasteljau_level=[list(map(str,q)) for q in L2],interpolated_point=list(map(str,P)),unit_Ts=list(map(str,Ts)),unit_Te=list(map(str,Te)),unit_Tp=list(map(str,Tp)),alpha='5',beta='-5',point_and_tangent_equations_9_107_108_exact=True,combined_LS_Gram_positive_definite=True,unique_LS_solution_exact=[5,-5],native_cubic_checks=nc,error_increment_9_110_checks=tests,correct_error_increment='Deltaalpha*B1*Ts+ Deltabeta*B2*Te',coordinate_scale='2.5cm',font_rescaling=False)
(root/'image_tex/build/planar-cubic-point-tangent-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.56:exactdeCasteljau/tangent;compatiblepoint+tangentLSuniquealpha5beta-5;',nc,'nativechecks;3independent9.110PLUSsignidentities.')
