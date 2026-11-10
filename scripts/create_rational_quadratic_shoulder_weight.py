"""9.26: exact nonisosceles angle-bisector shoulder and its rational weight."""
from pathlib import Path
from fractions import Fraction as F
import json
from local_quadratic_interpolator import add,mul,cross,dot,length
from native_bspline import point,cubic_path
from rational_geometry import approximate,evaluate,project
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_32.tex')['applied']
A=(F(0),F(0));B=(F(7),F(0));R=(F(5,2),F(6));M=mul(add(A,B),F(1,2));mr=add(R,M,-1)
assert length(add(R,A,-1))==F(13,2) and length(add(R,B,-1))==F(15,2)
def bisector(P,Q):
    a=add(R,P,-1);b=add(Q,P,-1)
    u=mul(a,1/length(a));v=mul(b,1/length(b));return add(u,v)
def intersection(P,D):
    delta=add(M,P,-1);den=cross(D,mr)
    t=cross(delta,mr)/den;s=cross(delta,D)/den
    X=add(P,D,t);assert X==add(M,mr,s) and t>0 and 0<s<1
    # A ray along the sum of the two unit sides is their internal bisector.
    return X,s
D1=bisector(A,B);D2=bisector(B,A)
S1,s1=intersection(A,D1);S2,s2=intersection(B,D2)
assert (s1,s2)==(F(7,20),F(7,22))
S=mul(add(S1,S2),F(1,2));s=(s1+s2)/2;w=s/(1-s)
assert s==F(147,440) and w==F(147,293) and S==add(M,mr,s)
H=(A+(F(1),),tuple(w*x for x in R)+(w,),B+(F(1),))
assert project(evaluate(H,F(1,2)))==S
assert project(H[0])==A and project(H[-1])==B and w>0
for j in range(101):assert evaluate(H,F(j,100))[-1]>0
# A rational rigid rotation keeps every incidence, angle and length exact.
def camera(q):
    x,y=q;return (F(24,25)*x+F(7,25)*y,-F(7,25)*x+F(24,25)*y)
HH=tuple(camera(h[:2])+(h[2],) for h in H)
ss=approximate(HH,F(1,100000));assert max(t['certified_l1_error'] for t in ss)<=F(1,100000)
def line(P,Q,style='book grid'):return r'\draw['+style+'] '+point(camera(P))+'--'+point(camera(Q))+';'
out=['% Exact13-14-15 triangle scaled1/2;angle bisectors,average shoulder and positive weight147/293.',r'\begin{tikzpicture}[book line,x=2.8cm,y=2.8cm]',r'\path[use as bounding box] (-.9,-2.7) rectangle (7.7,5.8);',line(A,R),line(R,B),line(A,B,'book grid,dashed'),line(M,R),line(A,S1),line(B,S2)]
out.extend(cubic_path(t) for t in ss)
for q,name,anchor in [(A,r'\mathbf Q_{k-1}','below left'),(B,r'\mathbf Q_k','below right'),(R,r'\mathbf R_k','above'),(M,r'\mathbf M','below'),(S1,r'\mathbf S_1','above right')]:
    out.extend([r'\draw '+point(camera(q))+r' circle[radius=2.4pt];',r'\node['+anchor+r'=6pt] at '+point(camera(q))+' {$'+name+'$};'])
out.extend([r'\draw '+point(camera(S2))+r' circle[radius=2.4pt];',r'\draw[book grid] '+point(camera(S2))+r'--(2.7,.3) node[left=4pt] {$\mathbf S_2$};',r'\fill '+point(camera(S))+r' circle[radius=1.4pt];',r'\draw[book grid] '+point(camera(S))+r'--(1.8,.95) node[left=4pt] {$\mathbf S$};',r'\end{tikzpicture}'])
(root/'image_tex/ch09/fig_9_32.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report=dict(figure='9.26',representative_triangle=[list(map(str,p)) for p in (A,R,B)],side_lengths=['13/2','15/2','7'],nonisosceles=True,bisector_directions=[list(map(str,p)) for p in (D1,D2)],bisector_MR_parameters=list(map(str,(s1,s2))),shoulder_MR_parameter=str(s),weight=str(w),shoulder=list(map(str,S)),rational_midpoint_equals_shoulder_exact=True,positive_denominator_samples=101,rigid_rational_rotation=['24/25','-7/25'],native_cubic_pieces=len(ss),certified_l1_error_bound='1e-5')
(root/'image_tex/build/rational-quadratic-shoulder-weight-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS9.26:exact nonisosceles13-14-15 triangle,bisectors7/20,7/22,average shoulder147/440,weight147/293 and rational midpoint identity;certified native curve.')
