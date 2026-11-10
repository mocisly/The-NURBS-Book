"""Fig5.25: three adjacent actual Bezier nets on one representative tensor sheet."""
from pathlib import Path
from fractions import Fraction as F
import json,argparse
from surface_geometry import local_patch,surface,verify_tensor,isocurve
from native_surface_drawing import wires
from native_bspline import segments,cubic_path,point
from knot59_data import insert_surface
from surface_refinement import verify_directional_identity

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--replace-unapplied',action='store_true');args=parser.parse_args()
root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_32.tex'
if target.exists():
    assert args.replace_unapplied
    manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
    assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch05/fig_5_32.tex').get('applied')
U=(F(0),)*4+(F(1,3),F(2,3))+(F(1),)*4
V=(F(0),)*3+(F(1,2),)+(F(1),)*3
xs=tuple(map(F,(3,1,-1,-3)));ys=tuple(F(str(t)) for t in (-3,-2,-.6,.8,2.2,3.5))
zu=tuple(F(str(t)) for t in (0,0,.6,2,2,2));zv=tuple(F(str(t)) for t in (.3,0,0,.6))
# Exact derivative-convex-hull slope bounds guarantee no projection folding.
# u increases physical y; v decreases physical x. Each direction is a positive
# combination of its adjacent control differences, so these ratio bounds hold
# for every parameter, not just a sampled screen grid.
u_slopes=[(-F(7,20)*(ys[i+1]-ys[i])+F(9,10)*(zu[i+1]-zu[i]))/(F(19,20)*(ys[i+1]-ys[i])) for i in range(5)]
v_slopes=[(-F(3,4)*(xs[j+1]-xs[j])+F(9,10)*(zv[j+1]-zv[j]))/(-F(9,10)*(xs[j+1]-xs[j])) for j in range(3)]
assert max(u_slopes)<min(v_slopes)
P=tuple(tuple((xs[j],ys[i],zu[i]+zv[j]) for j in range(4)) for i in range(6));base=(U,V,3,2,P)
tensor=verify_tensor(*base,steps=10);refined=base;proofs=[]
for t in (F(1,3),F(2,3)):
    for repeat in range(2):
        new=insert_surface(*refined,'u',t);proofs.append(verify_directional_identity(refined,new,'u'));refined=new
new=insert_surface(*refined,'v',F(1,2));proofs.append(verify_directional_identity(refined,new,'v'));refined=new
assert len(refined[-1])==10 and len(refined[-1][0])==5
lines=['% Fig5.25: three selected adjacent Bezier patches of an explicit6x4 p3q2 surface.',
       '% The original gives no numeric net; exact representative data and six-patch knots in report.',
       '% All selected controls are extracted from SAME surface; no display translations or contours.',
       r'\begin{tikzpicture}[book line,x={(-.9cm,-.75cm)},y={(.95cm,-.35cm)},z={(0cm,.9cm)}]',
       r'\path[use as bounding box] (canvas cs:x=-6.5cm,y=-5.2cm) rectangle (canvas cs:x=7cm,y=6.1cm);']
drawn,wireproof=wires(*base,count=35);lines+=drawn
patches=[];previous=None;pointchecks=0
for i in range(3):
    Q,_,_=local_patch(U,V,3,2,P,3+i,3)
    assert Q==tuple(tuple(row[2:5]) for row in refined[-1][3*i:3*i+4])
    a,b=U[3+i:5+i];c,d=F(1,2),F(1)
    child=((a,)*4+(b,)*4,(c,)*3+(d,)*3,3,2,Q)
    if previous is not None:assert previous[-1]==Q[0]
    previous=Q
    for j in range(11):
        for k in range(11):
            u=a+(b-a)*F(j,10);v=c+(d-c)*F(k,10)
            assert surface(*child,u,v)==surface(*base,u,v);pointchecks+=1
    for variable,values in [('u',(c,d)),('v',(a,b))]:
        for value in values:
            K,pd,R=isocurve(*child,variable,value)
            for s in segments(K,R,pd):lines.append(cubic_path(s,'book line'))
    for row in Q:lines.append(r'\draw[book line,dashed] '+'--'.join(map(point,row))+';')
    for j in range(3):lines.append(r'\draw[book line,dashed] '+'--'.join(point(row[j]) for row in Q)+';')
    for row in Q:
        for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius=1.2pt];')
    patches.append({'u_domain':list(map(str,(a,b))),'v_domain':list(map(str,(c,d))),
                    'actual_extracted_4x3_controls':[[list(map(str,t)) for t in row] for row in Q]})
lines += [r'\draw[book axis] (0,0,0)--(5.5,0,0) node[below left=4pt] {$x$};',
          r'\draw[book axis] (0,0,0)--(0,6.2,0) node[right=4pt] {$y$};',
          r'\draw[book axis] (0,0,0)--(0,0,6.2) node[above=4pt] {$z$};',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/on-the-fly-surface-check.json').write_text(json.dumps({
    'figure':'5.25','representative_original_control_count':[6,4],'degrees':[3,2],
    'U':list(map(str,U)),'V':list(map(str,V)),
    'original_controls':[[list(map(str,t)) for t in row] for row in P],
    'tensor_vs_nested_deboor_points':tensor,'directional_refinement_proofs':proofs,
    'refined_control_count':[10,5],'total_bezier_patches':6,'selected_adjacent_patches':patches,
    'selected_child_vs_original_exact_points':pointchecks,'selected_boundaries_share_control_points_exactly':True,
    'all_selected_nets_match_independently_refined_net':True,'no_display_translation':True,
    'native_whole_surface_wire_proof':wireproof,
    'certified_projected_u_tangent_max_slope':str(max(u_slopes)),
    'certified_projected_v_tangent_min_slope':str(min(v_slopes)),
    'strict_slope_separation_prevents_projection_folding':True},indent=2)+'\n')
print('PASS:121 tensor points,363 selected patch invariance points; three actual4x3 nets match refined10x5 net exactly; shared boundaries exact.')
