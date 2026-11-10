"""11.27 true one-side control projection of the established wavy surface."""
from pathlib import Path
from fractions import Fraction as F
import json
from surface_relocation_example_data import BASE,view
from knot59_data import insert_surface
from surface_refinement import verify_directional_identity
from surface_geometry import isocurve,surface
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];net=BASE
for t in(F(i,16)for i in range(1,16)):
    if t not in net[0]:net=insert_surface(*net,'u',t)
u_proof=verify_directional_identity(BASE,net,'u');before_v=net
for t in(F(i,16)for i in range(1,16)):
    if t not in net[1]:net=insert_surface(*net,'v',t)
v_proof=verify_directional_identity(before_v,net,'v');U,V,p,q,P=net;height=F(4,5)
Q=tuple(tuple((x,y,min(z,height))for x,y,z in row)for row in P);new=(U,V,p,q,Q);flat=[]
for i in range(p,len(P)):
    if U[i]==U[i+1]:continue
    for j in range(q,len(P[0])):
        if V[j]==V[j+1]:continue
        if all(Q[a][b][2]==height for a in range(i-p,i+1)for b in range(j-q,j+1)):flat.append((U[i],U[i+1],V[j],V[j+1]))
assert flat and all(z<=height for row in Q for x,y,z in row)
lines=['% Actual one-side projection on refined wavy tensor surface; no contour tracing.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]'];nc=cross=0
for index,S in enumerate((net,new)):
    lines.extend([r'\begin{scope}[xshift='+str(19*index)+r'cm]',r'\path[use as bounding box] (-9,-7) rectangle (9,8);'])
    if index==0:
        plane=tuple(view((x,y,height))for x,y in[(-4,-F(7,2)),(4,-F(7,2)),(4,F(7,2)),(-4,F(7,2))]);lines.append(r'\draw[book grid,dashed] '+'--'.join(point(a)for a in plane)+'--cycle;')
    for variable,values in[('u',tuple(F(i,16)for i in range(17))),('v',tuple(F(i,8)for i in range(9)))]:
        for t in values:
            K,d,C=isocurve(*S,variable,t);ss=segments(K,C,d);nc+=check(K,C,d,ss,steps=2)
            for z in(F(0),F(1,3),F(2,3),F(1)):
                assert de_boor(K,C,d,z)==(surface(*S,z,t)if variable=='u'else surface(*S,t,z));cross+=1
            for s in ss:lines.append(cubic_path(dict(bern=tuple(view(a)for a in s['bern'])),'book grid'))
    origin=(-F(15,2),-F(11,2))
    for end,label,anchor in[((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:lines.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tuple(a+b for a,b in zip(origin,view(end))))+r' node['+anchor+r'=4pt] {$'+label+'$};')
    lines.extend([r'\node at (0,7.4) {$'+(r'\pi:\ z=4/5' if index==0 else r'\widehat P_{i,j,z}=\min(P_{i,j,z},4/5)')+'$};',r'\node at (0,-6.6) {('+chr(97+index)+')};',r'\end{scope}'])
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_33.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/surface-flattening-check.json').write_text(json.dumps(dict(original_surface='same wavy BASE as11.8, exact refinement',u_knots=U,v_knots=V,degrees=(p,q),control_shape=(len(P),len(P[0])),controls=P,projected_controls=Q,plane_z=height,u_refinement=u_proof,v_refinement=v_proof,whole_flat_tensor_rectangles=flat,flat_rectangle_count=len(flat),all_modified_surface_below_plane=True,native_checks=nc,tensor_isocurve_checks=cross,native_curve_error=0,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.27',len(flat),'whole EXACT plane rectangles;',nc,'nativechecks; refined shape',len(P),len(P[0]))
