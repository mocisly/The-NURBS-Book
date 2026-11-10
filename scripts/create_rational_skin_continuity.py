"""10.10true rational skin with a certified finite denominator and a true crease."""
from pathlib import Path
from fractions import Fraction as F
import json
from rational_skin_continuity_data import construct,U,P,HP,positive_pieces
from native_bspline import segments,check,cubic_path,point,de_boor
from rational_geometry import approximate
from surface_geometry import isocurve,surface
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in m['images'] if e['tex']=='image_tex/ch10/fig_10_13.tex')['applied']
base,VP,r=construct()
def view(p):
    x,y,z=p;return(F(11,10)*(F(4,5)*x+F(3,5)*y),F(11,10)*(-F(9,25)*x+F(12,25)*y+F(4,5)*z))
def viewH(p):return view(p[:3])+(p[3],)
out=['% Printed positive weights, exact C1 section projections, true C0 rational skin. All geometry from explicit controls.',r'\begin{tikzpicture}[book line]'];proof=[]
for letter,shift in [('a',0),('b',18)]:
    out.extend([r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-6.5,-8) rectangle (10.5,8.2);'])
    nc=cross=pieces=0;maxerr=F(0);bounds=[]
    def path(bern,style=''):
        global pieces,maxerr
        for a,b,C in positive_pieces(bern):
            native=approximate(tuple(viewH(p) for p in C),F(1,10000));maxerr=max(maxerr,max(p['certified_l1_error'] for p in native));pieces+=len(native)
            for s in native:bounds.extend(s['bern']);out.append(cubic_path(s,style))
    if letter=='a':
        for k,(row,hom) in enumerate(zip(P,HP)):
            ss=segments(U,hom,2);nc+=check(U,hom,2,ss,steps=11)
            out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(p)) for p in row)+';')
            for s in ss:path(s['bern'])
            out.extend(r'\fill '+point(view(p))+r' circle[radius=1.2pt];' for p in row)
            out.append(r'\node[below left=5pt] at '+point(view(row[0]))+r' {$C_'+str(k)+r'(u)$};')
        title=r'$C_k(u)\in C^1,\qquad p=2$'
    else:
        for variable,fixed in [('u',tuple(sorted(set(tuple(F(i,32) for i in range(33))+VP)))),('v',tuple(F(i,20) for i in range(21)))]:
            for t in fixed:
                K,p,C=isocurve(*base,variable,t);ss=segments(K,C,p);nc+=check(K,C,p,ss,steps=3)
                for s in (F(0),F(1,3),F(2,3),F(1)):
                    assert de_boor(K,C,p,s)==(surface(*base,s,t) if variable=='u' else surface(*base,t,s));cross+=1
                for s in ss:path(s['bern'],'book grid')
        for hom in HP:
            for s in segments(U,hom,2):path(s['bern'])
        K,p,C=isocurve(*base,'v',F(1,2))
        for s in segments(K,C,p):path(s['bern'],'line width=1pt')
        title=r'$u=1/2:\quad S_u^-\ne S_u^+$'
    assert all(-F(13,2)<p[0]<F(21,2) and -F(8)<p[1]<F(41,5) for p in bounds)
    origin=(-F(23,5),-F(13,2))
    for end,name,anchor in [((F(6,5),0,0),'x','below'),((0,F(6,5),0),'y','right'),((0,0,F(6,5)),'z','above')]:
        to=tuple(a+b for a,b in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(to)+r' node['+anchor+r'=4pt] {$'+name+'$};')
    out.extend([r'\node at (2,7.7) {'+title+'};',r'\node at (2,-7.6) {('+letter+')};',r'\end{scope}'])
    proof.append(dict(panel=letter,native_homogeneous_checks=nc,isocurve_tensor_identities=cross,native_cubic_pieces=pieces,certified_native_L1_error_cm=str(maxerr),camera_scale='1.1',font_rescaling=False,all_native_curve_control_hulls_inside_bounds=True))
out.append(r'\end{tikzpicture}');(root/'image_tex/ch10/fig_10_13.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(native_panels=proof,no_contour_tracing=True)
(root/'image_tex/build/rational-skin-continuity-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print('PASS10.10native:',sum(p['native_homogeneous_checks'] for p in proof),'checks;',sum(p['native_cubic_pieces'] for p in proof),'certified rational pieces;wholeW>1/2;true geometric seam jumps.')
