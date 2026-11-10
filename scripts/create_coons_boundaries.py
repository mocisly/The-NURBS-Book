from pathlib import Path
from fractions import Fraction as F
import json
from coons_patch_data import U,V,C0U,C1U,C0V,C1V,CORNERS,view,construct
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];out=['% Exact compatible cubic/quadratic Coons boundaries; representative controls in scripts/coons_patch_data.py.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-9,-7) rectangle (9,8);'];checks=0
for K,C,p,label,anchor in [(U,C0U,3,'C_0(u)','above left'),(U,C1U,3,'C_1(u)','below right'),(V,C0V,2,'C_0(v)','above right'),(V,C1V,2,'C_1(v)','below left')]:
    ss=segments(K,C,p);checks+=check(K,C,p,ss,steps=7)
    out.extend(cubic_path(dict(bern=tuple(view(a) for a in s['bern']))) for s in ss)
    pos=view(de_boor(K,C,p,F(1,2)));out.append(r'\node['+anchor+r'=6pt] at '+point(pos)+r' {$'+label+'$};')
for row in CORNERS:
    for a in row:out.append(r'\fill '+point(view(a))+r' circle[radius=1.4pt];')
pos=view(CORNERS[1][0]);out.extend([r'\draw '+point(pos)+r' circle[radius=2.8pt];',r'\node[below=6pt] at '+point(pos)+r' {$S_{1,0}$};'])
origin=(-F(15,2),-F(11,2))
for end,name,anchor in [((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:
    to=tuple(a+b for a,b in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(to)+r' node['+anchor+r'=4pt] {$'+name+'$};')
out.append(r'\end{tikzpicture}');(root/'image_tex/ch10/fig_10_32.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
r=dict(representative_data=True,source='scripts/coons_patch_data.py',all_corner_compatibility_identities=4,whole_boundary_control_identities=22,native_curve_checks=checks,no_contour_tracing=True,nets=construct())
(root/'image_tex/build/coons-patch-data.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS10.24:',checks,'nativecurvechecks/4exactcorners/22wholeboundarycontrolidentities.')
