"""Printed11.5: inserting an existing quadratic knot then moving its new control."""
from pathlib import Path
from fractions import Fraction as F
import json
from knot51_data import insert
from native_bspline import segments,check,cubic_path,point,de_boor
from bspline_math import derivative,evaluate
root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'));assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch11/fig_11_05.tex')['applied']
U=(F(0),)*3+(F(1,4),F(1,2),F(3,4))+(F(1),)*3
P=tuple(tuple(map(F,a)) for a in [(0,0),('1.75','.6'),('1.75',3),('6.25',3),('6.25','.6'),(8,0)])
gre=tuple(sum(U[i+1:i+3])/2 for i in range(6));assert gre==(0,F(1,8),F(3,8),F(5,8),F(7,8),1)
K,Q,alpha=insert(U,P,2,F(1,2));assert K.count(F(1,2))==2 and Q[2]==P[2] and Q[4]==P[3] and Q[3]==de_boor(U,P,2,F(1,2))
assert sum(K[4:6])/2==F(1,2)
delta=(F(0),-F(9,5));R=tuple(tuple(a+b for a,b in zip(q,delta)) if i==3 else q for i,q in enumerate(Q));BASIS=tuple((F(i==3),) for i in range(7));assert de_boor(K,BASIS,2,F(1,2))==(F(1),)
original,refined,modified,basis=(segments(k,c,2) for k,c in [(U,P),(K,Q),(K,R),(K,BASIS)])
identity=local=0
for a,b,c in zip(refined,modified,basis):
    old=next(s for s in original if s['a']<=a['a'] and a['b']<=s['b']);assert old['power']==a['power'];identity+=6
    for axis in (0,1):assert all(v-u==delta[axis]*n for u,v,n in zip(a['power'][axis],b['power'][axis],c['power'][0]));local+=3
def sides(ss):
    left=next(s for s in ss if s['b']==F(1,2));right=next(s for s in ss if s['a']==F(1,2))
    assert tuple(evaluate(c,F(1,2)) for c in left['power'])==tuple(evaluate(c,F(1,2)) for c in right['power'])
    return tuple(tuple(evaluate(derivative(c),F(1,2)) for c in s['power']) for s in (left,right))
old_l,old_r=sides(refined);new_l,new_r=sides(modified);assert old_l==old_r and new_l!=new_r;det=new_l[0]*new_r[1]-new_l[1]*new_r[0];assert det!=0
out=['% Exact repeated-knot quadratic example: insertion preserves C1 geometry; relocation creates actual tangent jump.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm]',r'\path[use as bounding box] (-.7,-.8) rectangle (8.7,3.8);'];nc=lines=0
out.append(r'\draw[book grid] '+'--'.join(point(a) for a in P)+';');out.append(r'\draw[book grid,dashed] '+point(Q[2])+'--'+point(R[3])+'--'+point(Q[4])+';')
for t in (F(1,4)+F(i,72) for i in range(1,36)):
    if t==F(1,2):continue
    a,b=de_boor(K,Q,2,t),de_boor(K,R,2,t)
    if a==b:continue
    assert a[0]==b[0];out.append(r'\draw[book grid] '+point(a)+'--'+point(b)+';');lines+=1
for C,style in [(Q,''),(R,'dashed')]:
    ss=segments(K,C,2);nc+=check(K,C,2,ss,steps=7);out.extend(cubic_path(s,style) for s in ss)
for a in P:out.append(r'\draw '+point(a)+r' circle[radius=1.4pt];')
for pos,label,anchor in [(Q[2],'P_2=Q_2','above left'),(Q[4],'P_3=Q_4','above right'),(Q[3],'Q_3','above')]:out.append(r'\node['+anchor+r'=8pt] at '+point(pos)+r' {$'+label+'$};')
out.extend([r'\draw '+point(Q[3])+r' circle[radius=1.7pt];',r'\draw[book axis] '+point(Q[3])+'--'+point(R[3])+';',r'\draw '+point(R[3])+r' circle[radius=2pt] node[below=8pt] {$\widehat Q_3$};',r'\end{tikzpicture}'])
(root/'image_tex/ch11/fig_11_05.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r=dict(degree=2,original_knots=U,original_controls=P,original_greville=gre,inserted_existing_knot=F(1,2),new_knots=K,inserted_controls=Q,modified_controls=R,delta_control=delta,new_greville_3=F(1,2),basis_at_selected=1,original_exact_left_right_derivative=(old_l,old_r),modified_exact_left_right_derivative=(new_l,new_r),modified_tangent_determinant=det,position_continuous=True,whole_insertion_power_coefficient_identities=identity,whole_relocation_power_coefficient_identities=local,native_curve_checks=nc,actual_vertical_displacements=lines,native_curve_error=0,no_contour_tracing=True)
(root/'image_tex/build/quadratic-relocation-corner-check.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.5:',identity,'insertion/',local,'relocationcoefidentities;',nc,'nativechecks;C1before/actualcornerafter;tangentdet',det)
