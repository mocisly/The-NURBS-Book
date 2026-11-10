"""9.18:24coplanar data and one raised point;global interpolation ripples in flat regions."""
from fractions import Fraction as F
from pathlib import Path
import json
from global_interpolation_data import interpolate
from inverse_knot_projection import solve
from surface_geometry import weights,surface,verify_tensor,isocurve
from native_bspline import segments,check,de_boor,cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_22.tex')['applied']
params=tuple(F(i,4) for i in range(5));height=F(6,5)
Q=tuple(tuple((F(i-2),F(j-2),height if i==j==2 else F(0)) for j in range(5)) for i in range(5))
cols=[]
for j in range(5):
    U,C=interpolate(tuple(Q[i][j] for i in range(5)),params);cols.append(C)
R=tuple(tuple(cols[j][i] for j in range(5)) for i in range(5));P=[]
for row in R:
    V,C=interpolate(row,params);P.append(C)
P=tuple(P);base=(U,V,3,3,P)
assert U==V==(F(0),)*4+(F(1,2),)+(F(1),)*4
reverse=tuple(interpolate(row,params)[1] for row in Q)
revcols=tuple(interpolate(tuple(reverse[i][j] for i in range(5)),params)[1] for j in range(5))
assert P==tuple(tuple(revcols[j][i] for j in range(5)) for i in range(5))
assert all(surface(*base,u,v)==Q[i][j] for i,u in enumerate(params) for j,v in enumerate(params))
M=tuple(tuple(weights(U,3,t)) for t in params)
cardinal=tuple(r[0] for r in solve(M,tuple((F(i==2),) for i in range(5))))
assert all(P[i][j][2]==height*cardinal[i]*cardinal[j] for i in range(5) for j in range(5))
witness=surface(*base,F(1,8),F(3,8));assert witness[2]<0
tc=verify_tensor(*base);nc=0;iso=0
def camera(q):
    x,y,z=q;s=F(5,2)
    return (s*(-F(4,5)*x+F(9,10)*y),s*(-F(2,5)*x-F(7,20)*y+z))
def panel(mode,shift):
    global nc,iso
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-9,-6) rectangle (9,8);']
    if mode=='a':
        for row in Q:out.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(q)) for q in row)+';')
        for col in zip(*Q):out.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(q)) for q in col)+';')
    else:
        for axis,count in [('u',40),('v',16)]:
            for j in range(count+1):
                t=F(j,count);K,p,C=isocurve(*base,axis,t);ss=segments(K,C,p);nc+=check(K,C,p,ss)
                for k in range(21):
                    a=F(k,20);assert de_boor(K,C,p,a)==surface(*base,a,t) if axis=='u' else de_boor(K,C,p,a)==surface(*base,t,a);iso+=1
                out.extend(cubic_path(dict(bern=tuple(camera(q) for q in s['bern']))) for s in ss)
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(11,5)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    for row in Q:
        for q in row:out.append(r'\fill '+point(camera(q))+r' circle[radius=1.8pt];')
    out.extend([r'\node at (0,-5.3) {('+mode+')};',r'\end{scope}']);return out
lines=['%24coplanar points and one raised center;true global bicubic interpolation.',r'\begin{tikzpicture}[book line]']+panel('a',0)+panel('b',19)+[r'\end{tikzpicture}']
(root/'image_tex/ch09/fig_9_22.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/coplanar-data-surface-interpolation-check.json').write_text(json.dumps(dict(figure='9.18',representative_data=[[[str(x) for x in q] for q in row] for row in Q],data_count=25,coplanar_z0_count=24,raised_center_height=str(height),parameters=list(map(str,params)),knots=list(map(str,U)),all25interpolation_constraints_exact=True,reverse_interpolation_order_identical=True,independent_tensor_checks=tc,native_curve_checks=nc,isocurve_vs_surface_exact_checks=iso,whole_control_height_outer_product_identity=True,univariate_cardinal_controls=list(map(str,cardinal)),planar_region_negative_ripple_witness_parameter=['1/8','3/8'],ripple_witness_point=list(map(str,witness)),important_distinction='entirely coplanar data ARE plane-preserving;local coplanar subsets need not produce flat subregions'),indent=2)+'\n')
print('PASS:25point bicubic solve,24coplanar+1raised,whole height outer-product identity,negative ripple witness',list(map(str,witness)),',441tensor/native checks.')
