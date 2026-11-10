"""8.19:full4x2stereographic composite,rigidly oriented with its15-control net."""
from pathlib import Path
from fractions import Fraction as F
import json
from projected_spherical_triangle_data import K,T,PLANAR_NET
from stereographic_geometry import lift_h
from stereographic_patch_composition import compose_patch
from revolved_surface_data import camera
from native_bspline import point
from rational_geometry import project
from surface_geometry import surface,verify_tensor
from native_rational_surface_grid import grid
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_24.tex')['applied']
U,V,BASE,proof=compose_patch(K,T,PLANAR_NET)
M=((F(44,125),F(117,125),F(0)),(F(117,125),-F(44,125),F(0)),(F(0),F(0),-F(1)))
D=(F(0),F(2,5),F(2));center=(F(0),F(2,5),F(1))
assert all(sum(x*y for x,y in zip(a,b))==F(i==j) for i,a in enumerate(M) for j,b in enumerate(M))
det=sum(M[0][i]*(M[1][(i+1)%3]*M[2][(i+2)%3]-M[1][(i+2)%3]*M[2][(i+1)%3]) for i in range(3));assert det==1
def rigid_h(h):return tuple(sum(a*x for a,x in zip(row,h[:3]))+b*h[-1] for row,b in zip(M,D))+(h[-1],)
NET=tuple(tuple(rigid_h(h) for h in row) for row in BASE[::-1])
tc=verify_tensor(U,V,4,2,NET)
for i in range(21):
    for j in range(21):
        s,t=F(i,20),F(j,20);h=surface(U,V,4,2,BASE,s,t);p=surface(K,T,2,1,PLANAR_NET,s,t)
        assert h==lift_h((p[0],p[1],p[-1]))
        transformed=surface(U,V,4,2,NET,1-s,t);assert transformed==rigid_h(h)
        pp=project(transformed);assert sum((x-c)**2 for x,c in zip(pp,center))==1
        if t==0:assert pp==D
assert all(project(row[0])==D for row in NET)
def screen(p):return tuple(F(3,2)*x for x in camera(p))
lines=['% Full equation8.23 composition retained as degree4x2:all15homogeneous coefficients verified.',
       '% Rigid rotation det+1,translation,and s-reversal only;all five j0controls collapse.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-13,-9) rectangle (14,16);']
for j in range(3):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(screen(project(NET[i][j]))) for i in range(5))+';')
for row in NET:lines.append(r'\draw[book grid,dashed] '+'--'.join(point(screen(project(h))) for h in row)+';')
distinct={project(h) for row in NET for h in row};assert len(distinct)==11
lines.extend(r'\fill '+point(screen(p))+r' circle[radius=1.5pt];' for p in sorted(distinct))
paths,report=grid(U,V,4,2,NET,screen,tuple(F(i,16) for i in range(17)),tuple(F(j,16) for j in range(1,17)));lines+=paths
for end,name,anchor in [((F(12,5),0,0),'x','below left'),((0,F(11,5),0),'y','right'),((0,0,F(12,5)),'z','above')]:
    lines.append(r'\draw[book axis,book grid] (0,0)--'+point(screen(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
lines.append(r'\node[above right=8pt] at '+point(screen(D))+r' {$\mathbf P_{0,0}=\cdots=\mathbf P_{4,0}$};')
for i,j,anchor in [(0,1,'above left'),(4,1,'above right'),(0,2,'left'),(1,2,'below left'),(2,2,'below'),(3,2,'below right'),(4,2,'right')]:
    lines.append(r'\node['+anchor+r'=7pt] at '+point(screen(project(NET[i][j])))+r' {$\mathbf P_{'+str(i)+','+str(j)+'}$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_24.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/spherical-corner-patch-check.json').write_text(json.dumps({'figure':'8.19','same_planar_arc_as8_18':True,'degrees':[4,2],'control_dimensions':[5,3],'distinct_controls':11,'composition_proof':proof,'exact_tensor_checks':tc,'exact_homogeneous_composition_and_rigid_transform_checks':441,'exact_sphere_identities':441,'sphere_center':list(map(str,center)),'sphere_radius':1,'collapsed_t0_boundary_all5controls':True,'rotation':[[str(x) for x in row] for row in M],'rotation_determinant':str(det),'translation':list(map(str,D)),'s_direction_reversed_for_display':True,'native_grid':report,'coordinate_display_scale_cm':6,'display':'transparent wireframe'},indent=2)+'\n')
print('PASS:all15composite4x2power vectors exact,whole sphere polynomial identity,441tensor/composition/rigid identities;positive weights and5fold collapsed edge.')
