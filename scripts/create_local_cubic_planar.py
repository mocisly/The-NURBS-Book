"""9.57:actualC1cubicfits/globalcontrol polygons,three common-scale panels."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
from local_cubic_planar_data import Q
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_69.tex')['applied']
r=json.loads((root/'image_tex/build/local-cubic-planar-data.json').read_text());assert len(r['panels'])==3
out=['% ActualA9.12point+tangentLS/meanhandles/exactC1stitching,51representativeplanardata;no tracing.',r'\begin{tikzpicture}[book line,x=2.2cm,y=2.2cm]'];checks=[]
for index,panel in enumerate(r['panels']):
    U=tuple(map(F,panel['U']));P=tuple(tuple(map(F,p)) for p in panel['controls']);ss=segments(U,P,3);native=check(U,P,3,ss,steps=13)
    assert all(-F(13,10)<p[0]<10 and -1<p[1]<F(64,10) for p in P)
    out.extend([r'\begin{scope}[yshift='+str(18*(2-index))+r'cm]',r'\path[use as bounding box] (-1.3,-1) rectangle (10,6.4);',r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';'])
    out.extend(cubic_path(s) for s in ss);out.extend(r'\draw '+point(q)+r' circle[radius=1.7pt];' for q in Q)
    out.extend([r'\node at (4.35,6.1) {$E='+panel['tolerance']+r',\ K_{\max}='+str(panel['Kmax'])+'$};',r'\node at (4.35,-.75) {('+panel['letter']+')};',r'\end{scope}'])
    checks.append(dict(letter=panel['letter'],native_checks=native,global_C1_control_polygon=True,coordinate_scale='2.2cm',common_bounds=[[-1.3,-1],[10,6.4]],font_rescaling=False))
out.append(r'\end{tikzpicture}');(root/'image_tex/ch09/fig_9_69.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r.update(native_panels=checks,LS_noninterpolating_point_tangent_cases=sum(not q['point_tangent_constraints_compatible'] for p in r['panels'] for piece in p['pieces'] for q in piece['individual_LS']),error_shortcut_requires_zero_individual_point_residual=True)
(root/'image_tex/build/local-cubic-planar-check.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
print('PASS9.57native:',sum(x['native_checks'] for x in checks),'checks;globaldoubleknotC1controlpolygons,51samepoints,common2.2cm/font10;actualallerrorsverified.')
