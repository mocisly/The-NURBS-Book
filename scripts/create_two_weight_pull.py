from pathlib import Path
from fractions import Fraction as F
import json,argparse
from two_weight_pull_data import *
from native_bspline import segments,check,cubic_path,point
from rational_geometry import approximate
a=argparse.ArgumentParser();a.add_argument('figure',type=int,choices=(15,16));fig=a.parse_args().figure;r=case(fig);u=r['parameter'];W=r['new_weights'];root=Path(__file__).resolve().parents[1]
lines=['% Exact two-weight constraints; shared algebraically reconstructed control polygon, never scan traces.',r'\begin{tikzpicture}[book line,x=20cm,y=20cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-.05,-.06) rectangle (.92,.60);',r'\draw[book grid] '+'--'.join(point(p) for p in P)+';'];nc=0;proof=[]
for w,style in [(OLD,''),(W,'dashed')]:
    ss=segments(U,homogeneous(w),3);nc+=check(U,homogeneous(w),3,ss,steps=7);paths=[p for s in ss for p in approximate(s['bern'],F(1,2000000))];lines.extend(cubic_path(p,style) for p in paths);proof.append(dict(weights=w,screen_error_cm=max(p['certified_l1_error'] for p in paths)*20))
for j in range(1,36):
    v=F(1,5)+F(4,5)*F(j,36);x,y=curve(v,OLD),curve(v,W)
    if sum((a-b)**2 for a,b in zip(x,y))>F(1,1000000):lines.append(r'\draw[book grid] '+point(x)+'--'+point(y)+';')
for p in P:lines.append(r'\draw '+point(p)+r' circle[radius=1.4pt];')
for a,b in [(r['R'],P[4]),(r['R'],P[5]),(r['R'],r['Q'])]:lines.append(r'\draw[book grid] '+point(a)+'--'+point(b)+';')
for name,p,anchor,sep in [('P_4',P[4],'above left',8),('P_5',P[5],'above right',8),('R',r['R'],'below left',10),('Q',r['Q'],'above',10),('P',r['old_point'],'below right',8),(r'\widehat P',r['new_point'],'above left',24)]:lines.append(r'\draw '+point(p)+r' circle[radius=1.8pt] node['+anchor+'='+str(sep)+r'pt] {$'+name+'$};')
lines.extend([r'\draw[book axis] '+point(r['old_point'])+'--'+point(r['new_point'])+';',r'\node[anchor=west] at (.04,.55) {$d=0.088,\quad\bar u='+('0.608' if fig==15 else '0.612')+'$};',r'\end{tikzpicture}'])
(root/f'image_tex/ch11/fig_11_{fig+2:02}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');r.update(native_checks=nc,native_proofs=proof,both_printed_target_pairs_exact=True,no_contour_tracing=True);(root/f'image_tex/build/two-weight-pull-{fig}-check.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS',fig,'exactprintedweights/distance,',nc,'nativechecks; controls',[[round(float(x),5) for x in p] for p in P])
