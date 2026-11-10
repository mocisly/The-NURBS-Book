"""Fig5.35: exact, sequential cubic extraction/elevation/knot removal.

The printed knot vector is exact. Coordinates are an explicit representative
six-point arch; no coordinates or contours are extracted from the bitmap.
Intermediate mixed-degree nets are labelled as processing states, not asserted
to be a single uniform-degree B-spline.
"""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from knot51_data import insert
from rational_geometry import elevate,evaluate
from inverse_knot_projection import remove_to

root=Path(__file__).resolve().parents[1]
U=(F(0),)*4+(F('.3'),F('.7'))+(F(1),)*4
P=tuple(tuple(F(str(t)) for t in q) for q in [(0,0),(-1.5,4),(1.5,8),(8.5,8),(11.5,4),(10,0)])
ss=segments(U,P,3);checks=check(U,P,3,ss)
B=[s['bern'] for s in ss];E=[elevate(b) for b in B]
K,Q=U,P
for repeat in range(2):K,Q,_=insert(K,Q,3,F('.3'))
first_refined=Q
for repeat in range(2):K,Q,_=insert(K,Q,3,F('.7'))
assert Q==B[0]+B[1][1:]+B[2][1:]
two=E[0]+E[1][1:]
K2=(F(0),)*5+(F('.3'),)*4+(F('.7'),)*5
Kf,Qf,proofa=remove_to(K2,two,4,[F('.3')]*2)
assert proofa['curve_exactly_unchanged'] and len(Qf)==7
Qg=Qf+E[2][1:];Kg=Kf[:-5]+(F('.7'),)*4+(F(1),)*5
Kh,Qh,proofb=remove_to(Kg,Qg,4,[F('.7')]*2)
assert proofb['curve_exactly_unchanged'] and len(Qh)==9
assert Kh==(F(0),)*5+(F('.3'),)*2+(F('.7'),)*2+(F(1),)*5
states=[P,first_refined,E[0]+first_refined[4:],E[0]+Q[4:],two+B[2][1:],Qf+B[2][1:],Qg,Qh]
assert list(map(len,states))==[6,8,9,11,12,10,11,9]
comparisons=0
for s,b,e in zip(ss,B,E):
    for i in range(101):
        t=F(i,100);u=s['a']+(s['b']-s['a'])*t
        assert evaluate(b,t)==evaluate(e,t)==de_boor(U,P,3,u)
        comparisons+=1
for KK,QQ in [(Kf,Qf),(Kg,Qg),(Kh,Qh)]:
    quartic=segments(KK,QQ,4);checks+=check(KK,QQ,4,quartic)
    for s in quartic:
        ref=next(c for c in ss if c['a']==s['a'] and c['b']==s['b'])
        assert all(tuple(a)+(F(0),)==tuple(b) for a,b in zip(ref['power'],s['power']))
        for i in range(101):
            u=s['a']+(s['b']-s['a'])*F(i,100)
            assert de_boor(KK,QQ,4,u)==de_boor(U,P,3,u);comparisons+=1
titles=[r'$p=3$',r'$u_a:\ 1\to3$',r'$[0,u_a]:\ 3\to4$',r'$u_b:\ 1\to3$',r'$[u_a,u_b]:\ 3\to4$',r'$u_a:\ 4\to2$',r'$[u_b,1]:\ 3\to4$',r'$u_b:\ 4\to2$']
manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for pair in range(4):
    target=root/f'image_tex/ch05/fig_5_{47+pair}.tex'
    assert not next(e for e in manifest['images'] if e['tex']==str(target.relative_to(root)).replace('\\','/'))['applied']
    lines=['% Semantic degree-elevation states; exact arithmetic, common invariant cubic geometry.',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-2.3,-2.1) rectangle (26.6,8.8);']
    for col in range(2):
        j=2*pair+col
        lines.append(r'\begin{scope}[xshift='+str(14.6*col)+r'cm]')
        lines.append(r'\draw[book grid] '+'--'.join(map(point,states[j]))+';')
        for s in ss:lines.append(cubic_path(s))
        for q in states[j]:lines.append(r'\draw[fill=none] '+point(q)+r' circle[radius=1.8pt];')
        for t in (F('.3'),F('.7')):
            x,y=de_boor(U,P,3,t);r=F(2,25)
            lines.append(r'\draw '+point((x-r,y))+r'--'+point((x+r,y))+' '+point((x,y-r))+'--'+point((x,y+r))+';')
        lines.append(r'\node at (5,-.75) {('+chr(97+j)+') '+titles[j]+'};')
        lines.append(r'\node at (5,-1.5) {$N='+str(len(states[j]))+(r',\quad p=4,\quad C^2' if j==7 else '')+'$};')
        lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
report={'figure':'5.35','representative_controls':[[str(t) for t in q] for q in P],
        'original_knots':list(map(str,U)),'final_knots':list(map(str,Kh)),
        'state_control_counts':list(map(len,states)),
        'state_controls':[[[str(t) for t in q] for q in state] for state in states],
        'native_checks':checks,'exact_invariance_comparisons':comparisons,
        'all_quartic_global_power_coefficients_equal_original_cubic_with_zero_quartic_term':True,
        'two_ua_removals':proofa,'two_ub_removals':proofb,
        'intermediate_nets_are_mixed_degree_processing_states':True}
(root/'image_tex/build/degree-elevation-stages-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'PASS: {checks} native checks, {comparisons} exact invariance comparisons; both pairs of knots removed with zero residual.')
