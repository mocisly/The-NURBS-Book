"""Printed11.10, a mathematical rational curve family and exact cross ratio."""
from pathlib import Path
from fractions import Fraction as F
import json
from control_relocation_data import U
from native_bspline import segments,check,cubic_path,point,de_boor
from rational_geometry import approximate,project
root=Path(__file__).resolve().parents[1]
P=tuple(tuple(map(F,p)) for p in [(0,0),(2,0),(3,'1.8'),('1.5','3.3'),(4,6),('7.5','4.6'),('8.5',2),(6,0),('4.5','1.5')])
k=4;u=F(1,2);N=de_boor(U,tuple((F(i==k),) for i in range(9)),3,u)[0]
def H(w):return tuple(tuple((w if i==k else 1)*v for v in p)+(w if i==k else F(1),) for i,p in enumerate(P))
def C(w,t=u):return project(de_boor(U,H(w),3,t))
R,M,A=C(F(0)),C(F(1)),C(F(4));s=N;t=4*N/(1+3*N)
assert M==tuple((1-s)*r+s*p for r,p in zip(R,P[k]))
assert A==tuple((1-t)*r+t*p for r,p in zip(R,P[k]))
assert ((1-s)/s)/((1-t)/t)==4
lines=['% Representative nine-control cubic polygon chosen for Eq11.21-24, not digitized.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-.6,-.6) rectangle (9.2,6.8);',r'\draw[book grid] '+'--'.join(point(p) for p in P)+';']
proof=[]
for w,style in [(F(0),'dotted'),(F(1),''),(F(4),'dashed')]:
    S=segments(U,H(w),3);nc=check(U,H(w),3,S,steps=7);paths=[p for ss in S for p in approximate(ss['bern'],F(1,200000))]
    lines.extend(cubic_path(p,style) for p in paths)
    proof.append(dict(weight=w,native_checks=nc,paths=len(paths),certified_error_cm=max(p['certified_l1_error'] for p in paths)*2))
    for j in range(101):
        v=F(j,100);b=de_boor(U,tuple((F(i==k),) for i in range(9)),3,v)[0];a=w*b/(1-b+w*b)
        assert C(w,v)==tuple((1-a)*r+a*p for r,p in zip(C(F(0),v),P[k]))
lines.append(r'\draw[book grid] '+point(R)+'--'+point(P[k])+';')
for i,(p,anchor) in enumerate(zip(P,['below','below','right','left','above','above right','right','below','above left'])):
    lines.append(r'\draw '+point(p)+r' circle[radius=1.5pt] node['+anchor+r'=6pt] {$P_{'+str(i)+'}$};')
for name,p,anchor in [('R',R,'below right'),('M',M,'right'),('P',A,'above left')]:
    lines.append(r'\draw '+point(p)+r' circle[radius=2pt] node['+anchor+r'=8pt] {$'+name+'$};')
lines.append(r'\node[align=left,anchor=north west] at (.1,6.6) {$w_4=0:\ \mathrm{dotted}$\\$w_4=1:\ \mathrm{solid}$\\$w_4=4:\ \mathrm{dashed}$};')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch11/fig_11_12.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/weight-cross-ratio-check.json').write_text(json.dumps(dict(controls=P,knots=U,parameter=u,R=R,M=M,P=A,s=s,t=t,cross_ratio=4,exact_perspective_identities=303,proofs=proof,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8')
print('PASS11.10:303 exact perspective identities, exact crossratio4; certified rational native paths.')
