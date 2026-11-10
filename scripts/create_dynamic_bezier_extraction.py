"""Fig5.22: real two-step cubic extraction and next-segment work array."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from knot51_data import insert

root=Path(__file__).resolve().parents[1];targets=[root/f'image_tex/ch05/fig_5_{n}.tex' for n in (27,28)]
assert not any(p.exists() for p in targets)
U=(F(0),)*4+(F(1,3),F(2,3))+(F(1),)*4
P=tuple(tuple(F(str(t)) for t in pt) for pt in [(0,0),(3,1),(1.5,5.5),(7.5,5.5),(6,1.3),(9,0)])
ss=segments(U,P,3);proof=check(U,P,3,ss);a=F(1,3)
blend=lambda x,y,t:tuple((1-t)*c+t*d for c,d in zip(x,y))
initial=P[:4]
first=initial[:2]+(blend(P[1],P[2],F(1,2)),blend(P[2],P[3],F(1,3)))
second=first[:3]+(blend(first[2],first[3],F(1,2)),)
next_work=(second[3],first[3],P[3],P[4])
assert second==ss[0]['bern'] and second[-1]==ss[1]['bern'][0]==de_boor(U,P,3,a)
assert next_work[1]==ss[1]['bern'][1]
K1,R1,_=insert(U,P,3,a);K2,R2,_=insert(K1,R1,3,a)
assert R2[:4]==second and R2[3:7]==next_work
for K,R in ((K1,R1),(K2,R2)):
    ss2=segments(K,R,3);proof+=check(K,R,3,ss2)
    for s,t in zip(ss,ss2):assert s['power']==t['power']
    for k in range(101):assert de_boor(K,R,3,F(k,100))==de_boor(U,P,3,F(k,100))
states=(initial,first,second,next_work);knots=(U,K1,K2,K2)

def node(pt,label,position):return r'\node['+position+'] at '+point(pt)+' {$'+label+'$};'
def bar(K,arrows):
    lines=[r'\draw[book grid] (0,-1.8)--(9,-1.8);']
    for u in sorted(set(K)):
        m=K.count(u)
        for j in range(m):
            x=9*u+F(11,100)*(F(j)-F(m-1,2))
            lines.append(r'\draw[book grid] '+point((x,F(-19,10)))+'--'+point((x,F(-17,10)))+';')
    for j in range(arrows):
        x=9*a+F(22,100)*(F(j)-F(arrows-1,2))
        lines.append(r'\draw[book axis] '+point((x,F(-6,5)))+'--'+point((x,F(-33,20)))+';')
    return lines

panels=[]
for index,(work,K) in enumerate(zip(states,knots)):
    lines=[r'\draw[book grid] '+'--'.join(map(point,P))+';']
    for s in ss:lines.append(cubic_path(s))
    if index:lines.append(r'\draw[book grid] '+'--'.join(map(point,work))+';')
    # Previous work edges remain visible, as in the original construction diagram.
    if index>=2:lines.append(r'\draw[book grid] '+point(first[2])+'--'+point(first[3])+';')
    points=set(P)|set(work)
    if index>=2:points|=set(first)
    for pt in sorted(points):lines.append(r'\draw '+point(pt)+' circle[radius=1.6pt];')
    if index==0:
        for j,pos in enumerate(('below left=5pt','below right=5pt','above=6pt','above=6pt')):
            lines.append(node(P[j],r'\mathbf P_'+str(j)+r'=\mathbf Q_'+str(j)+'^0',pos))
        lines += [node(P[4],r'\mathbf P_4','left=5pt'),node(P[5],r'\mathbf P_5','below right=5pt')]
    elif index in (1,2):
        lines += [node(P[0],r'\mathbf P_0=\mathbf Q_0^0','below left=5pt'),
                  node(P[1],r'\mathbf P_1=\mathbf Q_1^0','below right=5pt'),
                  node(first[2],r'\mathbf Q_2^0','left=6pt')]
        lines.append(node(first[3],r'\mathbf Q_3^0=\mathbf Q_1^1' if index==1 else r'\mathbf Q_1^1','above=6pt'))
        if index==2:
            lines += [r'\draw[book grid] '+point(second[3])+r'--(4.2,3.8);',
                      r'\node[right=3pt] at (4.2,3.8) {$\mathbf Q_3^0=\mathbf Q_0^1$};']
    else:
        lines += [node(next_work[1],r'\mathbf Q_1^1','above=6pt'),
                  node(next_work[2],r'\mathbf Q_2^1=\mathbf P_3','above=6pt'),
                  node(next_work[3],r'\mathbf Q_3^1=\mathbf P_4','below left=6pt'),
                  r'\draw[book grid] '+point(next_work[0])+r'--(4.2,3.8);',
                  r'\node[right=3pt] at (4.2,3.8) {$\mathbf Q_0^1$};']
    lines+=bar(K,0 if index in (0,3) else index)
    lines += [r'\node at (4.5,-2.65) {('+chr(97+index)+')};'];panels.append(lines)
for pair,target in enumerate(targets):
    lines=['% Fig5.22: semantic work arrays from exact cubic knot insertion.',
           '% Representative U=0^4,1/3,2/3,1^4; same curve in all panels.',
           '% Q lower index is local control index, upper index is Bezier segment.',
           '% Initial Q entries in(a),(b),(d) are work entries, not all final Bezier controls.',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-1.5,-3.1) rectangle (25,6.6);']
    for panel,shift in ((2*pair,0),(2*pair+1,14)):
        lines+=[r'\begin{scope}[xshift='+str(shift)+'cm]']+panels[panel]+[r'\end{scope}']
    lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/dynamic-bezier-extraction-check.json').write_text(json.dumps({
    'figure':'5.22','degree':3,'U':list(map(str,U)),
    'representative_control_points':[[str(t) for t in pt] for pt in P],
    'native_curve_checks':proof,'curve_invariance_points':202,'unchanged_global_polynomial_spans':6,
    'work_arrays':[[list(map(str,pt)) for pt in work] for work in states],
    'two_insertions_at':'1/3','alphas_first_round':['1/2','1/3'],'alpha_second_round':'1/2',
    'first_final_bezier_controls_equal_extraction_exactly':True,
    'next_work_array_equals_inserted_controls':True,
    'stored_next_first_tangent_control_equals_next_extracted_control':True,
    'notation':'Q_k^j: local control k=0..3, segment j=0..2; partial work entries are not yet final.'},indent=2)+'\n')
print('PASS:369 native curve checks,202 invariant points,6 exact polynomial spans; final first segment and next work array match independent extraction/insertion.')
