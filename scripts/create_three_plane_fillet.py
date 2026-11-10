"""8.16: explicit orthogonal sharp corner and tangent cylinder/sphere fillets."""
from pathlib import Path
from fractions import Fraction as F
import json
from revolved_surface_data import camera,w
from native_bspline import segments,de_boor,cubic_path,point
from rational_geometry import project,approximate
from surface_geometry import surface,verify_tensor
from polynomial_native import multiply
from bspline_math import add,compose_affine
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_21.tex')['applied']
O=(F(1),F(1),F(3,2));R=F(11,20);length=F(21,10);C=tuple(x-R for x in O);L=length-R
E=tuple(tuple(F(i==j) for i in range(3)) for j in range(3));K=(F(0),)*3+(F(1),)*3;V=(F(0),F(0),F(1),F(1))
def translate(a,b,t):return tuple(x+t*y for x,y in zip(a,b))
vertices=tuple(translate(C,e,R) for e in E);arcs=[];reports=[]
for axis,(i,j) in enumerate(((1,2),(0,2),(0,1))):
    middle=tuple(C[k]+R*(E[i][k]+E[j][k]) for k in range(3))
    H=tuple(tuple(a*x for x in p)+(a,) for p,a in [(vertices[i],F(1)),(middle,w),(vertices[j],F(1))])
    NET=tuple((h,tuple(h[k]-L*E[axis][k]*h[-1] for k in range(3))+(h[-1],)) for h in H)
    tc=verify_tensor(K,V,2,1,NET);maxres=F(0)
    for n in range(21):
        u=F(n,20);base=project(de_boor(K,H,2,u));assert base[axis]==C[axis]
        for m in range(21):
            v=F(m,20);p=project(surface(K,V,2,1,NET,u,v));assert p==translate(base,E[axis],-v*L)
            res=abs(sum((p[k]-C[k])**2 for k in (i,j))-R*R);assert res<F(1,10**38);maxres=max(maxres,res)
    s=segments(K,H,2)[0];W=s['power'][-1]
    local=[add(s['power'][k],tuple(-C[k]*a for a in W)) for k in range(3)]
    residual=tuple(-R*R*a for a in multiply(W,W))
    for a in local:residual=add(residual,multiply(a,a))
    bound=sum(map(abs,compose_affine(residual,F(0),F(1))))/w**2;assert bound<F(1,10**38)
    assert vertices[i][i]==O[i] and vertices[j][j]==O[j]
    # A sphere-boundary normal has zero component along the adjacent cylinder axis.
    assert all((project(h)[axis]-C[axis])==0 for h in H)
    hh=tuple(camera(h[:3])+(h[-1],) for h in H);parts=approximate(hh,F(1,100000));arcs.append([cubic_path(p) for p in parts])
    reports.append({'cylinder_axis':axis,'cylinder_length':str(L),'exact_tensor_checks':tc,'exact_extrusion_and_cylinder_checks':441,'cylinder_residual_grid_max':str(maxres),'sphere_boundary_whole_span_residual_bound':str(bound),'sphere_and_cylinder_radial_normals_identical_on_shared_boundary':True,'endpoint_tangency_to_original_planes':True,'native_boundary_screen_L1_error_cm':str(max(p['certified_l1_error'] for p in parts))})
lines=['% Three orthogonal planes throughO,common fillet radius11/20;true quarter-cylinder/sphere boundary arcs.',r'\begin{tikzpicture}[book line]']
for label,shift in [('a',26),('b',0)]:
    lines.extend([r'\begin{scope}[yshift='+str(shift)+'cm]',r'\path[use as bounding box] (-11,-10) rectangle (12,14);'])
    for e in E:
        lines.append(r'\draw['+('book line' if label=='a' else 'book grid,dashed')+'] '+point(camera(O))+'--'+point(camera(translate(O,e,-length)))+';')
    if label=='b':
        for axis,(i,j) in enumerate(((1,2),(0,2),(0,1))):
            lines+=arcs[axis]
            for index in (i,j):lines.append(r'\draw '+point(camera(vertices[index]))+'--'+point(camera(translate(vertices[index],E[axis],-L)))+';')
    for end,name,anchor in [((F(27,10),0,0),'x','below left'),((0,F(27,10),0),'y','right'),((0,0,F(16,5)),'z','above')]:
        lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    labels={1:(F(1,2),F(83,10)),2:(F(6),F(1,5)),3:(-F(5),F(1,5))}
    if label=='b':labels.update({4:(F(11,2),F(7)),5:(F(11,10),-F(43,10)),6:(-F(11,2),F(26,5)),7:(-F(7,10),F(14,5))})
    for index,xy in labels.items():lines.append(r'\node at '+point(xy)+r' {$\mathbf S_{'+str(index)+'}$};')
    lines.extend([r'\node at (.5,-9.2) {('+label+')};',r'\end{scope}'])
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_21.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/three-plane-fillet-check.json').write_text(json.dumps({'figure':'8.16','representative_orthogonal_corner':list(map(str,O)),'fillet_radius':str(R),'sphere_center':list(map(str,C)),'planes':{'S1':'z=3/2','S2':'y=1','S3':'x=1'},'cylinders':{'S4':'axisX','S5':'axisZ','S6':'axisY'},'S7':'positive octant spherical patch','native_boundary_checks':reports,'common_camera_and_panel_scale':True,'display':'surface boundaries;dashed original sharp edges'},indent=2)+'\n')
print('PASS:3exactquarter-cylinder extrusions,1323tensor/cylinder checks;sphere boundary identities<1e-38,shared normals and original-plane tangent limits.')
