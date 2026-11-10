"""9.36: true local bicubic on16nonuniform,nonrectangular step-profile data."""
from pathlib import Path
from fractions import Fraction as F
import json
from local_bicubic_surface import construct
from mesh_interpolation_example_data import X,H,A,G,camera
from local_quadratic_interpolator import add,length
from surface_geometry import surface,verify_tensor,isocurve
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_43.tex')['applied']
Y=tuple(tuple(map(F,row)) for row in [('-2','-1.6','1.3','2'),('-2','-.7','.9','2'),('-2','-1.7','1.5','2'),('-2','-1.65','1.6','2')])
Q=tuple(tuple((X[i],Y[i][j],H[i]+A[i]*G[j]) for j in range(4)) for i in range(4))
base,(UP,VP),full,patch,proof=construct(Q)
chords=tuple(length(add(b,a,-1)) for lines in (Q,tuple(zip(*Q))) for row in lines for a,b in zip(row,row[1:]))
ratio=max(chords)/min(chords);assert ratio>10
tc=verify_tensor(*base,steps=4);native=iso=0
def view(q):return tuple(x/2 for x in camera(q))
projected=[view(q) for row in base[-1] for q in row]
assert min(q[0] for q in projected)>-F(13,2) and max(q[0] for q in projected)<F(13,2)
assert min(q[1] for q in projected)>-F(9,2) and max(q[1] for q in projected)<11
def poly(row):return r'\draw[book grid,dashed] '+'--'.join(point(view(p)) for p in row)+';'
def mark(q):return r'\draw '+point(view(q))+r' ++(-2pt,-2pt) rectangle ++(4pt,4pt);'
def panel(letter,shift):
    global native,iso
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-6.5,-4.5) rectangle (6.5,11);']
    if letter=='a':
        for row in Q:out.append(poly(row))
        for col in zip(*Q):out.append(poly(col))
    else:
        fixed=tuple(VP[k]+(VP[k+1]-VP[k])*F(j,c) for k,c in enumerate((12,16,12)) for j in range(c))+(F(1),)
        for v in fixed:
            K,p,C=isocurve(*base,'u',v);ss=segments(K,C,p);native+=check(K,C,p,ss,steps=7)
            for j in range(5):
                u=F(j,4);assert de_boor(K,C,p,u)==surface(*base,u,v);iso+=1
            out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern']))) for s in ss)
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(26,5)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(view(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend(mark(q) for row in Q for q in row);out.extend([r'\node at (0,-4) {('+letter+')};',r'\end{scope}']);return out
out=['%16chosen nonrectangular step-profile data with neighboring chord ratio>10;actual A9.5 interpolation.',r'\begin{tikzpicture}[book line]']+panel('a',0)+panel('b',14)+[r'\end{tikzpicture}']
(root/'image_tex/ch09/fig_9_43.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/irregular-local-bicubic-check.json').write_text(json.dumps(dict(figure='9.36',representative_data=[[[str(x) for x in p] for p in row] for row in Q],irregular_Y_rows=[list(map(str,row)) for row in Y],chord_min=str(min(chords)),chord_max=str(max(chords)),chord_max_over_min=float(ratio),construction=proof,independent_tensor_checks=tc,native_curve_checks=native,isocurve_surface_crosschecks=iso,displayed_u_isocurves=41,includes_all4data_parameter_lines=True,same_camera_and_bounds_as='9.32',projected_control_hull_bounds=[[float(min(q[i] for q in projected)),float(max(q[i] for q in projected))] for i in range(2)]),indent=2)+'\n')
print('PASS9.36:16irregular3Ddata,localbicubic9wholepatch identities/48C1edgecoefficients,exactall16data andzeroerrorknotremovals;neighborchordratio',float(ratio),';',native,'nativechecks.')
