"""8.15a/b: exact parabolic meridian revolution,then actual affine net scaling."""
from pathlib import Path
from fractions import Fraction as F
import json
from revolved_surface_data import U,CIRCLE,camera,w
from native_bspline import de_boor,point
from rational_geometry import project
from surface_geometry import surface,verify_tensor
from native_rational_surface_grid import grid
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (19,20):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch08/fig_8_{n:02d}.tex')['applied']
radius=F(3,2);PROFILE=((F(0),F(0)),(radius/2,F(0)),(radius,radius**2));V=(F(0),)*3+(F(1),)*3
BASE=tuple(tuple((x*r,y*r,a*z,a) for r,z in PROFILE) for x,y,a in CIRCLE)
reports=[]
for n,label,FAC in [(19,'a',(F(1),F(1),F(1))),(20,'b',(F(3,2),F(3,4),F(1)))]:
    NET=tuple(tuple(tuple(f*x for f,x in zip(FAC,h[:3]))+(h[-1],) for h in row) for row in BASE)
    assert all(h[-1]==b[-1] for row,base in zip(NET,BASE) for h,b in zip(row,base))
    tc=verify_tensor(U,V,2,2,NET);maxres=F(0)
    for i in range(21):
        for j in range(21):
            u,v=F(i,20),F(j,20);h=surface(U,V,2,2,NET,u,v);base=surface(U,V,2,2,BASE,u,v)
            assert h==tuple(f*x for f,x in zip(FAC,base[:3]))+(base[-1],)
            p=project(h);x,y,z=p;res=abs((x/FAC[0])**2+(y/FAC[1])**2-z)
            assert res<F(1,10**36);maxres=max(maxres,res)
            rr,zz=de_boor(V,PROFILE,2,v);assert (rr,zz)==(radius*v,radius**2*v*v)
            if v==0:assert p==(0,0,0)
    distinct={project(h) for row in NET for h in row};assert len(distinct)==17
    lines=['% Biquadratic paraboloid: r(v)=3v/2,z(v)=9v^2/4;scaled net '+str(tuple(map(str,FAC)))+'.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-12,-8) rectangle (13,16);']
    for j in (1,2):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(NET[i][j]))) for i in range(9))+';')
    for row in NET[:-1]:lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(h))) for h in row)+';')
    lines.extend(r'\fill '+point(camera(p))+r' circle[radius=1.3pt];' for p in sorted(distinct))
    paths,report=grid(U,V,2,2,NET,camera,tuple(F(i,8) for i in range(8)),tuple(F(j,16) for j in range(1,17)),interior='book line');lines+=paths
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','right'),((0,0,F(7,2)),'z','above')]:
        lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    lines.extend([r'\node at (.5,-7.4) {('+label+')};',r'\end{tikzpicture}'])
    (root/f'image_tex/ch08/fig_8_{n:02d}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    reports.append({'panel':label,'scaling':list(map(str,FAC)),'degrees':[2,2],'control_dimensions':[9,3],'distinct_controls':17,'exact_tensor_checks':tc,'exact_homogeneous_affine_scaling_identities':441,'paraboloid_implicit_checks':441,'implicit_residual_grid_max':str(maxres),'exact_parabolic_profile_identity':True,'collapsed_vertex_row':True,'native_grid':report})
(root/'image_tex/build/scaled-paraboloids-check.json').write_text(json.dumps({'figure':'8.15','profile_controls':[[str(x) for x in p] for p in PROFILE],'c':1,'weights_unchanged_by_scaling':True,'common_camera_scale_and_panel_bbox':True,'models':reports,'display':'transparent wireframe'},indent=2)+'\n')
print('PASS:two actual9x3paraboloid nets,882tensor/scaling/implicit checks,1008isocurve identities;exact parabolic meridian and unchanged weights.')
