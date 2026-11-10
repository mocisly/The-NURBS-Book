"""9.35: actual local bicubic retains8whole planar patches next to a boundary rise."""
from fractions import Fraction as F
from pathlib import Path
import json
from local_bicubic_surface import construct
from surface_geometry import surface,verify_tensor,isocurve
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_42.tex')['applied']
HEIGHT=tuple(map(F,['0','1/2','3/4','1/2','0']))
Q=tuple(tuple((F(i-2),F(j-2),HEIGHT[i] if j==4 else F(0)) for j in range(5)) for i in range(5))
base,(UP,VP),full,patch,proof=construct(Q)
flat=tuple((k,l) for k,row in enumerate(patch) for l,b in enumerate(row) if all(p[2]==0 for rr in b for p in rr))
assert flat==tuple((k,l) for k in range(4) for l in range(2))
tc=verify_tensor(*base,steps=4);native=iso=0
def camera(q):
    x,y,z=q;return (2*(-F(4,5)*x+F(9,10)*y),2*(-F(2,5)*x-F(7,20)*y+z))
def poly(row):return r'\draw[book grid,dashed] '+'--'.join(point(camera(p)) for p in row)+';'
def mark(q):return r'\draw '+point(camera(q))+r' ++(-2pt,-2pt) rectangle ++(4pt,4pt);'
def panel(letter,shift):
    global native,iso
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-7.5,-4.7) rectangle (7.5,6);']
    if letter=='a':
        for row in Q:out.append(poly(row))
        for col in zip(*Q):out.append(poly(col))
    else:
        fixed=tuple(UP[k]+(UP[k+1]-UP[k])*F(j,10) for k in range(4) for j in range(10))+(F(1),)
        for u in fixed:
            K,p,C=isocurve(*base,'v',u);ss=segments(K,C,p);native+=check(K,C,p,ss,steps=7)
            for j in range(5):
                v=F(j,4);assert de_boor(K,C,p,v)==surface(*base,u,v);iso+=1
            out.extend(cubic_path(dict(bern=tuple(camera(p) for p in s['bern']))) for s in ss)
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(5,2)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend(mark(q) for row in Q for q in row);out.extend([r'\node at (0,-4.1) {('+letter+')};',r'\end{scope}']);return out
out=['% Representative25point local bicubic with22planar and3raised boundary data;8whole patches exactlyz0.',r'\begin{tikzpicture}[book line]']+panel('a',0)+panel('b',16)+[r'\end{tikzpicture}']
(root/'image_tex/ch09/fig_9_42.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/local-bicubic-planar-regions-check.json').write_text(json.dumps(dict(figure='9.35',representative_data=[[[str(x) for x in p] for p in row] for row in Q],data_points=25,data_on_z0=22,raised_boundary_data=3,construction=proof,whole_planar_patch_indices=flat,all16Bezier_zcoefficients_zero_on_each_planar_patch=True,independent_tensor_checks=tc,native_curve_checks=native,isocurve_surface_crosschecks=iso,displayed_v_isocurves=41,common_camera_scale='2'),indent=2)+'\n')
print('PASS9.35:25data,22planar+3raised,16wholepatch identities,8wholepatches exactlyz0(all16coefficients),localC1andzeroerrorknotremovals;',native,'native checks.')
