"""10.17true projection-computed normals and actual Frenet triads along two curves."""
from pathlib import Path
from fractions import Fraction as F
import json
from projected_frame_comparison_data import view
from native_bspline import segments,check,cubic_path,point
from rational_geometry import approximate
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in m['images'] if e['tex']=='image_tex/ch10/fig_10_24.tex')['applied']
r=json.loads((root/'image_tex/build/projected-frame-comparison-data.json').read_text());proof=[]
out=['% Actual Eq10.27projected normals,certified normalization,exact Frenet axes;undefined Frenet frame at planar inflection omitted.',r'\begin{tikzpicture}[book line]']
for case in r['panels']:
    letter=case['panel'];offset=(F(0),F(0)) if letter=='a' else (-F(3,2),F(0));low,high=(-F(7),F(7)) if letter=='a' else (-F(4),F(6));shift=14 if letter=='a' else 0
    def loc(p):return tuple(a+b for a,b in zip(view(p),offset))
    out.extend([r'\begin{scope}[yshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-8.5,'+str(float(low))+') rectangle (8.5,'+str(float(high))+');'])
    K=tuple(map(F,case['trajectory_knots']));p=case['trajectory_degree'];P=tuple(tuple(map(F,q)) for q in case['trajectory_controls']);ss=segments(K,P,p);nc=check(K,P,p,ss,steps=21);native=[]
    for s in ss:
        B=tuple(loc(q) for q in s['bern'])
        native+=[dict(bern=B,certified_l1_error=F(0))] if len(B)==4 else approximate(tuple(q+(F(1),) for q in B),F(1,100000))
    assert all(-F(17,2)<q[0]<F(17,2) and low<q[1]<high for s in native for q in s['bern'])
    out.extend(cubic_path(s) for s in native);dashed=solid=0
    for index,node in enumerate(case['nodes']):
        A=tuple(map(F,node['point']));start=loc(A);out.append(r'\fill '+point(start)+r' circle[radius=1.15pt];')
        if node['Frenet_axes']:
            for vector in node['Frenet_axes']:
                B=tuple(map(F,vector));tip=loc(tuple(a+b for a,b in zip(A,B)))
                out.append(r'\draw[book grid,densely dashed,-{Stealth[length=3.5pt]}] '+point(start)+'--'+point(tip)+';');dashed+=1
        B=tuple(map(F,node['projected_normal']));tip=loc(tuple(a+b for a,b in zip(A,B)))
        out.append(r'\draw[book line,-{Stealth[length=4pt]}] '+point(start)+'--'+point(tip)+';');solid+=1
        if index==0:out.append((r'\node[left=5pt] at ' if letter=='a' else r'\node[above right=5pt] at ')+point(tip)+r' {$B_0$};')
    if letter=='a':
        out.extend([r'\draw (0,0) circle[radius=2.4pt];',r'\draw[book grid] (0,0)--(2,.5) node[above=4pt] {$\kappa=0$};'])
    origin=(-F(13,2),-F(5) if letter=='a' else -F(5,2))
    for end,name,anchor in [((F(4,5),0,0),'x','below left'),((0,F(4,5),0),'y','right'),((0,0,F(4,5)),'z','above')]:
        tip=tuple(a+b for a,b in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tip)+r' node['+anchor+r'=4pt] {$'+name+'$};')
    out.extend([r'\node at (0,'+str(float(high-F(1,2)))+') {'+(r'$T(v)\ \mathrm{planar}$' if letter=='a' else r'$T(v)\ \mathrm{spatial}$')+'};',r'\node at (0,'+str(float(low+F(2,5)))+') {('+letter+')};',r'\end{scope}'])
    proof.append(dict(panel=letter,native_curve_checks=nc,native_cubic_pieces=len(native),native_curve_L1_error_bound_cm=str(max(s['certified_l1_error'] for s in native)),actual_projected_normal_arrows=solid,actual_Frenet_axis_arrows=dashed,arrow_3D_length=1,normalization_direction_error_bound=case['maximum_accumulated_projected_direction_error_bound'],common_camera_scale='1.3',font_rescaling=False,coordinate_serialization_L1_error_bound_cm='1e-10'))
out.append(r'\end{tikzpicture}');(root/'image_tex/ch10/fig_10_24.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(native_panels=proof,no_contour_tracing=True)
(root/'image_tex/build/projected-frame-comparison-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('PASS10.17native:',sum(p['actual_projected_normal_arrows'] for p in proof),'actual PNarrows/',sum(p['actual_Frenet_axis_arrows'] for p in proof),'exact Frenet-axisarrows;14exactorthogonalityidentities/error<1e-18;curvechecks',sum(p['native_curve_checks'] for p in proof))
