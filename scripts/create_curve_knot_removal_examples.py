"""Fig5.27: one ten-control cubic and four actual approximate knot removals."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from inverse_knot_projection import remove_to
from knot51_data import insert

root=Path(__file__).resolve().parents[1];targets=[root/f'image_tex/ch05/fig_5_{n}.tex' for n in (34,35,36)]
assert not any(p.exists() for p in targets)
U=(F(0),)*4+(F(3,10),)+(F(1,2),)*3+(F(7,10),)*2+(F(1),)*4
P=tuple(tuple(F(str(t)) for t in pt) for pt in [(0,0),(-.3,2),(1.5,4.5),(4,5),(5,4.9),(6,4.6),(6.8,4.2),(7.7,2.2),(7.4,0),(11,0)])
original=segments(U,P,3);checks=check(U,P,3,original);states=[(U,P)];reports=[]
for removed in ((F(3,10),),(F(1,2),),(F(1,2),)*2,(F(1,2),)*3):
    K,Q,report=remove_to(U,P,3,removed);ss=segments(K,Q,3);checks+=check(K,Q,3,ss)
    assert Q[0]==P[0] and Q[-1]==P[-1]
    W,R=K,Q
    for t in sorted(removed):W,R,_=insert(W,R,3,t)
    assert W==U
    errors=tuple(tuple(a-b for a,b in zip(x,y)) for x,y in zip(P,R))
    bound=F(report['certified_whole_domain_L1_error_bound_cm']);assert bound>0
    maximum=F(0);outside=0
    active=[i for i,e in enumerate(errors) if any(e)]
    support=(min(U[i] for i in active),max(U[i+4] for i in active))
    for j in range(201):
        t=F(j,200);old=de_boor(U,P,3,t);new=de_boor(K,Q,3,t)
        difference=tuple(a-b for a,b in zip(old,new))
        assert difference==de_boor(U,errors,3,t)
        error=sum(map(abs,difference));assert error<=bound;maximum=max(maximum,error)
        if t<support[0] or t>support[1]:assert old==new;outside+=1
    report.update(U=list(map(str,K)),controls=[[str(t) for t in pt] for pt in Q],
                  common_basis_error_identity_points=201,sampled_max_L1_error_cm=str(maximum),
                  possible_error_support=list(map(str,support)),outside_support_unchanged_points=outside)
    reports.append(report);states.append((K,Q))
panels=[]
for index,(K,Q) in enumerate(states):
    lines=[]
    if index:
        for s in original:lines.append(cubic_path(s,'book grid,dashed'))
    lines.append(r'\draw[book grid'+(',dashed' if index==0 else '')+'] '+'--'.join(map(point,Q))+';')
    for s in segments(K,Q,3):lines.append(cubic_path(s,'book line'))
    for pt in Q:lines.append(r'\draw '+point(pt)+' circle[radius=1.6pt];')
    lines.append(r'\draw[book grid] (0,-1.35)--(11,-1.35);')
    for t in sorted(set(K)):
        m=K.count(t)
        for j in range(m):
            x=11*t+F(1,10)*(F(j)-F(m-1,2))
            lines.append(r'\draw[book grid] '+point((x,F(-29,20)))+'--'+point((x,F(-5,4)))+';')
    lines.append(r'\node at (5.5,-2.05) {('+chr(97+index)+')};');panels.append(lines)
for target,index in zip(targets,range(3)):
    lines=['% Fig5.27: independent removals from SAME representative ten-control cubic.',
           '% Original has three central1/2 knots: ten circles and three bar ticks confirm caption OCR correction.',
           '% Approximation is local least-squares inverse insertion, unaffected controls fixed.',
           '% All errors certified in original common basis; never claim exact invariance for these approximate examples.',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.6,-2.5) rectangle ('+('11.6' if index==0 else '24.6')+',5.8);']
    selection=[(0,0)] if index==0 else [(2*index-1,0),(2*index,13)]
    for panel,shift in selection:lines+=[r'\begin{scope}[xshift='+str(shift)+'cm]']+panels[panel]+[r'\end{scope}']
    lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/curve-knot-removal-examples-check.json').write_text(json.dumps({
    'figure':'5.27','degree':3,'original_U':list(map(str,U)),
    'original_representative_controls':[[str(t) for t in pt] for pt in P],
    'original_control_count':10,'original_half_knot_multiplicity':3,
    'all_native_curve_checks':checks,'all_comparisons_start_from_same_original':True,
    'new_control_counts':[len(p) for k,p in states[1:]],'approximate_removals':reports},indent=2)+'\n')
print('PASS:'+str(checks)+' exact native checks,804 common-basis error identities; actual controls10/9/9/8/7, positive certified approximation bounds '+','.join(f"{float(F(r['certified_whole_domain_L1_error_bound_cm'])):.5f}" for r in reports)+'cm.')
