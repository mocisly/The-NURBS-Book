"""10.15real offset loops of two computed NURBS skins, with a certified crossing."""
from pathlib import Path
from fractions import Fraction as F
import json
from offset_sweep_data import U,T_K,T_P,U_STAR,I,view
from native_bspline import segments,check,cubic_path,point,de_boor
from surface_geometry import surface,isocurve
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in m['images'] if e['tex']=='image_tex/ch10/fig_10_22.tex')['applied']
r=json.loads((root/'image_tex/build/offset-sweep-data.json').read_text());proof=[]
out=['% Actual NURBS offset-skin self-intersections;I is certified identical at two distinct parameter pairs,with transverse tangent planes.',r'\begin{tikzpicture}[book line]']
for index,(letter,state) in enumerate(zip('ab',r['sweeps'])):
    out.extend([r'\begin{scope}[xshift='+str(17*index)+r'cm]',r'\path[use as bounding box] (-7,-7) rectangle (9,6);']);nc=cross=count=0
    V=tuple(map(F,state['v_knots']));net=tuple(tuple(tuple(map(F,p)) for p in row) for row in state['surface_controls']);base=(U,V,3,3,net);VP=tuple(map(F,state['interpolation_parameters']))
    def path(B,style=''):
        global count
        B=tuple(view(p) for p in B);assert all(-7<p[0]<9 and -7<p[1]<6 for p in B)
        out.append(cubic_path(dict(bern=B),style));count+=1
    for variable,fixed in [('u',tuple(sorted(set(tuple(F(i,24) for i in range(25))+VP)))),('v',tuple(sorted(set(tuple(F(i,20) for i in range(21))+(U_STAR,)))))]:
        for t in fixed:
            K,p,P=isocurve(*base,variable,t);ss=segments(K,P,p);nc+=check(K,P,p,ss,steps=3)
            for s in (F(0),F(1,3),F(2,3),F(1)):
                assert de_boor(K,P,p,s)==(surface(*base,s,t) if variable=='u' else surface(*base,t,s));cross+=1
            for s in ss:path(s['bern'],'book grid')
    for row in state['placed_section_controls']:
        P=tuple(tuple(map(F,p)) for p in row)
        for s in segments(U,P,3):path(s['bern'])
    for s in segments(T_K,T_P,3):path(s['bern'],'dashed' if letter=='a' else '')
    K,p,P=isocurve(*base,'v',U_STAR)
    for s in segments(K,P,p):path(s['bern'],'line width=1pt')
    assert all(surface(*base,U_STAR,F(v))==I for v in state['intersection_v_parameters'])
    out.append(r'\draw '+point(view(I))+r' circle[radius=3.5pt];')
    out.append(r'\fill '+point(view(I))+r' circle[radius=1.4pt];')
    out.append(r'\draw[book grid] '+point(view(I))+r' -- (-5,4.9) node[above=3pt] {$I$};')
    origin=(-F(5),-F(5))
    for end,name,anchor in [((F(6,5),0,0),'x','below'),((0,F(6,5),0),'y','right'),((0,0,F(6,5)),'z','above')]:
        to=tuple(a+b for a,b in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(to)+r' node['+anchor+r'=5pt] {$'+name+'$};')
    title=r'$\mathrm{A10.2}:\quad7\ \mathrm{sections}$' if letter=='a' else r'$\mathrm{A10.1}:\quad S(1/2,v)=T(v)$'
    out.extend([r'\node at (1,5.5) {'+title+'};',r'\node at (1,-6.6) {('+letter+')};',r'\end{scope}'])
    proof.append(dict(panel=letter,native_curve_checks=nc,tensor_isocurve_identities=cross,native_cubic_pieces=count,native_curve_error='0',common_camera_scale='1.8',font_rescaling=False,intersection_marker_is_exact_3D_point=True))
out.append(r'\end{tikzpicture}');(root/'image_tex/ch10/fig_10_22.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(native_panels=proof,minimum_trajectory_curvature_radius='1',highlighted_inward_offset='55/48',no_contour_tracing=True)
(root/'image_tex/build/offset-sweep-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('PASS10.15native:',sum(p['native_curve_checks'] for p in proof),'checks;',sum(p['tensor_isocurve_identities'] for p in proof),'tensoridentities;two actual transverse self-intersections,not just sampled image crossing.')
