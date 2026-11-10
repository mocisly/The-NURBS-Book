"""Fig5.12/5.13: clamped child control nets and genuine separated surface pieces."""
from pathlib import Path
from fractions import Fraction as F
import json,argparse
from knot59_data import U,V,P
from native_bspline import point
from native_surface_drawing import wires
from surface_subdivision import split,verify_restrictions

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--axis',choices=['u','v'],default='u');args=parser.parse_args()
axis=args.axis;value=F(2,5) if axis=='u' else F(7,10);figure='5.12' if axis=='u' else '5.13';source=13 if axis=='u' else 14
root=Path(__file__).resolve().parents[1];target=root/f'image_tex/ch05/fig_5_{source:02}.tex';assert not target.exists()
base=(U,V,3,2,P);children,refined=split(base,axis,value);report=verify_restrictions(base,children,axis)
# Display translations are separate from all exact restriction/continuity checks.
offsets=((F(0),F(-13,20),F(0)),(F(0),F(13,20),F(0))) if axis=='u' else ((F(13,20),F(0),F(0)),(F(-13,20),F(0),F(0)))
lines=['% Fig'+figure+': same representative surface as5.9/5.11, genuine clamped child surfaces.',
       '% Split at GLOBAL '+axis+'='+str(value)+', original parameterization retained; only display translations separate pieces.',
       '% Two equal-camera views: control nets(a), actual exact polynomial isolines(b).',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (canvas cs:x=-11.8cm,y=-4.9cm) rectangle (canvas cs:x=12.2cm,y=6.8cm);']
wire_reports=[]
for panel,xshift in enumerate((-6,6)):
    lines += [r'\begin{scope}[xshift='+str(xshift)+'cm]',r'\begin{scope}[x={(-.72cm,-.48cm)},y={(.8cm,-.28cm)},z={(0cm,.8cm)}]']
    for child,offset in zip(children,offsets):
        A,B,p,q,S=child;display=tuple(tuple(tuple(c+d for c,d in zip(pt,offset)) for pt in row) for row in S)
        if panel==0:
            for row in display:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
            for j in range(len(display[0])):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(row[j]) for row in display)+';')
            for row in display:
                for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius=1.2pt];')
        else:
            values=sorted({B[q],B[len(S[0])]}|{F(j,30) for j in range(31) if B[q]<=F(j,30)<=B[len(S[0])]})
            paths,r=wires(A,B,p,q,display,stripe_values=values);lines+=paths;wire_reports.append(r)
    lines += [r'\draw[book axis] (0,0,0)--(5,0,0) node[below left=4pt] {$x$};',r'\draw[book axis] (0,0,0)--(0,6,0) node[right=4pt] {$y$};',r'\draw[book axis] (0,0,0)--(0,0,7.1) node[above=4pt] {$z$};',r'\end{scope}',r'\node at (.3,-4.3) {('+chr(97+panel)+')};',r'\end{scope}']
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
report.update(figure=figure,axis=axis,split_parameter=str(value),same_controls_as5_9=True,unit_weights=True,
    refined_control_count=[len(refined[-1]),len(refined[-1][0])],
    children=[{'U':list(map(str,A)),'V':list(map(str,B)),'control_count':[len(S),len(S[0])],'actual_controls':[[list(map(str,pt)) for pt in row] for row in S],'display_translation':list(map(str,offset))} for (A,B,p,q,S),offset in zip(children,offsets)],
    exact_child_wire_checks=wire_reports,global_stripe_grid_preserved=True)
(root/f'image_tex/build/directional-surface-subdivision-{axis}-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS:{figure},two clamped children,{report["identical_directional_polynomial_spans"]} identical polynomial spans,{report["child_vs_original_surface_points"]} invariant global surface points; true shared boundary before display translations.')
