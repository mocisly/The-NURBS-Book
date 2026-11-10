"""10.14true nonplanar path, exact orthogonal frames and trajectory-preserving skin."""
from pathlib import Path
from fractions import Fraction as F
import json
from spatial_frame_sweep_data import U,T_K,T_P,C,view,trajectory,frame
from native_bspline import segments,check,cubic_path,point,de_boor
from surface_geometry import surface,isocurve
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (20,21):assert not next(e for e in m['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex')['applied']
r=json.loads((root/'image_tex/build/spatial-frame-sweep-data.json').read_text());proof=[]
def panel(letter,shift):
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-8.5,-5) rectangle (8.5,9);'];nc=cross=count=0
    def path(B,style=''):
        nonlocal count
        B=tuple(view(p) for p in B);assert len(B)==4
        assert all(-F(17,2)<p[0]<F(17,2) and -5<p[1]<9 for p in B)
        out.append(cubic_path(dict(bern=B),style));count+=1
    if letter=='a':
        for K,P in [(T_K,T_P),(U,C)]:
            ss=segments(K,P,3);nc+=check(K,P,3,ss,steps=7)
            out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(p)) for p in P)+';')
            for s in ss:path(s['bern'])
            out.extend(r'\fill '+point(view(p))+r' circle[radius=1pt];' for p in P)
        start=trajectory(F(0));B=frame(F(0))[2];end=tuple(a+F(6,5)*b for a,b in zip(start,B))
        out.append(r'\draw[book axis] '+point(view(start))+'--'+point(view(end))+r' node[above right=5pt] {$B_0$};')
        out.append(r'\node[below left=5pt] at '+point(view(start))+r' {$T(v)$};')
        out.append(r'\node[below left=5pt] at '+point(view(C[-1]))+r' {$C(u)$};')
        out.append(r'\draw (0,0) circle[radius=2pt];');title=r'$T(v),\ C(u),\ B_0$'
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
        for s in segments(T_K,T_P,3):path(s['bern'],'dashed' if letter=='b' else 'line width=1pt')
        title=r'$\mathrm{A10.2}:\quad7\ \mathrm{sections}$' if letter=='b' else r'$\mathrm{A10.1}:\quad S(1/2,v)=T(v)$'
    origin=(F(0),F(0)) if letter=='a' else (-F(13,2),-F(3))
    axes=[((F(5),0,0),'x','below'),((0,F(4),0),'y','left'),((0,0,F(4)),'z','above')] if letter=='a' else [((F(6,5),0,0),'x','below'),((0,F(6,5),0),'y','left'),((0,0,F(6,5)),'z','above')]
    for end,name,anchor in axes:
        to=tuple(a+b for a,b in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(to)+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend([r'\node at (0,8.5) {'+title+'};',r'\node at (0,-4.6) {('+letter+')};',r'\end{scope}'])
    proof.append(dict(panel=letter,native_curve_checks=nc,tensor_isocurve_identities=cross,native_cubic_pieces=count,projection='orthographic:1.6*(.8x-.6y,-.36x-.48y+.8z)',font_rescaling=False,native_curve_error='0'))
    return out
for n,letters in [(20,'ab'),(21,'c')]:
    out=['% Actual true-spatial sweep comparison;exact cubic polynomial path/rational orthonormal frames;constant(.6,.6,1)scale.',r'\begin{tikzpicture}[book line]']
    for i,letter in enumerate(letters):out+=panel(letter,18*i)
    out.append(r'\end{tikzpicture}');(root/f'image_tex/ch10/fig_10_{n:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(native_panels=proof,no_contour_tracing=True)
(root/'image_tex/build/spatial-frame-sweep-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('PASS10.14native:',sum(p['native_curve_checks'] for p in proof),'checks;',sum(p['tensor_isocurve_identities'] for p in proof),'tensoridentities;126whole-sectionconstraints/11wholetrajectorycoefficients exact.')
