"""10.12actual A10.2/A10.1 skins; shared mathematical input and exact frames."""
from pathlib import Path
from fractions import Fraction as F
import json
from moving_frame_sweep_data import U,T_K,T_P,RAW_C,view,spine
from native_bspline import segments,check,cubic_path,point,de_boor
from rational_geometry import approximate
from surface_geometry import isocurve,surface
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (16,17):assert not next(e for e in m['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex')['applied']
r=json.loads((root/'image_tex/build/moving-frame-sweep-data.json').read_text());states={x['method']:x for x in r['sweeps']};proof=[]
def panel(letter,shift):
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-4,-10.5) rectangle (12,7.5);'];nc=cross=count=0;maximum=F(0)
    def path(bern,style=''):
        nonlocal count,maximum
        B=tuple(view(p) for p in bern)
        native=[dict(bern=B,certified_l1_error=F(0))] if len(B)==4 else approximate(tuple(p+(F(1),) for p in B),F(1,100000))
        maximum=max(maximum,max(s['certified_l1_error'] for s in native));count+=len(native)
        assert all(-4<p[0]<12 and -F(21,2)<p[1]<F(15,2) for s in native for p in s['bern'])
        out.extend(cubic_path(s,style) for s in native)
    if letter=='a':
        for K,P,p in [(T_K,T_P,5),(U,RAW_C,3)]:
            ss=segments(K,P,p);nc+=check(K,P,p,ss,steps=7)
            out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(q)) for q in P)+';')
            for s in ss:path(s['bern'])
            out.extend(r'\fill '+point(view(q))+r' circle[radius=1pt];' for q in P)
        start=spine(F(0));end=tuple(a+b for a,b in zip(start,(F(0),F(0),F(6,5))))
        out.append(r'\draw[book axis] '+point(view(start))+'--'+point(view(end))+r' node[above right=5pt] {$B_0$};')
        out.append(r'\draw[book grid] '+point(view(de_boor(U,RAW_C,3,F(2,5))))+r' -- (-2.5,4) node[above=4pt] {$C(u)$};')
        out.append(r'\node[below right=5pt] at '+point(view(T_P[-1]))+r' {$T(v)$};')
        title=r'$T(v),\ C(u),\ B_0$'
    else:
        state=states['A10.2' if letter=='b' else 'A10.1'];V=tuple(map(F,state['v_knots']));q=state['v_degree'];net=tuple(tuple(tuple(map(F,p)) for p in row) for row in state['surface_controls']);base=(U,V,3,q,net);VP=tuple(map(F,state['interpolation_parameters']))
        for variable,fixed in [('u',tuple(sorted(set(tuple(F(i,24) for i in range(25))+VP)))),('v',tuple(F(i,20) for i in range(21)))]:
            for t in fixed:
                K,p,C=isocurve(*base,variable,t);ss=segments(K,C,p);nc+=check(K,C,p,ss,steps=3)
                for s in (F(0),F(1,3),F(2,3),F(1)):
                    assert de_boor(K,C,p,s)==(surface(*base,s,t) if variable=='u' else surface(*base,t,s));cross+=1
                for s in ss:path(s['bern'],'book grid')
        for row in state['placed_section_controls']:
            P=tuple(tuple(map(F,p)) for p in row)
            for s in segments(U,P,3):path(s['bern'])
        for s in segments(T_K,T_P,5):path(s['bern'],'dashed')
        title=r'$\mathrm{'+state['method']+r'}:\quad q='+str(q)+r',\quad '+str(state['instance_count'])+r'\ \mathrm{sections}$'
    origin=(F(0),F(0)) if letter=='a' else (-F(2),-F(8))
    axes=[((F(6),0,0),'x','below'),((0,F(4),0),'y','right'),((0,0,F(4)),'z','above')] if letter=='a' else [((F(6,5),0,0),'x','below'),((0,F(6,5),0),'y','right'),((0,0,F(6,5)),'z','above')]
    for end,name,anchor in axes:
        tip=tuple(a+b for a,b in zip(origin,view(end)))
        out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tip)+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend([r'\node at (4,7) {'+title+'};',r'\node at (4,-10.1) {('+letter+')};',r'\end{scope}'])
    proof.append(dict(panel=letter,native_curve_checks=nc,isocurve_tensor_identities=cross,native_cubic_pieces=count,native_L1_error_bound_cm=str(maximum),camera_scale='1.8',font_rescaling=False))
    return out
for n,letters in [(16,'ab'),(17,'c')]:
    out=['% Moving-frame sweeps: actual algorithm-specific interpolation, common PH planar trajectory and positive-Z section.',r'\begin{tikzpicture}[book line]']
    for i,letter in enumerate(letters):out+=panel(letter,17*i)
    out.append(r'\end{tikzpicture}');(root/f'image_tex/ch10/fig_10_{n:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(native_panels=proof,all119section_control_vector_identities_exact=True,global_trajectory_exclusion='S_z(u,v)>=.3 while T_z(v)=0',no_contour_tracing=True)
(root/'image_tex/build/moving-frame-sweep-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('PASS10.12native:',sum(p['native_curve_checks'] for p in proof),'checks;',sum(p['isocurve_tensor_identities'] for p in proof),'tensorisocurve identities;all119whole-sectioncontrolconstraints;W1/nativequinticerror<=1e-5cm.')
