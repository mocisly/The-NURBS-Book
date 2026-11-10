"""10.3: original sections, exact common representation and interpolating skin."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from surface_geometry import isocurve,surface
from skinning_compatibility_data import construct
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (4,5,6):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex')['applied']
original,compatible,VP,base,report=construct();U,V,p,q,net=base
def view(P):
    x,y,z=P
    return(F(6,5)*(-F(4,5)*x+F(3,5)*y),F(6,5)*(-F(9,25)*x-F(12,25)*y+F(4,5)*z))
proof=[]
def panel(letter,shift=0):
    low,high=-F(21,5),F(24,5)
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-6.8,'+str(float(low))+') rectangle (6.8,'+str(float(high))+');']
    checks=iso=pieces=0
    if letter in 'ab':
        for k,(K,degree,P) in enumerate(original):
            if letter=='b':K,degree,P=U,3,compatible[k]
            ss=segments(K,P,degree);checks+=check(K,P,degree,ss,steps=7)
            out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(v)) for v in P)+';')
            out.extend(cubic_path(dict(bern=tuple(view(v) for v in s['bern']))) for s in ss);pieces+=len(ss)
            out.extend(r'\fill '+point(view(v))+r' circle[radius=.95pt];' for v in P)
            out.append(r'\node[above left=5pt] at '+point(view(P[0]))+r' {$C_'+str(k)+r'$};')
    elif letter=='c':
        for rows in (net,tuple(zip(*net))):
            for row in rows:out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(v)) for v in row)+';')
        out.extend(r'\fill '+point(view(v))+r' circle[radius=1pt];' for row in net for v in row)
    else:
        for variable,fixed,style in [('u',tuple(sorted(set(tuple(F(i,24) for i in range(25))+VP))),'book grid'),('v',tuple(sorted(set(tuple(F(i,20) for i in range(21))+U))),'book grid')]:
            for t in fixed:
                K,degree,P=isocurve(*base,variable,t);ss=segments(K,P,degree);checks+=check(K,P,degree,ss,steps=3)
                for s in (F(0),F(1,3),F(2,3),F(1)):
                    assert de_boor(K,P,degree,s)==(surface(*base,s,t) if variable=='u' else surface(*base,t,s));iso+=1
                out.extend(cubic_path(dict(bern=tuple(view(v) for v in z['bern'])),style) for z in ss);pieces+=len(ss)
        for K,degree,P in original:
            out.extend(cubic_path(dict(bern=tuple(view(v) for v in z['bern']))) for z in segments(K,P,degree))
    out.extend([r'\node at (0,'+str(float(high-F(1,4)))+') {'+{'a':r'$p_k=1,2,1,2,3$','b':r'$p=3,\quad 22\ \mathrm{controls/section}$','c':r'$22\times5\ \mathrm{control\ net}$','d':r'$p=q=3,\quad S(u,\bar v_k)=C_k(u)$'}[letter]+'};',r'\node at (0,'+str(float(low+F(3,10)))+') {('+letter+')};',r'\end{scope}'])
    proof.append(dict(panel=letter,native_checks=checks,native_pieces=pieces,isocurve_tensor_identities=iso,orthographic_camera_scale='1.2',font_rescaling=False))
    return out
for n,letters in [(4,'a'),(5,'bc'),(6,'d')]:
    out=['% Semantic 10.3: prescribed degrees and knots; representative Greville-Y control heights, exact whole-section interpolation.',r'\begin{tikzpicture}[book line]']
    for i,letter in enumerate(letters):out+=panel(letter,14.6*i)
    out.append(r'\end{tikzpicture}');(root/f'image_tex/ch10/fig_10_{n:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report.update(native_panels=proof,layout='A centered,BC aligned row,D centered; common orthographic camera and native10pt font',no_contour_tracing=True)
(root/'image_tex/build/skinning-compatibility-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS10.3:',sum(p['native_checks'] for p in proof),'native checks;',sum(p['isocurve_tensor_identities'] for p in proof),'isocurve identities;480 coefficient identities;all110 complete-section control identities.')
