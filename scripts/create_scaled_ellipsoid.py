"""8.14: affine scaling of the unit-sphere homogeneous net,weights unchanged."""
from pathlib import Path
from fractions import Fraction as F
import json
from revolved_surface_data import U,CIRCLE,camera,w
from native_bspline import point
from rational_geometry import project
from surface_geometry import surface,verify_tensor
from native_rational_surface_grid import grid
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_18.tex')['applied']
A=(F(1),F(3,4),F(9,5));P=[(0,0,-1),(1,0,-1),(1,0,0),(1,0,1),(0,0,1)]
PROFILE=tuple(tuple(F(x)*b for x in p)+(b,) for i,p in enumerate(P) for b in [w if i%2 else F(1)])
V=(F(0),)*3+(F(1,2),)*2+(F(1),)*3
UNIT=tuple(tuple((x*rh,y*rh,b*zh,b*c) for rh,_,zh,c in PROFILE) for x,y,b in CIRCLE)
NET=tuple(tuple(tuple(a*x for a,x in zip(A,h[:3]))+(h[-1],) for h in row) for row in UNIT)
assert all(h[-1]==b[-1] for row,base in zip(NET,UNIT) for h,b in zip(row,base))
tc=verify_tensor(U,V,2,2,NET);maxres=F(0)
for i in range(21):
    for j in range(21):
        u,v=F(i,20),F(j,20);h=surface(U,V,2,2,NET,u,v);base=surface(U,V,2,2,UNIT,u,v)
        assert h==tuple(a*x for a,x in zip(A,base[:3]))+(base[-1],)
        p=project(h);assert p==tuple(a*x for a,x in zip(A,project(base)))
        res=abs(sum((x/a)**2 for x,a in zip(p,A))-1);assert res<F(1,10**36);maxres=max(maxres,res)
distinct={project(h) for row in NET for h in row};assert len(distinct)==26
lines=['% Actual unit-sphere9x5 homogeneous net scaled diag(1,3/4,9/5);weights untouched.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-10,-13) rectangle (11,14);']
for j in (1,2,3):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(NET[i][j]))) for i in range(9))+';')
for row in NET[:-1]:lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(h))) for h in row)+';')
lines.extend(r'\fill '+point(camera(p))+r' circle[radius=1.3pt];' for p in sorted(distinct))
paths,report=grid(U,V,2,2,NET,camera,tuple(F(i,12) for i in range(12)),tuple(F(j,16) for j in range(1,16)),interior='book line');lines+=paths
for end,name,anchor in [((F(5,2),0,0),'x','below left'),((0,F(5,2),0),'y','right'),((0,0,F(16,5)),'z','above')]:
    lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_18.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/scaled-ellipsoid-check.json').write_text(json.dumps({'figure':'8.14','semiaxes':list(map(str,A)),'unit_sphere_template_control_dimensions':[9,5],'degrees':[2,2],'unchanged_homogeneous_weights':True,'distinct_controls':26,'exact_tensor_checks':tc,'exact_homogeneous_affine_scaling_identities':441,'ellipsoid_implicit_checks':441,'implicit_residual_grid_max':str(maxres),'native_grid':report,'same_camera_scale_as8_11':True,'display':'transparent wireframe'},indent=2)+'\n')
print('PASS:441exact homogeneous scaling/tensor identities,ellipsoid residual<1e-36;567isocurve checks,unchanged weights and26distinct controls.')
