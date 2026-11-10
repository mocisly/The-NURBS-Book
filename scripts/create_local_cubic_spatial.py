"""9.58:actual mixed3Dfits and25piece exact interpolant,common projected geometry."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from local_cubic_spatial_data import Q
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (70,71):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n}.tex')['applied']
r=json.loads((root/'image_tex/build/local-cubic-spatial-data.json').read_text());assert len(r['panels'])==3
panels={p['letter']:p for p in r['panels']};proof=[]
def view(p):
    x,y,z=p;return(F(12,5)*(-F(4,5)*x+F(9,10)*y),F(12,5)*(-F(2,5)*x-F(7,20)*y+z))
def panel(letter,shift):
    p=panels[letter];U=tuple(map(F,p['U']));P=tuple(tuple(map(F,q)) for q in p['controls']);ss=segments(U,P,3);native=check(U,P,3,ss,steps=13)
    assert all(-F(78,10)<view(q)[0]<F(78,10) and -F(47,10)<view(q)[1]<12 for q in P)
    K=tuple(sorted(set(U)));assert len(K)==len(p['pieces'])+1;interpolated=set();squares=[];identity=0
    for i,piece in enumerate(p['pieces']):
        C=tuple(tuple(map(F,q)) for q in piece['controls'])
        for j,t in enumerate(map(F,piece['projection_parameters'])):
            value=de_boor(U,P,3,K[i]+(K[i+1]-K[i])*t);assert value==de_boor((F(0),)*4+(F(1),)*4,C,3,t);identity+=1
            q=Q[piece['start']+j];sq=sum((a-b)**2 for a,b in zip(value,q));squares.append(sq)
            if sq==0:interpolated.add(piece['start']+j)
    assert max(squares)<=F(p['tolerance'])**2
    if letter=='c':assert interpolated==set(range(51))
    out=[r'\begin{scope}[xshift='+str(float(shift))+r'cm]',r'\path[use as bounding box] (-7.8,-4.7) rectangle (7.8,12);']
    for end,name,anchor in [((F(16,5),0,0),'x','below left'),((0,F(16,5),0),'y','below right'),((0,0,F(43,10)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(view(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(q)) for q in P)+';')
    out.extend(cubic_path(dict(bern=tuple(view(q) for q in s['bern']))) for s in ss)
    out.extend(r'\fill '+point(view(q))+r' circle[radius=1pt];' for q in Q)
    for index in p['segment_boundaries']:
        out.append(r'\draw '+point(view(Q[index]))+r' ++(-2.3pt,-2.3pt) rectangle ++(4.6pt,4.6pt);')
    out.extend([r'\node at (0,11.55) {$E='+p['tolerance']+r',\ K_{\max}=20$};',r'\node at (0,-4.25) {('+letter+')};',r'\end{scope}'])
    proof.append(dict(letter=letter,native_checks=native,all_data_global_local_curve_identities=identity,maximum_actual_3D_distance=float(max(squares))**.5,exactly_interpolated_data_count=len(interpolated),common_camera_scale='2.4',common_bounds=[[-7.8,-4.7],[7.8,12]],font_rescaling=False))
    return out
for n,letters in [(70,'ab'),(71,'c')]:
    out=['% Actual51point3Dfits,planarendsections/skewconnector;exactzero-toleranceinterpolant;no raster geometry.',r'\begin{tikzpicture}[book line]']
    for i,letter in enumerate(letters):out+=panel(letter,F(169,10)*i)
    out.append(r'\end{tikzpicture}');(root/f'image_tex/ch09/fig_9_{n}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(native_panels=proof,common_camera=True,exact_all51interpolation_in_C=True,zero_tolerance_no_minimality_claim=True)
(root/'image_tex/build/local-cubic-spatial-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
print('PASS9.58native:',sum(x['native_checks'] for x in proof),'checks;allglobal-localdatasamples/3Derrors exact,C all51points0,all3C1/commoncamera/font.')
