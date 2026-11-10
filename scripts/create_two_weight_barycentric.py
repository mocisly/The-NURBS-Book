from pathlib import Path
from fractions import Fraction as F
import json
from two_weight_data import *
from native_bspline import segments,check,cubic_path,point
from rational_geometry import approximate
root=Path(__file__).resolve().parents[1];a,b=bary(UBAR,OLD);aa,bb=bary(UBAR,NEW);X,Z=curve(UBAR,OLD),curve(UBAR,NEW);Q=edge(b/(a+b));A,B,C,D=edge(b),edge(1-a),edge(bb),edge(1-aa)
assert X==blend(a,b) and Z==blend(aa,bb)
assert aa/a==bb/b
def cross(v,w):return v[0]*w[1]-v[1]*w[0]
def sub(x,y):return tuple(a-b for a,b in zip(x,y))
assert cross(sub(X,A),sub(R,P[4]))==cross(sub(X,B),sub(R,P[5]))==0
assert cross(sub(Z,C),sub(R,P[4]))==cross(sub(Z,D),sub(R,P[5]))==0
assert cross(sub(Q,R),sub(X,R))==cross(sub(Q,R),sub(Z,R))==0
assert ((1-a-b)/a)/((1-aa-bb)/aa)==NEW[4]/OLD[4]
assert ((1-a-b)/b)/((1-aa-bb)/bb)==NEW[5]/OLD[5]
lines=['% All A/B/C/D/R/Q derived from actual rational basis and barycentric parallel projections.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-.6,-.6) rectangle (9.2,7);',r'\draw[book grid] '+'--'.join(point(p) for p in P)+';'];nc=0;proof=[]
for W,style in [(OLD,''),(NEW,'dashed')]:
    ss=segments(U,homogeneous(W),3);nc+=check(U,homogeneous(W),3,ss,steps=7);paths=[p for s in ss for p in approximate(s['bern'],F(1,200000))];lines.extend(cubic_path(p,style) for p in paths);proof.append(dict(weights=W,screen_error_cm=2*max(p['certified_l1_error'] for p in paths)))
for p,q in [(R,P[4]),(R,P[5]),(R,Q),(X,A),(X,B),(Z,C),(Z,D)]:lines.append(r'\draw[book grid] '+point(p)+'--'+point(q)+';')
for i,(p,anchor) in enumerate(zip(P,['below','below','right','left','above left','above right','right','below','above left'])):lines.append(r'\draw '+point(p)+r' circle[radius=1.5pt] node['+anchor+r'=7pt] {$P_{'+str(i)+'}$};')
for name,p,anchor,sep in [('A',A,'above',5),('C',C,'above',18),('Q',Q,'above',5),('D',D,'above',18),('B',B,'above',5),('R',R,'below',8),('P',X,'below right',8),(r'\widehat P',Z,'below right',18)]:
    lines.append(r'\draw '+point(p)+r' circle[radius=1.8pt] node['+anchor+'='+str(sep)+r'pt] {$'+name+'$};')
lines.append(r'\draw[book axis] '+point(X)+'--'+point(Z)+';');lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch11/fig_11_16.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/two-weight-barycentric-check.json').write_text(json.dumps(dict(controls=P,knots=U,parameter=UBAR,old_weights=OLD,new_weights=NEW,old_barycentric=(a,b),new_barycentric=(aa,bb),auxiliary_points=dict(A=A,B=B,C=C,D=D,R=R,Q=Q,P=X,Phat=Z),exact_parallel_and_barycentric_checks=10,native_checks=nc,proofs=proof,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.14',nc,'nativechecks, exact barycentric/parallel/weight ratio identities.')
