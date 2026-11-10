"""Fig5.17: unchanged surface, actual11x4,4x10,11x10 refined control nets."""
from pathlib import Path
from fractions import Fraction as F
import json
from knot59_data import U,V,P
from surface_refinement import refine_surface,verify_directional_identity
from surface_geometry import surface
from native_bspline import segments,point
from midpoint_refinement import polygon_error_bound

root=Path(__file__).resolve().parents[1];targets=[root/f'image_tex/ch05/fig_5_{n}.tex' for n in (20,21)];assert not any(p.exists() for p in targets)
base=(U,V,3,2,P);Au,umids=refine_surface(base,'u',3);Av,vmids=refine_surface(base,'v',2)
Auv,_=refine_surface(Au,'v',2);Avu,_=refine_surface(Av,'u',3);assert Auv==Avu
proofs=[verify_directional_identity(a,b,axis) for a,b,axis in [(base,Au,'u'),(base,Av,'v'),(Au,Auv,'v'),(Av,Avu,'u')]]
def net_bound(net):
    A,B,p,q,R=net
    assert all(R[i][j]==tuple(R[i][0][d]+R[0][j][d]-R[0][0][d] for d in range(3)) for i in range(len(R)) for j in range(len(R[0])))
    # This representative translation surface is the sum of two curves minus its corner.
    # Bilinear interpolation at tensor Greville points has residual bounded by their sum.
    C=tuple(row[0] for row in R)
    return polygon_error_bound(A,C,p,segments(A,C,p))+polygon_error_bound(B,R[0],q,segments(B,R[0],q))
base_bound=net_bound(base);bounds=[net_bound(net) for net in (Au,Av,Auv)]
assert bounds[2]<min(bounds[:2]) and max(bounds[:2])<base_bound
panels=[];reports=[]
for index,net in enumerate((Au,Av,Auv)):
    A,B,p,q,R=net;assert (len(R),len(R[0]))==[(11,4),(4,10),(11,10)][index]
    for a in range(11):
        for b in range(11):assert surface(*net,F(a,10),F(b,10))==surface(*base,F(a,10),F(b,10))
    lines=[r'\begin{scope}[x={(-.72cm,-.48cm)},y={(.8cm,-.28cm)},z={(0cm,.8cm)}]']
    for row in R:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
    for j in range(len(R[0])):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(row[j]) for row in R)+';')
    for row in R:
        for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius='+('.8pt' if index==2 else '.9pt')+'];')
    lines += [r'\draw[book axis] (0,0,0)--(5,0,0) node[below left=4pt] {$x$};',r'\draw[book axis] (0,0,0)--(0,6,0) node[right=4pt] {$y$};',r'\draw[book axis] (0,0,0)--(0,0,7.1) node[above=4pt] {$z$};',r'\end{scope}',r'\node at (.3,-4.25) {('+chr(97+index)+')};'];panels.append(lines)
    reports.append({'panel':chr(97+index),'control_count':[len(R),len(R[0])],'U':list(map(str,A)),'V':list(map(str,B)),'controls':[[list(map(str,pt)) for pt in row] for row in R],'exact_surface_invariance_points':121,'separable_example_bilinear_greville_net_L1_error_bound_cm':str(bounds[index])})
for index,target in enumerate(targets):
    lines=['% Fig5.17: actual midpoint refinements of SAME representative unit-weight surface as5.9.',
           '% (a)3u rounds,(b)2v rounds,(c)both; global polynomial surface and parametrization unchanged.',
           '% Refined control counts11x4,4x10,11x10. Exact native control nets, no contours.',r'\begin{tikzpicture}[book line]',
           r'\path[use as bounding box] (canvas cs:x='+('-11.3cm' if index==0 else '-5.3cm')+',y=-4.9cm) rectangle (canvas cs:x='+('12cm' if index==0 else '6cm')+',y=6.7cm);']
    for panel,xshift in ([(0,-6),(1,6)] if index==0 else [(2,0)]):
        lines.append(r'\begin{scope}[xshift='+str(xshift)+'cm]');lines+=panels[panel];lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/midpoint-surface-refinement-check.json').write_text(json.dumps({'figure':'5.17','same_original_surface_as5.9':True,'degrees':[3,2],'unit_weights':True,'u_midpoint_rounds':[[str(t) for t in row] for row in umids],'v_midpoint_rounds':[[str(t) for t in row] for row in vmids],'directional_polynomial_identity_proofs':proofs,'refinement_orders_commute_exactly':True,'original_bilinear_greville_net_L1_error_bound_cm':str(base_bound),'refined_bilinear_greville_net_bounds_cm':list(map(str,bounds)),'panels':reports},indent=2)+'\n')
print('PASS:11x4/4x10/11x10 nets,363 invariant surface points,'+str(sum(p['identical_directional_polynomial_spans'] for p in proofs))+' identical polynomial spans; orders commute; certified net bounds '+','.join(f'{float(e):.5f}' for e in [base_bound]+bounds)+'cm.')
