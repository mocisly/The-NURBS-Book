"""10.16actual skin through exact Frenet-oriented sections,with a true collapsed iso."""
from pathlib import Path
from fractions import Fraction as F
import json
from frenet_flip_data import U,T_K,T_P,view
from native_bspline import segments,check,cubic_path,point,de_boor
from rational_geometry import approximate
from surface_geometry import surface,isocurve
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in m['images'] if e['tex']=='image_tex/ch10/fig_10_23.tex')['applied']
r=json.loads((root/'image_tex/build/frenet-flip-data.json').read_text());V=tuple(map(F,r['v_knots']));net=tuple(tuple(tuple(map(F,p)) for p in row) for row in r['surface_controls']);base=(U,V,3,3,net);VP=tuple(map(F,r['interpolation_parameters']))
out=['% Actual Frenet-oriented skin. Exact opposite binormal limits and antisymmetric interpolation make S_hat(u,.5)=0 for ALLu.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-9.5,-8) rectangle (9.5,9.5);'];nc=cross=count=0
def path(B,style=''):
    global count
    B=tuple(view(p) for p in B);assert len(B)==4 and all(-F(19,2)<p[0]<F(19,2) and -8<p[1]<F(19,2) for p in B)
    out.append(cubic_path(dict(bern=B),style));count+=1
for variable,fixed in [('u',tuple(sorted(set(tuple(F(i,32) for i in range(33))+VP)))),('v',tuple(F(i,20) for i in range(21)))]:
    for t in fixed:
        K,p,P=isocurve(*base,variable,t);ss=segments(K,P,p);nc+=check(K,P,p,ss,steps=3)
        for s in (F(0),F(1,3),F(2,3),F(1)):
            assert de_boor(K,P,p,s)==(surface(*base,s,t) if variable=='u' else surface(*base,t,s));cross+=1
        for s in ss:path(s['bern'],'book grid')
for row in r['placed_section_controls']:
    P=tuple(tuple(map(F,p)) for p in row)
    for s in segments(U,P,3):path(s['bern'])
ts=segments(T_K,T_P,5);nc+=check(T_K,T_P,5,ts,steps=21)
native=approximate(tuple(view(p)+(F(1),) for p in T_P),F(1,100000));assert max(s['certified_l1_error'] for s in native)<=F(1,100000)
out.extend(cubic_path(s,'dashed') for s in native)
K,p,P=isocurve(*base,'u',F(1,2));assert P==((F(0),)*3,)*7
out.append(r'\draw (0,0) circle[radius=2.5pt];')
for end,name,anchor in [((F(9,2),0,0),'x','below left'),((0,F(6),0),'y','right'),((0,0,F(4)),'z','above')]:
    out.append(r'\draw[book grid,book axis] (0,0)--'+point(view(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
out.extend([r'\node at (0,8.8) {$B(1/2^-)=-B(1/2^+)$};',r'\node at (0,-7.4) {$\widehat S(u,1/2)=\mathbf0$};',r'\end{tikzpicture}'])
(root/'image_tex/ch10/fig_10_23.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(native_curve_checks=nc,tensor_isocurve_identities=cross,native_cubic_surface_pieces=count,quintic_reference_native_pieces=len(native),reference_native_L1_error_bound_cm='1e-5',surface_native_error='0',camera_scale='2.2',font_rescaling=False,no_contour_tracing=True)
(root/'image_tex/build/frenet-flip-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('PASS10.16native:',nc,'checks;',cross,'tensorisoidentities;actualentiremidsectionzero/Frenetnormalreversalexact.')
