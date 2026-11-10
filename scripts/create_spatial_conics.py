"""7.10: three genuine coplanar spatial conics in an exact orthonormal frame."""
from pathlib import Path
from fractions import Fraction as F
import json
from polynomial_native import bernstein
from rational_geometry import approximate,evaluate,project
from native_bspline import cubic_path,point

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_10.tex')['applied']
O=(F(1),F(1,2),F(1));X=(F(0),F(3,5),-F(4,5));Y=(-F(4,5),F(12,25),F(9,25))
N=(F(3,5),F(16,25),F(12,25))
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
assert dot(X,X)==dot(Y,Y)==dot(N,N)==1 and dot(X,Y)==dot(X,N)==dot(Y,N)==0
def spatial(x,y):return tuple(o+x*u+y*v for o,u,v in zip(O,X,Y))
def homogeneous(H):return tuple(tuple(o*w+x*u+y*v for o,u,v in zip(O,X,Y))+(w,) for x,y,w in H)
def plane_check(H):
    assert all(dot(N,tuple(v-w*o for v,o in zip(h[:-1],O)))==0 for h in H for w in (h[-1],))
lines=['% Explicit representative orthonormal frame, common O/X/Y for ALL THREE conics.',
       '% X/Y arrows have actual unit length; dashed lines extend local coordinate axes.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-6,-5.5) rectangle (6,6.2);',
       r'\begin{scope}[x={(-.9cm,-.6cm)},y={(.95cm,-.35cm)},z={(0cm,1cm)}]',
       r'\draw[book axis,book grid] (0,0,0)--(5,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis,book grid] (0,0,0)--(0,5.5,0) node[right=4pt] {$y$};',
       r'\draw[book axis,book grid] (0,0,0)--(0,0,5.6) node[above=4pt] {$z$};',
       r'\draw[book grid] '+'--'.join(point(spatial(x,y)) for x,y in [(-F(14,5),-F(3)),(F(14,5),-F(3)),(F(14,5),F(3)),(-F(14,5),F(3))])+r'--cycle;',
       r'\draw[book grid,dashed] '+point(spatial(-F(14,5),0))+'--'+point(spatial(F(14,5),0))+';',
       r'\draw[book grid,dashed] '+point(spatial(0,-F(3)))+'--'+point(spatial(0,F(3)))+';']
proofs=[];samples=0
quarter=((F(1),F(0),F(1)),(F(1),F(1),F(1)),(F(0),F(2),F(2)))
for quadrant in range(4):
    H=[]
    for x,y,w in quarter:
        for _ in range(quadrant):x,y=-y,x
        H.append((2*x,F(6,5)*y,w))
    world=homogeneous(H);plane_check(world)
    for i in range(21):
        x,y=project(evaluate(H,F(i,20)));C=project(evaluate(world,F(i,20)))
        assert x*x/4+y*y/F(36,25)==1 and C==spatial(x,y);samples+=1
    paths=approximate(world,F(1,100000));lines.extend(cubic_path(s) for s in paths)
    proofs.append({'kind':'ellipse','quadrant':quadrant,'paths':len(paths),'certified_world_L1_error':str(max(s['certified_l1_error'] for s in paths))})
h=F(13,20);a,b=F(4,5),F(11,20)
for sign in (-1,1):
    H=bernstein(((sign*a,F(0),sign*a),(F(0),2*b,F(0)),(F(1),F(0),-F(1))),-h,h)
    world=homogeneous(H);plane_check(world)
    for i in range(21):
        x,y=project(evaluate(H,F(i,20)));C=project(evaluate(world,F(i,20)))
        assert x*x/(a*a)-y*y/(b*b)==1 and C==spatial(x,y);samples+=1
    paths=approximate(world,F(1,100000));lines.extend(cubic_path(s) for s in paths)
    proofs.append({'kind':'hyperbola','sign':sign,'paths':len(paths),'certified_world_L1_error':str(max(s['certified_l1_error'] for s in paths))})
ap=F(7,20);hp=F(23,10)
local=bernstein(((F(0),F(0),ap),(F(0),2*ap)),-hp,hp)
world=tuple(spatial(*p) for p in local);assert all(dot(N,tuple(c-o for c,o in zip(pt,O)))==0 for pt in world)
lines.append(cubic_path({'bern':world}))
for i in range(21):
    t=-hp+2*hp*F(i,20);x,y=ap*t*t,2*ap*t;C=spatial(x,y)
    assert y*y==4*ap*x and dot(N,tuple(c-o for c,o in zip(C,O)))==0;samples+=1
lines += [r'\draw[book axis] '+point(O)+'--'+point(spatial(1,0))+r' node[below right=5pt] {$\mathbf X$};',
          r'\draw[book axis] '+point(O)+'--'+point(spatial(0,1))+r' node[above right=5pt] {$\mathbf Y$};',
          r'\draw '+point(O)+r' circle[radius=1.8pt] node[above left=7pt] {$\mathbf O$};',r'\end{scope}']
def screen(P):
    x,y,z=P;return (-F(9,10)*x+F(19,20)*y,-F(3,5)*x-F(7,20)*y+z)
targets=[('Hyperbola',(-F(21,5),F(23,10)),spatial(-a*(1+h*h)/(1-h*h),-2*b*h/(1-h*h)),'east'),
         ('Ellipse',(F(31,10),-F(14,5)),spatial(2,0),'west'),
         ('Parabola',(-F(37,10),-F(22,5)),spatial(ap*hp*hp,-2*ap*hp),'east')]
for index,(label,location,target,anchor) in enumerate(targets):
    name='coniclabel'+str(index)
    lines.append(r'\node[anchor='+anchor+'] ('+name+') at '+point(location)+r' {$\mathrm{'+label+'}$};')
    lines.append(r'\draw[book axis,book grid] ('+name+'.'+anchor+')--'+point(screen(target))+';')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch07/fig_7_10.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/spatial-conics-check.json').write_text(json.dumps({'figure':'7.10','O':list(map(str,O)),'X':list(map(str,X)),'Y':list(map(str,Y)),'normal':list(map(str,N)),'exact_orthonormality':True,'exact_planarity_and_local_implicit_samples':samples,'all_native_homogeneous_controls_exactly_coplanar':True,'display_basis_vectors_true_unit_length':True,'rational_path_certificates':proofs,'parabola_path':'exact quadratic, elevated to cubic'},indent=2)+'\n')
print(f'PASS:{samples} exact coplanarity/local implicit checks; exact orthonormal frame; certified world rational paths and exact parabola.')
