"""10.1: actual6controlprofile and11controltrajectory,shared withfuture10.2."""
from pathlib import Path
from fractions import Fraction as F
import json
from swung_surface_example_data import P,T,U,V,ALPHA,WP,WT
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_01.tex')['applied']
assert len(P)==6 and len(T)==11 and all(p[1]==0 for p in P) and all(t[2]==0 for t in T)
def view(p):
    x,y,z=p;return(F(3,2)*(-F(4,5)*x+F(9,10)*y),F(3,2)*(-F(2,5)*x-F(7,20)*y+z))
out=['% Explicit representative6profile/11trajectorycontrols,shared unchanged with10.2;clampedcubic curves.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-9.5,-6.6) rectangle (11.5,10.5);'];checks=[]
for points,K,prefix,anchors in [(P,U,'P',('below right','above right','above right','below left','above left','above right')),(T,V,'T',('above left','below','above','right','left','below','right','left','above','below right','above right'))]:
    ss=segments(K,points,3);checks.append(check(K,points,3,ss))
    out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(p)) for p in points)+';')
    out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern']))) for s in ss)
    for i,(p,anchor) in enumerate(zip(points,anchors)):
        out.extend([r'\fill '+point(view(p))+r' circle[radius=1.4pt];',r'\node['+anchor+r'=5pt] at '+point(view(p))+r' {$\mathbf '+prefix+'_'+str(i)+'$};'])
for end,name,anchor in [((F(6),0,0),'x','below left'),((0,F(7),0),'y','right'),((0,0,F(6)),'z','above')]:
    out.append(r'\draw[book grid,book axis] (0,0)--'+point(view(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
out.extend([r'\node (profile) at (-6.4,4.7) {$\mathbf P(u)$};',r'\draw[book grid,shorten >=4pt] (profile)--'+point(view(de_boor(U,P,3,F(3,4))))+';',r'\node (trajectory) at (1,-5.9) {$\mathbf T(v)$};',r'\draw[book grid,shorten >=4pt] (trajectory)--'+point(view(de_boor(V,T,3,F(11,20))))+';',r'\end{tikzpicture}'])
(root/'image_tex/ch10/fig_10_01.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report=dict(figure='10.1',representative_controls=True,profile_controls=[list(map(str,p)) for p in P],trajectory_controls=[list(map(str,p)) for p in T],profile_knots=list(map(str,U)),trajectory_knots=list(map(str,V)),degrees=[3,3],all_profile_y_zero=True,all_trajectory_z_zero=True,native_curve_checks=checks,shared_unchanged_data_for='10.2',future_swung_alpha=str(ALPHA),future_profile_weights=list(map(str,WP)),future_trajectory_weights=list(map(str,WT)),camera_scale='1.5',font_rescaling=False)
(root/'image_tex/build/swung-profile-trajectory-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS10.1:6profilecontrols inxz/11trajectorycontrols inxy,clampedcubics;',sum(checks),'nativechecks;shared10.2data andprintedweightindices.')
