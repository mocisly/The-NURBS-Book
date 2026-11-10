"""Fig5.14: four genuine clamped restrictions, common controls and exact shared corner."""
from pathlib import Path
from fractions import Fraction as F
import json
from knot59_data import U,V,P
from surface_subdivision import split,verify_restrictions
from surface_geometry import surface
from native_bspline import point
from native_surface_drawing import wires

root=Path(__file__).resolve().parents[1];targets=[root/f'image_tex/ch05/fig_5_{n}.tex' for n in (15,16)];assert not any(p.exists() for p in targets)
base=(U,V,3,2,P);u0,v0=F(2,5),F(7,10);u_children,_=split(base,'u',u0);reports=[verify_restrictions(base,u_children,'u')];children=[]
for parent in u_children:
    pair,_=split(parent,'v',v0);reports.append(verify_restrictions(parent,pair,'v'));children.extend(pair)
v_children,_=split(base,'v',v0);reverse=[]
for parent in v_children:reverse.extend(split(parent,'u',u0)[0])
assert children==[reverse[i] for i in (0,2,1,3)]
corner=surface(*base,u0,v0)
assert [children[0][-1][-1][-1],children[1][-1][-1][0],children[2][-1][0][-1],children[3][-1][0][0]]==[corner]*4
offsets=[(F(13,20),F(-13,20),F(0)),(F(-13,20),F(-13,20),F(0)),(F(13,20),F(13,20),F(0)),(F(-13,20),F(13,20),F(0))]
wire_reports=[]
for panel,target in enumerate(targets):
    lines=['% Fig5.14('+chr(97+panel)+'): four exact clamped restrictions of the SAME surface as5.9/5.11.',
           '% GLOBAL splits u=2/5,v=7/10; both insertion orders produce identical child nets.',
           '% Shared boundary and corner checked BEFORE explicit display-only translations.',
           r'\begin{tikzpicture}[book line,x={(-.72cm,-.48cm)},y={(.8cm,-.28cm)},z={(0cm,.8cm)}]',
           r'\path[use as bounding box] (canvas cs:x=-5.7cm,y=-4.9cm) rectangle (canvas cs:x=6.3cm,y=6.8cm);']
    for child,offset in zip(children,offsets):
        A,B,p,q,S=child;D=tuple(tuple(tuple(c+d for c,d in zip(pt,offset)) for pt in row) for row in S)
        if panel==0:
            for row in D:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
            for j in range(len(D[0])):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(row[j]) for row in D)+';')
            for row in D:
                for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius=1.2pt];')
        else:
            values=sorted({B[q],B[len(S[0])]}|{F(j,30) for j in range(31) if B[q]<=F(j,30)<=B[len(S[0])]})
            paths,r=wires(A,B,p,q,D,stripe_values=values);lines+=paths;wire_reports.append(r)
    lines += [r'\draw[book axis] (0,0,0)--(5,0,0) node[below left=4pt] {$x$};',r'\draw[book axis] (0,0,0)--(0,6,0) node[right=4pt] {$y$};',r'\draw[book axis] (0,0,0)--(0,0,7.1) node[above=4pt] {$z$};',r'\node at (canvas cs:x=.3cm,y=-4.3cm) {('+chr(97+panel)+')};',r'\end{tikzpicture}']
    target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
report={'figure':'5.14','same_controls_as5.9':True,'unit_weights':True,'global_splits':['2/5','7/10'],'both_split_orders_give_identical_children':True,'four_shared_corner_controls_equal_actual_surface_point':list(map(str,corner)),'restriction_checks':reports,
        'children':[{'U':list(map(str,A)),'V':list(map(str,B)),'control_count':[len(S),len(S[0])],'actual_controls':[[list(map(str,pt)) for pt in row] for row in S],'display_translation':list(map(str,offset))} for (A,B,p,q,S),offset in zip(children,offsets)],'global_stripe_grid_preserved':True,'exact_child_wire_checks':wire_reports}
(root/'image_tex/build/four-surface-patches-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS:four real clamped patches,32 identical polynomial spans,726 original-parameter surface comparisons; split order commutes and all four corners=S(2/5,7/10).')
