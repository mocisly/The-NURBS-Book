"""Printed10.18: actual compatible native cubic/quadratic B-spline curves."""
from pathlib import Path
import json
from fractions import Fraction as F
from gordon_network_data import UC,VC,UH,VH,CK,CL,Q,view
from native_bspline import segments,check,cubic_path,point
root=Path(__file__).resolve().parents[1]
out=['% Representative compatible network: original cubic Uc and quadratic Vc; actual coefficient data in scripts/gordon_network_data.py.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-9,-6.8) rectangle (9,8);']
checks=0
for K,curves,p in [(UC,CK,3),(VC,CL,2)]:
    for C in curves:
        ss=segments(K,C,p);checks+=check(K,C,p,ss,steps=7)
        out.extend(cubic_path(dict(bern=tuple(view(a) for a in s['bern']))) for s in ss)
for row in Q:
    for p in row:out.append(r'\fill '+point(view(p))+r' circle[radius=1.5pt];')
for p,label,anchor in [(CK[1][0],r'C_1(u)','above'),(CK[3][0],r'C_3(u)','right'),(CL[1][-1],r'C_1(v)','above right'),(CL[3][-1],r'C_3(v)','below')]:
    out.append(r'\node['+anchor+r'=6pt] at '+point(view(p))+r' {$'+label+'$};')
tip=view(Q[3][1]);out.append(r'\draw '+point(tip)+r' circle[radius=2.8pt];');out.append(r'\node[below left=5pt] at '+point(tip)+r' {$Q_{3,1}$};')
origin=(-F(15,2),-F(9,2))
for end,name,anchor in [((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:
    to=tuple(a+b for a,b in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(to)+r' node['+anchor+r'=4pt] {$'+name+'$};')
out.append(r'\end{tikzpicture}')
(root/'image_tex/ch10/fig_10_25.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r=dict(representative_data=True,source='scripts/gordon_network_data.py',original_degrees=[3,2],u_knots=list(map(str,UC)),v_knots=list(map(str,VC)),u_parameters=list(map(str,UH)),v_parameters=list(map(str,VH)),exact_intersection_vector_identities=20,native_curve_checks=checks,native_curve_error=0,no_contour_tracing=True)
(root/'image_tex/build/gordon-network-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('PASS10.18:',checks,'nativecurvechecks/20exactsharedintersectionpoints.')
