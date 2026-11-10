from pathlib import Path
from fractions import Fraction as F
import json
from periodic_curve_data import K as ORIGINAL_K,P as ORIGINAL_P
from unclamped_geometry import verified_segments
from bspline_math import piece
from native_bspline import cubic_path,point
from inverse_knot_projection import solve
root=Path(__file__).resolve().parents[1];reference,_=verified_segments(ORIGINAL_K,ORIGINAL_P,3)
KS=[(F(3),)*4+tuple(F(i)for i in range(4,8))+(F(8),)*4,tuple(map(F,('0','.5','2.3','3','4','5','6','7','8','8.7','10.5','11'))),ORIGINAL_K]
reports=[]
for j,K in enumerate(KS):
    A=[];D=[]
    for s,ref in zip(range(3,8),reference):
        assert (K[s],K[s+1])==(ref['a'],ref['b'])
        bs=[piece(K,i,3,s)for i in range(8)]
        for k in range(4):A.append(tuple(c[k]if k<len(c)else F(0)for c in bs));D.append(tuple(c[k]for c in ref['power']))
    G=tuple(tuple(sum(row[i]*row[k]for row in A)for k in range(8))for i in range(8));B=tuple(tuple(sum(row[i]*q[d]for row,q in zip(A,D))for d in range(2))for i in range(8));P=solve(G,B)
    assert all(tuple(sum(row[i]*P[i][d]for i in range(8))for d in range(2))==q for row,q in zip(A,D))
    ss,n=verified_segments(K,P,3)
    assert all(a['power']==b['power']for a,b in zip(ss,reference))
    if j==0:assert P[0]==P[-1]
    if j==1:assert all(P[i]!=P[i+5]for i in range(3))
    if j==2:assert P==ORIGINAL_P
    out=[r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-2.65,-2.5) rectangle (2.65,2.2);',r'\draw[book grid,dashed] '+'--'.join(point(q)for q in P)+';'];out.extend(cubic_path(s)for s in ss)
    indices=range(7)if j==0 else range(5)if j==2 else range(8)
    for i in indices:
        label='P_'+str(i)
        if j==0 and i==0:label+='=P_7'
        if j==2 and i<3:label+='=P_'+str(i+5)
        anchor={0:'above left=7pt',1:'left=7pt',2:'below=7pt',3:'right=7pt',4:'above=7pt',5:'above right=7pt',6:'left=7pt',7:'below left=7pt'}[i]
        if j==0:anchor={0:'left=7pt',1:'below left=7pt',2:'below=7pt',3:'right=7pt',4:'above=7pt',5:'above=7pt',6:'above left=7pt'}[i]
        out.append(r'\draw[book grid] '+point(P[i])+r' circle[radius=1.6pt] node['+anchor+r'] {$'+label+'$};')
    out.extend([r'\node at (0,-2.3) {('+chr(97+j)+')};',r'\end{tikzpicture}']);name=('fig_12_03','fig_12_04','fig_12_03c')[j]
    (root/f'image_tex/ch12/{name}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8');reports.append(dict(knots=K,controls=P,native_checks=n,whole_polynomial_vector_identities=len(A),exact_same_curve=True,wrapped=j==2))
(root/'image_tex/build/unclamping-comparison-check.json').write_text(json.dumps(dict(reference_knots=ORIGINAL_K,reference_controls=ORIGINAL_P,cases=reports,total_whole_vector_coefficient_identities=60,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS3printed knot vectors;60WHOLE vector coefficient identities; SAMEcurve; C2closure unchanged; Bnotwrapped/Cwrapped.')
