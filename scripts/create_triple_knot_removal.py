"""Fig5.26: exact removal of a triple knot from one cubic polynomial curve."""
from pathlib import Path
from fractions import Fraction as F
import json
from knot51_data import insert
from native_bspline import segments,check,cubic_path,point,de_boor

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_33.tex';assert not target.exists()
baseU=(F(0),)*4+(F(2),)*4
baseP=tuple(tuple(F(str(t)) for t in pt) for pt in [(1,0),(0,5.5),(10,6.3),(9,0)])
insertions=[(baseU,baseP)];U,P=baseU,baseP
for repeat in range(3):
    U,P,_=insert(U,P,3,F(1));insertions.append((U,P))
stages=list(reversed(insertions));R=[p for k,p in stages]
assert [len(p) for p in R]==[7,6,5,4]
blend=lambda a,b:tuple((x+y)/2 for x,y in zip(a,b))
twice_minus=lambda a,b:tuple(2*x-y for x,y in zip(a,b))
# Independent inward recovery using the three equation systems in the prose.
assert R[0][3]==blend(R[1][2],R[1][3])                           #5.25
qleft=twice_minus(R[1][2],R[2][1]);qright=twice_minus(R[1][3],R[2][3])
assert qleft==qright==R[2][2]                                  #5.26
q1=twice_minus(R[2][1],R[3][0]);q2=twice_minus(R[2][3],R[3][3])
assert q1==R[3][1] and q2==R[3][2] and R[2][2]==blend(q1,q2)    #5.27
rootspan=segments(baseU,baseP,3)[0];checks=points=0
for K,Q in stages:
    ss=segments(K,Q,3);checks+=check(K,Q,3,ss)
    for s in ss:assert s['power']==rootspan['power']
    for k in range(201):
        u=F(k,100);assert de_boor(K,Q,3,u)==de_boor(baseU,baseP,3,u);points+=1
# Label identities are actual equalities, not coincident-looking projections.
assert R[0][0]==R[3][0] and R[0][6]==R[3][3]
assert R[0][1]==R[1][1]==R[2][1]
assert R[0][2]==R[1][2] and R[0][4]==R[1][3]
assert R[0][5]==R[1][4]==R[2][3]
lines=['% Fig5.26: one representative cubic Bezier with knot1 inserted three times, then removed exactly.',
       '% Every P_i^t and label equality computed in exact rational arithmetic.',
       '% All four stages are the SAME global polynomial and parameterization on[0,2].',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-3.4,-3.7) rectangle (14,7.2);']
for index,Q in enumerate(R):
    style=('book grid' if index<2 else 'book grid,dashed' if index==2 else 'book grid,dash dot')
    lines.append(r'\draw['+style+'] '+'--'.join(map(point,Q))+';')
lines.append(cubic_path(rootspan))
for pt in R[0]:lines.append(r'\fill '+point(pt)+' circle[radius=1.7pt];')
for pt in (R[2][2],R[3][1],R[3][2]):lines.append(r'\draw '+point(pt)+' circle[radius=1.8pt];')
labels=[(R[0][0],r'\mathbf P_0^0=\mathbf P_0^3','below left=6pt'),
        (R[0][6],r'\mathbf P_6^0=\mathbf P_3^3','below right=6pt'),
        (R[0][1],r'\mathbf P_1^2=\mathbf P_1^1=\mathbf P_1^0','left=6pt'),
        (R[0][2],r'\mathbf P_2^1=\mathbf P_2^0','above left=6pt'),
        (R[0][3],r'\mathbf P_3^0','below=7pt'),
        (R[0][4],r'\mathbf P_4^0=\mathbf P_3^1','above right=6pt'),
        (R[0][5],r'\mathbf P_5^0=\mathbf P_4^1=\mathbf P_3^2','right=6pt'),
        (R[2][2],r'\mathbf P_2^2','above=7pt'),
        (R[3][1],r'\mathbf P_1^3','above left=7pt'),
        (R[3][2],r'\mathbf P_2^3','above right=7pt')]
for pt,label,pos in labels:lines.append(r'\node['+pos+'] at '+point(pt)+' {$'+label+'$};')
lines.append(r'\draw[book grid] (1,-2.35)--(10,-2.35);')
for u,m,label in [(F(0),4,r'u_0=u_1=u_2=u_3'),(F(1),3,r'u_4=u_5=u_6'),(F(2),4,r'u_7=u_8=u_9=u_{10}')]:
    x=1+F(9,2)*u
    for j in range(m):
        xx=x+F(1,10)*(F(j)-F(m-1,2))
        lines.append(r'\draw[book grid] '+point((xx,F(-49,20)))+'--'+point((xx,F(-9,4)))+';')
    lines.append(r'\node[below=7pt] at '+point((x,F(-47,20)))+' {$'+label+'$};')
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/triple-knot-removal-check.json').write_text(json.dumps({
    'figure':'5.26','degree':3,'original_U':['0']*4+['1']*3+['2']*4,
    'representative_global_bezier_controls':[[str(t) for t in pt] for pt in baseP],
    'removal_stages':[{'t':i,'U':list(map(str,K)),'controls':[[str(t) for t in pt] for pt in Q]} for i,(K,Q) in enumerate(stages)],
    'three_removal_equation_systems525526527_satisfied_exactly':True,
    'all_labeled_control_equalities_exact':True,'all_global_power_coefficients_identical':True,
    'native_cubic_checks':checks,'exact_parameterization_invariance_points':points,
    'example_all_three_knots_removable_not_a_claim_for_arbitrary_triple_knots':True},indent=2)+'\n')
print('PASS:287 exact native checks,804 parameter-invariance points;5.25/5.26/5.27 inward recovery exact; all control label identities exact.')
