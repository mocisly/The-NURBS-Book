"""10.13actual A10.2before/after printed scaling,common geometry and typography."""
from pathlib import Path
from fractions import Fraction as F
import json
from moving_frame_sweep_data import U,T_K,T_P,view,spine
from native_bspline import segments,check,cubic_path,point,de_boor
from rational_geometry import approximate
from surface_geometry import isocurve,surface
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (18,19):assert not next(e for e in m['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex')['applied']
r=json.loads((root/'image_tex/build/scaled-moving-sweep-data.json').read_text());C=tuple(tuple(map(F,p)) for p in r['local_section_controls']);proof=[]
def panel(letter,shift):
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-4,-10.5) rectangle (13,7.5);'];nc=cross=count=0;maximum=F(0)
    def path(B,style=''):
        nonlocal count,maximum
        B=tuple(view(p) for p in B);native=[dict(bern=B,certified_l1_error=F(0))] if len(B)==4 else approximate(tuple(p+(F(1),) for p in B),F(1,100000))
        maximum=max(maximum,max(s['certified_l1_error'] for s in native));count+=len(native)
        assert all(-4<p[0]<13 and -F(21,2)<p[1]<F(15,2) for s in native for p in s['bern'])
        out.extend(cubic_path(s,style) for s in native)
    if letter=='a':
        for K,P,p in [(T_K,T_P,5),(U,C,3)]:
            ss=segments(K,P,p);nc+=check(K,P,p,ss,steps=7)
            out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(p)) for p in P)+';')
            for s in ss:path(s['bern'])
            out.extend(r'\fill '+point(view(p))+r' circle[radius=1pt];' for p in P)
        start=spine(F(0));end=tuple(a+b for a,b in zip(start,(F(0),F(0),F(6,5))))
        out.append(r'\draw[book axis] '+point(view(start))+'--'+point(view(end))+r' node[above right=5pt] {$B_0$};')
        out.append(r'\draw[book grid] '+point(view(de_boor(U,C,3,F(2,5))))+r' -- (-2.5,4) node[above=4pt] {$C(u)$};')
        out.append(r'\node[below right=5pt] at '+point(view(T_P[-1]))+r' {$T(v)$};')
        out.append(r'\draw (0,0) circle[radius=2pt];')
        title=r'$C(1/2)=\mathbf0$'
    else:
        state=r['sweeps'][0 if letter=='b' else 1];V=tuple(map(F,state['v_knots']));net=tuple(tuple(tuple(map(F,p)) for p in row) for row in state['surface_controls']);base=(U,V,3,3,net);VP=tuple(map(F,state['interpolation_parameters']))
        for variable,fixed in [('u',tuple(sorted(set(tuple(F(i,24) for i in range(25))+VP)))),('v',tuple(F(i,20) for i in range(21)))]:
            for t in fixed:
                K,p,P=isocurve(*base,variable,t);ss=segments(K,P,p);nc+=check(K,P,p,ss,steps=3)
                for s in (F(0),F(1,3),F(2,3),F(1)):
                    assert de_boor(K,P,p,s)==(surface(*base,s,t) if variable=='u' else surface(*base,t,s));cross+=1
                for s in ss:path(s['bern'],'book grid')
        for row in state['placed_section_controls']:
            P=tuple(tuple(map(F,p)) for p in row)
            for s in segments(U,P,3):path(s['bern'])
        for s in segments(T_K,T_P,5):path(s['bern'],'dashed')
        title=r'$s_x=s_y=s_z=1$' if letter=='b' else r'$\mathbf s(v)\ \mathrm{piecewise\ linear}$'
    origin=(F(0),F(0)) if letter=='a' else (-F(2),-F(8))
    axes=[((F(6),0,0),'x','below'),((0,F(4),0),'y','right'),((0,0,F(4)),'z','above')] if letter=='a' else [((F(6,5),0,0),'x','below'),((0,F(6,5),0),'y','right'),((0,0,F(6,5)),'z','above')]
    for end,name,anchor in axes:
        tip=tuple(a+b for a,b in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tip)+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend([r'\node at (4.5,7) {'+title+'};',r'\node at (4.5,-10.1) {('+letter+')};',r'\end{scope}'])
    proof.append(dict(panel=letter,native_curve_checks=nc,tensor_isocurve_identities=cross,native_cubic_pieces=count,native_L1_error_bound_cm=str(maximum),camera_scale='1.8',font_rescaling=False))
    return out
for n,letters in [(18,'ab'),(19,'c')]:
    out=['% Exact A10.2surfaces from same origin-passing section,with/without printed piecewise linear scale.',r'\begin{tikzpicture}[book line]']
    for i,letter in enumerate(letters):out+=panel(letter,18*i)
    out.append(r'\end{tikzpicture}');(root/f'image_tex/ch10/fig_10_{n:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(native_panels=proof,no_contour_tracing=True)
(root/'image_tex/build/scaled-moving-sweep-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('PASS10.13native:',sum(p['native_curve_checks'] for p in proof),'checks;',sum(p['tensor_isocurve_identities'] for p in proof),'tensor identities;98exactsectionvectorconstraints/14trajectoryanchors.')
