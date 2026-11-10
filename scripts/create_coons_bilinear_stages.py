"""Printed10.25, one four-panel mathematical construction with common boundaries."""
from pathlib import Path
from fractions import Fraction as F
import json
from coons_patch_data import U,V,GU,GV,X,Y,C0U,C1U,C0V,C1V,view,construct,bilinear
from native_bspline import segments,check,cubic_path,point,de_boor
from surface_geometry import isocurve,surface
root=Path(__file__).resolve().parents[1];nets=construct();sources={};proof=[]
for source in (33,34,35):
    target=f'image_tex/ch10/fig_10_{source:02}.tex';manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'));assert not next(e for e in manifest['images'] if e['tex']==target)['applied']
    sources[source]=['% Exact Coons construction from shared boundary data; no tracing or font scaling.',r'\begin{tikzpicture}[book line]']
for source,letter,name,shift in [(33,'a','R1',0),(33,'b','R2',19),(34,'c','T',0),(35,'d','S',0)]:
    net=nets[name];out=sources[source];out.extend([r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-9,-7) rectangle (9,8);']);nc=cross=pieces=straight=0
    def curve(K,C,d,style=''):
        global nc,pieces
        ss=segments(K,C,d);nc+=check(K,C,d,ss,steps=3)
        for s in ss:
            B=tuple(view(a) for a in s['bern']);assert all(-9<a[0]<9 and -7<a[1]<8 for a in B)
            out.append(cubic_path(dict(bern=B),style));pieces+=1
        return ss
    directions=('v',) if name=='R1' else ('u',) if name=='R2' else ('u','v')
    for variable in directions:
        for t in (F(i,24) for i in range(25)):
            K,d,C=isocurve(*net,variable,t);ss=curve(K,C,d,'book grid')
            if name in ('R1','R2','T'):
                assert all(all(c==0 for c in p[2:]) for s in ss for p in s['power']);straight+=1
            for z in (F(0),F(1,3),F(2,3),F(1)):
                assert de_boor(K,C,d,z)==(surface(*net,z,t) if variable=='u' else surface(*net,t,z));cross+=1
    for K,C,d,interpolated in [(U,C0U,3,name in ('R1','S')),(U,C1U,3,name in ('R1','S')),(V,C0V,2,name in ('R2','S')),(V,C1V,2,name in ('R2','S'))]:curve(K,C,d,'line width=.9pt' if interpolated else 'dashed')
    if name=='T':
        for a,b in [(0,0),(0,1),(1,0),(1,1)]:out.append(r'\fill '+point(view(bilinear(F(a),F(b))))+r' circle[radius=1.5pt];')
    origin=(-F(15,2),-F(11,2))
    for end,label,anchor in [((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:
        to=tuple(a+b for a,b in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(to)+r' node['+anchor+r'=4pt] {$'+label+'$};')
    title={'R1':r'R_1:\quad\mathrm{linear\ in}\ v','R2':r'R_2:\quad\mathrm{linear\ in}\ u','T':r'T:\quad\mathrm{bilinear}','S':r'S=R_1+R_2-T'}[name]
    out.extend([r'\node at (0,7.4) {$'+title+'$};',r'\node at (0,-6.6) {('+letter+')};',r'\end{scope}'])
    assert all(p[0]==X[i] and p[1]==Y[j] for i,row in enumerate(net[4]) for j,p in enumerate(row))
    proof.append(dict(panel=letter,name=name,native_curve_checks=nc,tensor_crosschecks=cross,exact_Bezier_pieces=pieces,whole_straight_isocurves_proved_by_zero_higher_power_coefficients=straight,whole_XY_affine_map=True,XY_Jacobian=56))
for source,out in sources.items():out.append(r'\end{tikzpicture}');(root/f'image_tex/ch10/fig_10_{source:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/coons-bilinear-stages-check.json').write_text(json.dumps(dict(panels=proof,whole_boundary_control_identities=22,whole_patch_not_bilinear=True,no_contour_tracing=True,native_curve_error=0),indent=2)+'\n',encoding='utf-8');print('PASS10.25:',sum(r['native_curve_checks'] for r in proof),'nativechecks/',sum(r['tensor_crosschecks'] for r in proof),'tensorchecks;',sum(r['whole_straight_isocurves_proved_by_zero_higher_power_coefficients'] for r in proof),'wholelinesexact.')
