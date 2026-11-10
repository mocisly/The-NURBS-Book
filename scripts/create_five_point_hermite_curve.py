"""9.1:solve all five interpolation and both endpoint derivative constraints exactly."""
from pathlib import Path
from fractions import Fraction as F
import json
from inverse_knot_projection import solve
from surface_geometry import weights
from bspline_math import piece,derivative,evaluate
from native_bspline import segments,check,de_boor,cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_01.tex')['applied']
Q=tuple(tuple(map(F,p)) for p in [(0,0),(F(3,2),2),(F(7,2),3),(F(28,5),F(5,2)),(F(15,2),F(1,2))])
D0=(F(4),F(9));D4=(F(6),-F(9));U=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
rows=[tuple(weights(U,3,F(i,4))) for i in range(5)]
rows.extend(tuple(evaluate(derivative(piece(U,i,3,span)),u) for i in range(7)) for span,u in [(3,F(0)),(6,F(1))])
P=solve(tuple(rows),Q+(D0,D4));ss=segments(U,P,3);nc=check(U,P,3,ss)
assert all(de_boor(U,P,3,F(i,4))==q for i,q in enumerate(Q))
assert tuple(evaluate(derivative(c),F(0)) for c in ss[0]['power'])==D0
assert tuple(evaluate(derivative(c),F(1)) for c in ss[-1]['power'])==D4
dx=min(3*(s['bern'][i+1][0]-s['bern'][i][0])/(s['b']-s['a']) for s in ss for i in range(3));assert dx>0
lines=['% Exact representative9.1 Hermite interpolation:five given points andtwo actual endpoint derivatives.',
       '% Uniform point parametersi/4,p3,7controls;arrow vectors both scaled1/4,not independently normalized.',
       r'\begin{tikzpicture}[book line,x=2.2cm,y=2.2cm]',r'\path[use as bounding box] (-.8,-2.4) rectangle (10,3.8);']
lines.extend(cubic_path(s) for s in ss)
for q,D,name,anchor in [(Q[0],D0,'0','above left'),(Q[-1],D4,'4','below left')]:
    tip=tuple(x+y/4 for x,y in zip(q,D));lines.append(r'\draw[book axis] '+point(q)+'--'+point(tip)+r' node['+anchor+r'=7pt] {$\mathbf D_'+name+'$};')
for i,(q,anchor) in enumerate(zip(Q,['below right','below right','below right','below left','below left'])):
    lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
    lines.append(r'\node['+anchor+r'=7pt] at '+point(q)+r' {$\mathbf Q_'+str(i)+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch09/fig_9_01.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/five-point-hermite-curve-check.json').write_text(json.dumps({'figure':'9.1','representative_data_points':[[str(x) for x in q] for q in Q],'point_parameters':['0','1/4','1/2','3/4','1'],'degree':3,'knots':list(map(str,U)),'solved_controls':[[str(x) for x in p] for p in P],'exact_interpolation_constraints':5,'exact_endpoint_derivative_constraints':2,'endpoint_derivatives':[list(map(str,D0)),list(map(str,D4))],'linear_system_all7_rows_exactly_solved':True,'native_piece_checks':nc,'strictly_positive_dx_du_Bernstein_lower_bound':str(dx),'C2_internal_continuity_verified':True,'derivative_arrow_common_scale':'1/4','native_coordinate_scale_cm':'11/5'},indent=2)+'\n')
print('PASS:exact7x7Hermite solve,all5points and2endpoint derivatives;C2native cubic pieces,strictly positive x derivative and common1/4arrow scale.')
