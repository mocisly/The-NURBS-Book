"""Fig5.41: explicit quintic sixteen-point S curve and quartic approximation."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point
from native_polynomial_drawing import paths
from degree_elevation_geometry import elevate_spline
from spline_degree_reduction import reduce_spline

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_62.tex';assert not target.exists()
W=(F(0),)*5+tuple(F(t) for t in ('.15','.3','.5','.7','.85'))+(F(1),)*5
R=tuple(tuple(F(str(t)) for t in pt) for pt in [(3,0),(1.2,0),(-.4,3.2),(1.7,6.8),(4.2,5.6),(5.2,1.6),(7.8,.4),(10.2,3.6),(8.8,6.8),(6.8,6.8)])
U,P,elevation=elevate_spline(W,R,4,1);P=list(P)
for i,d in [(5,(F(0),F('.12'))),(10,(F('-.1'),F('-.08')))]:P[i]=tuple(x+y for x,y in zip(P[i],d))
P=tuple(P)
assert U==(F(0),)*6+tuple(F(t) for t in ('.15','.15','.3','.3','.5','.5','.7','.7','.85','.85'))+(F(1),)*6
K,Q,proof=reduce_spline(U,P,5);assert len(P)==16 and len(Q)==10 and K==W
nativechecks=0;drawing=[];certificates=[]
for knots,controls,degree,style in [(U,P,5,'book line'),(K,Q,4,'book line,dashed')]:
    ss=segments(knots,controls,degree);nativechecks+=check(knots,controls,degree,ss)
    commands,certificate=paths(ss,style);drawing+=commands;certificates.append(certificate)
lines=['% Representative perturbed elevated-quartic S curve; printed quintic knots exact.',
       '% Reduction5.41/5.42 and rational inverse-insertion assembly; whole error verified.',
       r'\begin{tikzpicture}[book line,x=1.5cm,y=1.5cm]',r'\path[use as bounding box] (-1,-.7) rectangle (11,7.7);',
       r'\draw[book grid] '+'--'.join(map(point,P))+';',
       r'\draw[book grid,dashed] '+'--'.join(map(point,Q))+';']+drawing
for pt in P:lines.append(r'\draw '+point(pt)+r' circle[radius=1.8pt];')
for pt in Q:lines.append(r'\node[rectangle,draw,inner sep=1.5pt] at '+point(pt)+' {};')
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/spline-degree-reduction-check.json').write_text(json.dumps({
    'figure':'5.41','printed_original_knots':list(map(str,U)),'final_knots':list(map(str,K)),
    'original_controls':[[str(t) for t in pt] for pt in P],'approximation_controls':[[str(t) for t in pt] for pt in Q],
    'representative_construction':'quartic elevated exactly, then two small control perturbations',
    'root_quartic_controls':[[str(t) for t in pt] for pt in R],
    'original_elevation_proof':elevation,'reduction_proof':proof,
    'native_checks':nativechecks,'native_render_certificates':certificates,
    'coordinate_unit_display_scale':1.5},indent=2)+'\n')
print(f'PASS:{nativechecks} native checks,246 exact whole-error identities;16 quintic ->10 quartic controls, certified L1 bound={float(F(proof["certified_whole_curve_L1_error_bound"]))}.')
