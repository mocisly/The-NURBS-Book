"""9.54: analytic spiral,actualA9.11fits/control polygons and trueparameter view."""
from pathlib import Path
from fractions import Fraction as F
import json
from rational_geometry import approximate,project
from native_bspline import point,cubic_path,de_boor
from log_spiral_data import Q
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (64,65,66):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n}.tex')['applied']
r=json.loads((root/'image_tex/build/local-conic-spiral-data.json').read_text());assert [p['letter'] for p in r['panels']]==list('abcd')
panels={p['letter']:p for p in r['panels']};proof=[]
def panel(letter,shift):
    bounds=r'\path[use as bounding box] (-3.8,-3) rectangle (4.6,5.5);' if letter!='e' else r'\path[use as bounding box] (-3.8,-2.2) rectangle (4.6,3.2);'
    out=[r'\begin{scope}[xshift='+str(float(shift))+r'cm]',bounds];native=0
    if letter!='e':
        p=panels[letter]
        for piece in p['pieces']:
            H=tuple(tuple(map(F,pt)) for pt in piece['H']);controls=tuple(map(project,H))
            assert all(-F(38,10)<q[0]<F(46,10) and -3<q[1]<F(55,10) for q in controls)
            out.append(r'\draw[book grid,dashed] '+'--'.join(map(point,controls))+';')
            ss=approximate(H,F(1,10**7));assert max(s['certified_l1_error'] for s in ss)<=F(1,10**7)
            out.extend(cubic_path(s) for s in ss);native+=len(ss)
        out.extend(r'\draw '+point(q)+r' circle[radius=1.7pt];' for q in Q)
        title=r'$E='+p['tolerance']+r',\ K_{\max}='+str(p['Kmax'])+r'$'
    else:
        p=panels['b'];U=tuple(map(F,p['U']));H=tuple(tuple(map(F,q)) for q in p['homogeneous_controls'])
        for j in range(51):
            q=project(de_boor(U,H,2,F(j,50)))
            out.extend([r'\draw '+point(q)+r' ++(-2pt,0)--++(4pt,0);',r'\draw '+point(q)+r' ++(0,-2pt)--++(0,4pt);'])
        title=r'$(b):\ u=j/50,\ j=0,\ldots,50$'
    out.extend([r'\node at (.4,'+('5.1' if letter!='e' else '2.9')+') {'+title+'};',r'\node at (.4,'+('-2.75' if letter!='e' else '-1.95')+') {('+letter+')};',r'\end{scope}'])
    proof.append(dict(letter=letter,native_certified_cubic_pieces=native,native_curve_L1_tolerance='1e-7',common_coordinate_scale='1.8cm',font_rescaling=False,bounds=[[-3.8,-3],[4.6,5.5]] if letter!='e' else [[-3.8,-2.2],[4.6,3.2]],E_only_empty_vertical_space_trimmed=letter=='e'))
    return out
for n,letters in [(64,'ab'),(65,'cd'),(66,'e')]:
    out=['% Actual r=exp(theta/5)/2 samples and computed positive-weight conicfits,not raster geometry.',r'\begin{tikzpicture}[book line,x=1.8cm,y=1.8cm]']
    for i,letter in enumerate(letters):out+=panel(letter,F(33,2)*i)
    out.append(r'\end{tikzpicture}');(root/f'image_tex/ch09/fig_9_{n}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(native_panels=proof,unscaled_common_font=True,true_b_curve_parameter_markers=51,no_contour_tracing=True)
(root/'image_tex/build/local-conic-spiral-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
print('PASS9.54native:',sum(x['native_certified_cubic_pieces'] for x in proof),'certifiedpieces;all5panelscommoncamera/font,actualbNURBS51equal-parametermarks.')
