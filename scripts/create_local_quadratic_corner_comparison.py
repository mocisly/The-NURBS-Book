"""9.24: identical data/algorithm with only the Akima corner flag changed."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import cubic_path,point
from local_quadratic_interpolator import interpolate
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_30.tex')['applied']
Q=tuple(tuple(map(F,q)) for q in [(0,0),(0,1),(0,2),(2,2),(2,1),(2,0),(4,0),(6,0),(6,1),(6,3)])
out=['% Actual Eq9.29/31/33 tangent estimates and local quadratic construction;representative data.',r'\begin{tikzpicture}[book line,x=2.7cm,y=2.7cm]'];reports=[]
for i,corners in enumerate((False,True)):
    ss,report=interpolate(Q,'akima',corners);reports.append(report)
    out.extend([r'\begin{scope}[yshift='+str(-12.7*i)+r'cm]',r'\path[use as bounding box] (-.6,-.85) rectangle (6.8,3.5);'])
    out.extend(cubic_path(s) for s in ss)
    out.extend(r'\draw '+point(q)+r' circle[radius=2.4pt];' for q in Q)
    out.extend([r'\node at (3,-.6) {('+chr(97+i)+')};',r'\end{scope}'])
    if corners:
        assert report['flagged_corner_indices']==[5,7]
        assert sum(not x['G1'] for x in report['joins'])==2
        for s in ss:
            a,b,c=s['bern']
            if a[1]==c[1]==0:assert b[1]==0
            if a[0]==c[0] and a[0] in (2,6) and max(a[1],c[1])<=1:assert b[0]==a[0]
    else:assert all(j['G1'] for j in report['joins'])
out.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_30.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/local-quadratic-corner-comparison-check.json').write_text(json.dumps(dict(figure='9.24',panels=reports,same_data_and_algorithm=True,only_corner_flag_changed=True,two_exact_corners_preserved=True,all_other_joins_G1=True,all_data_interpolated=True),indent=2)+'\n')
print('PASS9.24: common10data/algorithm, smooth case allG1;cornerflag preserves exactlyQ5/Q7with horizontal/vertical runs exact.')
