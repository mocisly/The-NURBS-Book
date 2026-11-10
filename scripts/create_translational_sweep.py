"""10.11same exact input curves and surface S(u,v)=C(u)+T(v)."""
from pathlib import Path
from fractions import Fraction as F
import json
from translational_sweep_data import U,V,Q,T,NET,view
from native_bspline import segments,check,cubic_path,point,de_boor
from surface_geometry import surface,isocurve,verify_tensor
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (14,15):assert not next(e for e in m['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex')['applied']
base=(U,V,3,3,NET)
assert Q[0]==Q[-1] and de_boor(U,Q,3,F(1,3))==(0,0,0)
assert all(NET[i][j]==tuple(a+b for a,b in zip(Q[i],T[j])) for i in range(10) for j in range(7))
for i in range(7):
    for j in range(7):
        u,v=F(i,6),F(j,6);assert surface(*base,u,v)==tuple(a+b for a,b in zip(de_boor(U,Q,3,u),de_boor(V,T,3,v)))
proof=[]
for n,letter in [(14,'a'),(15,'b')]:
    out=['% Exact translational sweep from explicit closed B-section and spatial cubic trajectory;allweights1.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-7.5,-4.5) rectangle (8.5,9.5);'];nc=cross=pieces=0
    if letter=='a':
        for K,P in [(U,Q),(V,T)]:
            ss=segments(K,P,3);nc+=check(K,P,3,ss,steps=13)
            out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(p)) for p in P)+';')
            out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern']))) for s in ss);pieces+=len(ss)
            out.extend(r'\fill '+point(view(p))+r' circle[radius=1pt];' for p in P)
        out.append(r'\node[above=6pt] at '+point(view(T[0]))+r' {$T(v)$};')
        out.append(r'\draw[book grid] '+point(view(de_boor(U,Q,3,F(11,20))))+r' -- (3,2.8) node[above=3pt] {$C(u)$};')
        title=r'$C(u),\quad T(v)$'
    else:
        for variable,fixed in [('u',tuple(F(i,24) for i in range(25))),('v',tuple(F(i,24) for i in range(25)))]:
            for t in fixed:
                K,p,C=isocurve(*base,variable,t);ss=segments(K,C,p);nc+=check(K,C,p,ss,steps=3)
                for s in (F(0),F(1,3),F(2,3),F(1)):
                    assert de_boor(K,C,p,s)==(surface(*base,s,t) if variable=='u' else surface(*base,t,s));cross+=1
                out.extend(cubic_path(dict(bern=tuple(view(p) for p in z['bern'])),'book grid') for z in ss);pieces+=len(ss)
        for v in (F(0),F(1)):
            K,p,C=isocurve(*base,'u',v)
            out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern']))) for s in segments(K,C,p))
        out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern'])),'line width=1pt') for s in segments(V,T,3))
        title=r'$S(u,v)=T(v)+C(u)$'
    for end,name,anchor in [((F(4),0,0),'x','below'),((0,F(4),0),'y','right'),((0,0,F(5)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(view(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend([r'\node at (.5,9) {'+title+'};',r'\node at (.5,-4.1) {('+letter+')};',r'\end{tikzpicture}'])
    (root/f'image_tex/ch10/fig_10_{n:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
    proof.append(dict(panel=letter,native_curve_checks=nc,tensor_isocurve_identities=cross,native_pieces=pieces,camera_scale='1.6',font_rescaling=False))
report=dict(figure='10.11',representative_controls=True,section_knots=list(map(str,U)),trajectory_knots=list(map(str,V)),section_controls=[[str(x) for x in q] for q in Q],trajectory_controls=[[str(x) for x in q] for q in T],all_weights=1,surface_control_shape=[10,7],all70exact_tensor_control_sums=True,independent_sum_formula_checks=49,tensor_checks=verify_tensor(*base,steps=3),closed_section_and_surface_u=True,section_at_u_one_third_exactly_origin=True,whole_trajectory_exact_surface_isocurve='S(1/3,v)=T(v)',native_panels=proof,no_contour_tracing=True)
(root/'image_tex/build/translational-sweep-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print('PASS10.11:70tensorcontrol sums/49independent formula checks;',sum(p['native_curve_checks'] for p in proof),'native checks,closedu/exacttrajectoryiso.')
