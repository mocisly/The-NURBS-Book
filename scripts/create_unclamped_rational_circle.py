from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from unclamp_algorithm import unclamp
from unclamped_geometry import verified_segments
from bspline_math import evaluate,derivative
from native_bspline import point
root=Path(__file__).resolve().parents[1]
K=(F(0),)*3+(F(1,4),)*2+(F(1,2),)*2+(F(3,4),)*2+(F(1),)*3
P=tuple(tuple(F(x)for x in p)for p in[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1),(1,0)])
# Flatten each exact a+b*w component, w^2=1/2, so A12.1 acts over rational coefficients.
H=tuple(tuple(c for x in q+(F(1),)for c in((F(0),x)if i%2 else(x,F(0))))for i,q in enumerate(P))
U,Q=unclamp(K,H,2)
expected=tuple(map(F,('-1/4','-1/4','0','1/4','1/4','1/2','1/2','3/4','3/4','1','5/4','5/4')));assert U==expected
old,n=verified_segments(K,H,2);new,m=verified_segments(U,Q,2);assert all(a['power']==b['power']for a,b in zip(old,new))
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,b):return(a[0]*b[0]+a[1]*b[1]/2,a[0]*b[1]+a[1]*b[0])
def product(A,B):
    C=[(F(0),F(0))for _ in range(len(A)+len(B)-1)]
    for i,a in enumerate(A):
        for j,b in enumerate(B):C[i+j]=add(C[i+j],mul(a,b))
    return C
circle_checks=0
for s in new:
    pol=[tuple(zip(s['power'][i],s['power'][i+1]))for i in(0,2,4)]
    x,y,w=(product(p,p)for p in pol)
    assert all(add(add(a,b),tuple(-z for z in c))==(0,0)for a,b,c in zip(x,y,w));circle_checks+=len(x)
assert all(evaluate(a,F(0))==evaluate(b,F(1))for a,b in zip(old[0]['power'],old[-1]['power']))
assert any(evaluate(derivative(a),F(0))!=evaluate(derivative(b),F(1))for a,b in zip(old[0]['power'],old[-1]['power']))
D=10**40;t=isqrt(2*D*D);lo,hi=F(t,2*D),F(t+1,2*D);assert lo*lo<F(1,2)<hi*hi;w=(lo+hi)/2
def project(q):
    h=tuple(q[i]+q[i+1]*w for i in(0,2,4));assert h[2]>0;return tuple(x/h[2]for x in h[:2])
controls=tuple(map(project,Q));assert controls[0]!=controls[-1]and controls[1:8]==P[1:8]
out=[r'\begin{tikzpicture}[book line,x=4cm,y=4cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-1.6,-1.55) rectangle (6.15,1.55);']
for panel,poly in enumerate((P,controls)):
    out.append(r'\begin{scope}[shift={'+point((F(22,5)*panel,0))+'}]');out.append(r'\draw (0,0) circle[radius=1];');out.append(r'\draw[book grid,dashed] '+'--'.join(point(q)for q in poly)+';')
    indices=range(8)if panel==0 else range(9)
    for i in indices:
        label='P_'+str(i)+('=P_8'if panel==0 and i==0 else'')
        anchor={0:'right=8pt',1:'above right=6pt',2:'above=6pt',3:'above left=6pt',4:'left=6pt',5:'below left=6pt',6:'below=6pt',7:'below right=6pt',8:'right=8pt'}[i]
        out.append(r'\draw[book grid] '+point(poly[i])+r' circle[radius=1.6pt] node['+anchor+r'] {$'+label+'$};')
    out.extend([r'\node at (0,-1.4) {('+('a'if panel==0 else'b')+')};',r'\end{scope}'])
out.append(r'\end{tikzpicture}');(root/'image_tex/ch12/fig_12_08.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/unclamped-rational-circle-check.json').write_text(json.dumps(dict(algebraic_field='Q[w]/(w^2-1/2),w>0',original_knots=K,original_exact_homogeneous_pair_controls=H,new_knots=U,new_exact_homogeneous_pair_controls=Q,exact_circle_pair_polynomial_identities=circle_checks,whole_homogeneous_vector_coefficient_identities=12,homogeneous_C0_but_not_C1_closure=True,display_weight_interval=(lo,hi),projected_new_controls=controls,new_end_controls_distinct=True,native_checks=n+m,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS exactQ(w)A12.1/printednewU;20circle polynomial identities;12wholehomogeneous vector identities; C0notC1homogeneous/no wrap.')
