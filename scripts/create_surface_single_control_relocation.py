"""Printed11.8, actual control net and localized surface displacement, same camera."""
from pathlib import Path
from fractions import Fraction as F
import json
from surface_relocation_example_data import BASE,U,V,P,view,single
from surface_geometry import isocurve,surface
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (9,10):assert not next(e for e in manifest['images'] if e['tex']==f'image_tex/ch11/fig_11_{n:02}.tex')['applied']
new,r=single();reports=[]
for n,letter in [(9,'a'),(10,'b')]:
    out=['% Actual one-control surface relocation; exact data and whole-patch identities in surface_relocation_example_data.py.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-9,-7) rectangle (9,8);'];nc=cross=pieces=arrows=0
    def curve(net,variable,t,style='',clip=None):
        global nc,cross,pieces
        K,p,C=isocurve(*net,variable,t);ss=segments(K,C,p);nc+=check(K,C,p,ss,steps=3)
        for z in (F(0),F(1,3),F(2,3),F(1)):
            assert de_boor(K,C,p,z)==(surface(*net,z,t) if variable=='u' else surface(*net,t,z));cross+=1
        for s in ss:
            if clip and not clip[0]<=s['a']<s['b']<=clip[1]:continue
            B=tuple(view(a) for a in s['bern']);assert all(-9<a[0]<9 and -7<a[1]<8 for a in B);out.append(cubic_path(dict(bern=B),style));pieces+=1
    if letter=='a':
        for row in P:out.append(r'\draw[book grid] '+'--'.join(point(view(a)) for a in row)+';')
        for j in range(7):out.append(r'\draw[book grid] '+'--'.join(point(view(row[j])) for row in P)+';')
        for row in P:
            for a in row:out.append(r'\fill '+point(view(a))+r' circle[radius=1pt];')
        before=P[4][3];after=new[4][4][3]
        for i,j in ((3,3),(5,3),(4,2),(4,4)):out.append(r'\draw[book grid,dashed] '+point(view(P[i][j]))+'--'+point(view(after))+';')
        out.extend([r'\draw '+point(view(before))+r' circle[radius=2.5pt];',r'\draw[book axis] '+point(view(before))+'--'+point(view(after))+';',r'\fill '+point(view(after))+r' circle[radius=1.5pt];'])
        title=r'P_{4,3}\mapsto\widehat P_{4,3}'
    else:
        for variable in ('u','v'):
            for z in (F(i,10) for i in range(11)):curve(BASE,variable,z,'book grid')
        for z in tuple(map(F,('.3','.4','.5','.6','.7'))):curve(new,'u',z,'dashed',(U[4],U[8]))
        for z in tuple(map(F,('.35','.45','.55','.65','.75'))):curve(new,'v',z,'dashed',(V[3],V[6]))
        for u in tuple(map(F,('.35','.45','.55','.65','.75'))):
            for v in tuple(map(F,('.3','.4','.5','.6','.7'))):
                a,b=surface(*BASE,u,v),surface(*new,u,v);delta=tuple(y-x for x,y in zip(a,b));assert delta[0]==delta[1]==0
                if delta[2]<F(1,10):continue
                out.append(r'\draw[book grid,-{Stealth[length=3pt]}] '+point(view(a))+'--'+point(view(b))+';');arrows+=1
        a,b=r['selected_point'],r['modified_selected_point'];out.extend([r'\draw[book axis] '+point(view(a))+'--'+point(view(b))+';',r'\draw '+point(view(a))+r' circle[radius=2pt];',r'\draw '+point(view(b))+r' circle[radius=2pt];']);title=r'(\bar u,\bar v)=(.55,.55),\quad d=3/5'
    origin=(-F(15,2),-F(11,2))
    for end,label,anchor in [((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:
        to=tuple(a+b for a,b in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(to)+r' node['+anchor+r'=4pt] {$'+label+'$};')
    out.extend([r'\node at (0,7.4) {$'+title+'$};',r'\node at (0,-6.6) {('+letter+')};',r'\end{tikzpicture}'])
    (root/f'image_tex/ch11/fig_11_{n:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8');reports.append(dict(panel=letter,native_curve_checks=nc,tensor_crosschecks=cross,exact_Bezier_pieces=pieces,actual_displacement_arrows=arrows))
r.update(native_panels=reports,native_curve_error=0,no_contour_tracing=True)
(root/'image_tex/build/surface-single-control-relocation-check.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.8:',r['whole_tensor_Bezier_vector_coefficient_identities'],'wholepatch-vectorcoefficients/',r['whole_unchanged_exterior_patches'],'unchangedpatches;',sum(p['native_curve_checks'] for p in reports),'nativechecks/',sum(p['tensor_crosschecks'] for p in reports),'tensorchecks;exact(.55,.55)pointdeltaZ.6.')
