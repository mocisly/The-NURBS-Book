"""Fig5.29: same original curve, five genuine whole-curve tolerance budgets."""
from pathlib import Path
from fractions import Fraction as F
import json
from knot529_data import U,P,OPERATIONS
from tolerance_knot_projection import experiment
from native_bspline import segments,check,cubic_path,point,de_boor,number
from knot51_data import insert

root=Path(__file__).resolve().parents[1];targets=[root/f'image_tex/ch05/fig_5_{n}.tex' for n in (39,40,41)]
assert not any(p.exists() for p in targets)
tolerances=tuple(F(t) for t in ('0.007','0.025','0.07','0.6','1.2'))
results=experiment(U,P,3,tolerances);states=[(U,P)]+[(K,Q) for K,Q,r in results]
assert [len(Q) for K,Q in states]==[11,10,8,7,6,5]
original=segments(U,P,3);checks=check(U,P,3,original);reports=[]
for (K,Q,proof),tolerance in zip(results,tolerances):
    checks+=check(K,Q,3,segments(K,Q,3));W,R=K,Q
    removed=tuple(F(r['removed']) for r in proof['removal_history'])
    assert sorted(removed)==sorted(set(U)-set(K))
    for t in sorted(removed):W,R,_=insert(W,R,3,t)
    assert W==U and Q[0]==P[0] and Q[-1]==P[-1]
    errors=tuple(tuple(a-b for a,b in zip(x,y)) for x,y in zip(P,R))
    bound=F(proof['certified_whole_domain_L1_error_bound_cm']);assert bound<=tolerance
    maximum=F(0)
    for i in range(201):
        t=F(i,200);old=de_boor(U,P,3,t);new=de_boor(K,Q,3,t);delta=tuple(a-b for a,b in zip(old,new))
        assert delta==de_boor(U,errors,3,t)
        error=sum(map(abs,delta));assert error<=bound<=tolerance;maximum=max(maximum,error)
    reports.append(dict(proof,U=list(map(str,K)),controls=[[str(t) for t in pt] for pt in Q],
                        common_basis_error_identity_points=201,sampled_max_L1_error_cm=str(maximum)))
panels=[]
for index,(K,Q) in enumerate(states):
    lines=[r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';']
    for s in original:lines.append(cubic_path(s,'book grid,dashed'))
    if index:
        lines.append(r'\draw[book grid] '+'--'.join(map(point,Q))+';')
        for s in segments(K,Q,3):lines.append(cubic_path(s,'book line'))
    for pt in Q:lines.append(r'\draw '+point(pt)+' circle[radius=1.6pt];')
    lines.append(r'\draw[book grid] (0,-1.35)--(11,-1.35);')
    for t in sorted(set(U)):
        m=U.count(t)
        for j in range(m):
            x=11*t+F(1,10)*(F(j)-F(m-1,2))
            lines.append(r'\draw[book grid] '+point((x,F(-29,20)))+'--'+point((x,F(-5,4)))+';')
        if t not in K:lines.append(r'\draw[book line] '+point((11*t,F(-27,20)))+' circle[radius=3pt];')
    label='('+chr(97+index)+')'
    if index:label+=r'\quad $\varepsilon='+('0.007','0.025','0.07','0.6','1.2')[index-1]+r'$'
    lines.append(r'\node at (5.5,-2.15) {'+label+'};');panels.append(lines)
for pair,target in enumerate(targets):
    high=max(max(pt[1] for pt in states[i][1]) for i in (pair*2,pair*2+1))+F(7,10)
    high=max(high,max(pt[1] for pt in P)+F(7,10))
    lines=['% Fig5.29: exact printed knots and one explicit representative hooked cubic.',
           '% Five separate inverse-insertion experiments use the SAME original curve and data-unit scale.',
           '% Every global L1 error bound <= displayed epsilon; circled bar nodes equal actual removed knot set.',
           '% Representative multiscale control coordinates documented in knot529_data.py and report.',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.6,-2.8) rectangle (30,'+number(high)+');']
    for panel,shift in ((2*pair,0),(2*pair+1,F(79,5))):
        lines+=[r'\begin{scope}[xshift='+number(shift)+'cm]']+panels[panel]+[r'\end{scope}']
    lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/tolerance-knot-removal-check.json').write_text(json.dumps({
    'figure':'5.29','degree':3,'original_U':list(map(str,U)),
    'representative_original_controls':[[str(t) for t in pt] for pt in P],
    'representative_data_construction':OPERATIONS,
    'all_experiments_start_from_same_original':True,'control_counts':[len(Q) for K,Q in states],
    'all_native_curve_checks':checks,'whole_domain_error_budget_not_stepwise_budget':True,
    'native_exact_cubic_geometry':True,'tolerance_experiments':reports},indent=2)+'\n')
print('PASS:'+str(checks)+' exact native checks,1005 common-basis error identities; control counts11/10/8/7/6/5, all five certified whole-curve bounds within displayed tolerances.')
