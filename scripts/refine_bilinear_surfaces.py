"""8.1: independently verify existing bilinear examples and align the two panels."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point
from surface_geometry import surface
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_01.tex')['applied']
K=(F(0),F(0),F(1),F(1))
def camera(p):
    x,y,z=p;return (4*(-F(39,50)*x+F(24,25)*y),4*(-x/2-F(3,10)*y+z))
def blend(P,u,v):return tuple((1-u)*(1-v)*P[0][k]+u*(1-v)*P[1][k]+(1-u)*v*P[2][k]+u*v*P[3][k] for k in range(3))
def line(a,b,style):return r'\draw['+style+'] '+point(camera(a))+'--'+point(camera(b))+';'
models=[('a',[(1,0,F(13,20)),(1,1,0),(0,0,1),(0,1,F(7,20))]),('b',[(1,0,1),(1,1,0),(0,0,0),(0,1,1)])]
lines=['% Existing semantic8.1 reverified exactly; affine camera and common scale, horizontal panels.',r'\begin{tikzpicture}[book line]'];reports=[]
for panel,raw in models:
    P=tuple(tuple(map(F,p)) for p in raw);grid=((P[0],P[2]),(P[1],P[3]))
    for i in range(21):
        for j in range(21):
            u,v=F(i,20),F(j,20);s=blend(P,u,v);assert surface(K,K,1,1,grid,u,v)==s
            assert s==tuple((1-v)*x+v*y for x,y in zip(blend(P,u,0),blend(P,u,1)))
            assert s==tuple((1-u)*x+u*y for x,y in zip(blend(P,0,v),blend(P,1,v)))
            x,y,z=s
            if panel=='a':assert z==1-F(7,20)*x-F(13,20)*y
            else:assert z==x+y-2*x*y
    lines += [r'\begin{scope}'+('[xshift=14cm]' if panel=='b' else ''),r'\path[use as bounding box] (-5.7,-5.8) rectangle (6.9,7);']
    if panel=='a':
        plane=[(x,y,1-F(7,20)*x-F(13,20)*y) for x,y in [(F(61,50),-F(1,5)),(F(61,50),F(6,5)),(-F(11,50),F(6,5)),(-F(11,50),-F(1,5))]]
        lines += [r'\draw[book grid,dashed] '+'--'.join(point(camera(p)) for p in plane)+'--cycle;',r'\node at (-1.73,4) {$\Pi$};']
    else:
        for axis in range(3):
            for a in (F(0),F(1)):
                for b in (F(0),F(1)):
                    other=[k for k in range(3) if k!=axis];p=[F(0)]*3;q=p.copy();p[other[0]]=q[other[0]]=a;p[other[1]]=q[other[1]]=b;q[axis]=1
                    lines.append(line(p,q,'book grid,dashed'))
    for end,label,anchor in [((F(7,5),0,0),'x','below left'),((0,F(29,20),0),'y','above right'),((0,0,F(3,2)),'z','above right')]:
        lines += [line((0,0,0),end,'book axis,book grid'),r'\node['+anchor+r'=4pt] at '+point(camera(end))+' {$'+label+'$};']
    for j in range(21):
        t=F(j,20);style='book line' if j in (0,20) else 'book grid'
        lines += [line(blend(P,t,0),blend(P,t,1),style),line(blend(P,0,t),blend(P,1,t),style)]
    for i,(p,label,anchor) in enumerate(zip(P,['0,0','1,0','0,1','1,1'],['left','below','above','right'])):
        lines.append(r'\fill '+point(camera(p))+r' circle[radius=1.7pt];')
        if panel=='b' and i==2:lines.append(r'\draw[book axis,book grid] (-4.3,.55) node[left=4pt] {$\mathbf P_{0,1}$}--(-.12,.04);')
        else:
            if panel=='a' and i==2:anchor='right'
            lines.append(r'\node['+anchor+r'=6pt] at '+point(camera(p))+r' {$\mathbf P_{'+label+'}$};')
    lines += [r'\node at (.6,-5.35) {('+panel+')};',r'\end{scope}'];reports.append({'panel':panel,'controls':[[str(x) for x in p] for p in P],'exact_tensor_and_straight_isoline_checks':441,'physical_equation':'z=1-7x/20-13y/20' if panel=='a' else 'z=x+y-2xy','grid_intervals':20})
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_01.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/bilinear-surfaces-check.json').write_text(json.dumps({'figure':'8.1','camera':'affine (-78x/100+96y/100,-x/2-3y/10+z),scale4cm','models':reports,'saddle_physical_xy_hessian_determinant':-4},indent=2)+'\n')
print('PASS:882exact tensor/straight-isoline checks; coplanar plane identity and true hyperbolic paraboloid; horizontal panels with common affine camera.')
