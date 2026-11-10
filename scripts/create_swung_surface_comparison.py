"""10.2:actual6x11swung tensor net and unit/weighted surfaces from10.1."""
from pathlib import Path
from fractions import Fraction as F
import json
from swung_surface_example_data import P,T,U,V,WP,WT,ALPHA,homogeneous,net
from surface_geometry import surface,isocurve,verify_tensor
from native_bspline import segments,check,cubic_path,point,de_boor
from rational_geometry import project,approximate
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (2,3):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex')['applied']
plain=net(False);weighted=net(True);controls=tuple(tuple(project(h) for h in row) for row in plain[-1])
assert controls==tuple(tuple(project(h) for h in row) for row in weighted[-1])
reports=[]
for state,flag in [(plain,False),(weighted,True)]:
    a,b=(WP,WT) if flag else ((F(1),)*6,(F(1),)*11);HP=homogeneous(P,a);HT=homogeneous(T,b)
    for i in range(6):
        for j in range(11):
            expected=(ALPHA*HP[i][0]*HT[j][0],ALPHA*HP[i][0]*HT[j][1],HP[i][2]*HT[j][3],HP[i][3]*HT[j][3])
            assert state[-1][i][j]==expected
    for i in range(5):
        for j in range(5):
            u,v=F(i,4),F(j,4);p=project(de_boor(U,HP,3,u));t=project(de_boor(V,HT,3,v));actual=project(surface(*state,u,v))
            assert actual==(ALPHA*p[0]*t[0],ALPHA*p[0]*t[1],p[2])
    reports.append(dict(weighted=flag,all66homogeneous_tensor_control_factorizations_exact=True,independent_swung_formula_checks=25,tensor_checks=verify_tensor(*state,steps=2),whole_domain_positive_denominator_lower_bound='1',profile_weights=list(map(str,a)),trajectory_weights=list(map(str,b))))
def view(q):
    x,y,z=q;return(F(9,5)*(-F(4,5)*x+F(9,10)*y),F(9,5)*(-F(2,5)*x-F(7,20)*y+z))
def viewH(h):return view(h[:3])+(h[3],)
out_proof=[]
def panel(letter,shift):
    out=[r'\begin{scope}[xshift='+str(float(shift))+r'cm]',r'\path[use as bounding box] (-5.025,-3) rectangle (5.55,11.4);'];nc=iso=pieces=0
    if letter=='a':
        for rows in (controls,tuple(zip(*controls))):
            for row in rows:out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(q)) for q in row)+';')
        out.extend(r'\fill '+point(view(q))+r' circle[radius=1pt];' for row in controls for q in row)
        title=r'$6\times11$'
    else:
        state=plain if letter=='b' else weighted
        for variable,fixed,style in [('u',tuple(F(i,32) for i in range(33)),''),('v',tuple(sorted(set(tuple(F(i,16) for i in range(17))+(F(1,3),F(2,3))))),'book grid')]:
            for t in fixed:
                K,p,C=isocurve(*state,variable,t);ss=segments(K,C,p);nc+=check(K,C,p,ss,steps=3)
                for s in (F(0),F(1,3),F(2,3),F(1)):
                    assert de_boor(K,C,p,s)==surface(*state,s,t) if variable=='u' else de_boor(K,C,p,s)==surface(*state,t,s)
                    iso+=1
                for seg in ss:
                    if letter=='b':
                        assert all(h[-1]==1 for h in seg['bern']);out.append(cubic_path(dict(bern=tuple(view(h[:3]) for h in seg['bern'])),style));pieces+=1
                    else:
                        native=approximate(tuple(viewH(h) for h in seg['bern']),F(1,10000));assert max(p['certified_l1_error'] for p in native)<=F(1,10000)
                        out.extend(cubic_path(p,style) for p in native);pieces+=len(native)
        title=r'$w_{ij}=1$' if letter=='b' else r'$w_{ij}=w_i^P w_j^T$'
    for end,name,anchor in [((F(31,10),0,0),'x','below left'),((0,F(31,10),0),'y','right'),((0,0,F(29,5)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(view(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend([r'\node at (.2625,11.175) {'+title+'};',r'\node at (.2625,-2.7) {('+letter+')};',r'\end{scope}'])
    out_proof.append(dict(panel=letter,native_homogeneous_curve_checks=nc,isocurve_tensor_crosschecks=iso,native_cubic_pieces=pieces,weighted_native_render_L1_bound_cm='1e-4' if letter=='c' else '0',common_camera_scale='1.8',font_rescaling=False,common_bounds=[[-5.025,-3],[5.55,11.4]]))
    return out
for n,letters in [(2,'a'),(3,'bc')]:
    out=['% ActualswungtensorproductEq10.3..6,shared10.1data,alpha.12,sameEuclideancontrolnetforbothweights.',r'\begin{tikzpicture}[book line]']
    for i,letter in enumerate(letters):out+=panel(letter,F(451,40)*i)
    out.append(r'\end{tikzpicture}');(root/f'image_tex/ch10/fig_10_{n:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report=dict(figure='10.2',same_data_as='10.1',alpha=str(ALPHA),control_shape=[6,11],degrees=[3,3],identical_Euclidean_control_positions_for_plain_and_weighted=True,printed_weight_indices_preserved=True,constructions=reports,native_panels=out_proof,layout='ABCsinglealignedrow,allunscaledfont10pt/camera1.8',no_contour_tracing=True)
(root/'image_tex/build/swung-surface-comparison-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS10.2:all66controlfactorizations exact/bothweights,50swungformula checks;allW>=1;nativechecks',sum(p['native_homogeneous_curve_checks'] for p in out_proof),'pieces',sum(p['native_cubic_pieces'] for p in out_proof))
