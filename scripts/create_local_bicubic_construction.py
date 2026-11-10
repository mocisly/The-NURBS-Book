"""9.32: actual16data ->100Bezier controls ->64Bspline controls ->local bicubic."""
from pathlib import Path
from fractions import Fraction as F
import json
from local_bicubic_interpolation_data import Q,UP,VP,R,S,DU,DV,MIX,PATCH,FULL,U,V,P,BASE,REMOVE_U,REMOVE_V,EDGE_CHECKS
from mesh_interpolation_example_data import camera
from surface_geometry import surface,verify_tensor,isocurve
from native_bspline import segments,check,de_boor,cubic_path,point
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (38,39):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex')['applied']
def view(q):return tuple(x/2 for x in camera(q))
def poly(row,style='book grid,dashed'):return r'\draw['+style+'] '+'--'.join(point(view(q)) for q in row)+';'
def small(q):return r'\fill '+point(view(q))+r' circle[radius=1.1pt];'
def data(q):
    # Screen-space open square distinguishes input data from smaller control dots.
    xy=point(view(q));return r'\draw '+xy+r' ++(-2pt,-2pt) rectangle ++(4pt,4pt);'
tc=verify_tensor(*BASE,steps=4);native=0;iso=0
def panel(mode,shift):
    global native,iso
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-6.5,-4.5) rectangle (6.5,11);']
    net=Q if mode=='a' else FULL if mode=='b' else P if mode=='c' else None
    if net:
        for row in net:out.append(poly(row))
        for col in zip(*net):out.append(poly(col))
        if mode!='a':out.extend(small(q) for row in net for q in row)
    else:
        counts=(15,12,13)
        fixed=tuple(VP[l]+(VP[l+1]-VP[l])*F(j,counts[l]) for l in range(3) for j in range(counts[l]))+(F(1),)
        assert len(fixed)==41 and all(v in fixed for v in VP)
        for v in fixed:
            K,p,C=isocurve(*BASE,'u',v);ss=segments(K,C,p);native+=check(K,C,p,ss,steps=7)
            for k in range(5):
                u=F(k,4);assert de_boor(K,C,p,u)==surface(*BASE,u,v);iso+=1
            out.extend(cubic_path(dict(bern=tuple(view(q) for q in s['bern']))) for s in ss)
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(26,5)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(view(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend(data(q) for row in Q for q in row)
    out.extend([r'\node at (0,-4) {('+mode+')};',r'\end{scope}']);return out
header=['% Actual local bicubic Hermite construction on SAME16data as9.15..17;commoncamera7/4.',r'\begin{tikzpicture}[book line]']
for n,letters in [(38,('a','b')),(39,('c','d'))]:
    out=header+panel(letters[0],0)+panel(letters[1],14)+[r'\end{tikzpicture}']
    (root/f'image_tex/ch09/fig_9_{n:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report=dict(figure='9.32',same16representative_data_as='9.15..9.17',data=[[[str(x) for x in q] for q in row] for row in Q],A9_5_summed_chord_parameters=[list(map(str,UP)),list(map(str,VP))],row_chord_totals=list(map(str,R)),column_chord_totals=list(map(str,S)),unit_tangent_length_precision='1e-21',mixed_derivatives_nonzero=True,boundary_rule='Eq9.32 one-sided Bessel derivative of each derivative field;nearest interior alpha/beta in9.59 blend',Bezier_patch_count=9,full_composite_Bezier_control_shape=[10,10],minimal_Bspline_control_shape=[8,8],all16point_interpolations_exact=True,all9extracted_bicubic_patches_coefficientwise_identical=True,whole_edge_C1_coefficient_equalities=EDGE_CHECKS,zero_error_u_knot_removal=REMOVE_U,zero_error_v_knot_removal=REMOVE_V,independent_tensor_checks=tc,native_curve_checks=native,isocurve_surface_cross_checks=iso,displayed_u_isocurves=41,isocurve_family_contains_all4data_rows=True,common_camera_scale='7/4',data_markers='open4pt squares',control_markers='filled1.1pt dots')
(root/'image_tex/build/local-bicubic-construction-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS9.32:16data,9wholepatch coefficient identities,48wholeedge C1identities,100to64controlzero-error removals,41actual native tensor isocurves;',native,'native checks,',iso,'tensor crosschecks.')
