"""9.3:real chord-length/averaged-knot interpolation and correctly positioned knot ruler."""
from pathlib import Path
from fractions import Fraction as F
import json
from global_interpolation_data import Q,LENGTHS,TOTAL,PARAMS,U,P
from native_bspline import segments,check,de_boor,cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_03.tex')['applied']
ss=segments(U,P,3);nc=check(U,P,3,ss)
assert all(de_boor(U,P,3,t)==q for t,q in zip(PARAMS,Q))
assert all(U[i]<PARAMS[i]<U[i+4] for i in range(1,6))
assert TOTAL==F(101,10) and U[4:7]==(F(95,303),F(160,303),F(218,303))
lines=['% Representative seven-point data with EXACT Pythagorean chord lengths;shared with9.4.',
       '% Seven controls are solved,not placed by eye;all datum parameters and averaged knots exact.',
       r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-1.1,-2.3) rectangle (8.2,3.9);',
       r'\draw[book grid,dashed] '+'--'.join(point(p) for p in P)+';']
lines.extend(cubic_path(s) for s in ss)
for i,(p,anchor) in enumerate(zip(P,['below left','left','above','above','below right','above','above right'])):
    lines.append(r'\node['+anchor+r'=7pt] at '+point(p)+r' {$\mathbf P_'+str(i)+'$};')
for i,(q,anchor) in enumerate(zip(Q,['below right','right','below right','below left','above left','below right','below right'])):
    lines.extend([r'\draw '+point(q)+r' circle[radius=2.4pt];',r'\node['+anchor+r'=8pt] at '+point(q)+r' {$\mathbf Q_'+str(i)+'$};'])
level=-F(17,10);length=F(36,5)
lines.append(r'\draw[book grid] (-.2,-1.7)--(7.4,-1.7);')
for t in U[4:7]:lines.append(r'\draw[book grid] '+point((length*t,level-F(3,25)))+'--'+point((length*t,level+F(3,25)))+';')
for end in (F(0),F(1)):
    for offset in (-F(3,25),-F(3,50),F(3,50),F(3,25)):
        x=length*end+offset;lines.append(r'\draw[book grid] '+point((x,level-F(3,25)))+'--'+point((x,level+F(3,25)))+';')
for i,t in enumerate(PARAMS):
    pt=(length*t,level);lines.append(r'\draw '+point(pt)+r' circle[radius=2pt];')
    lines.append(r'\node[below=7pt] at '+point(pt)+r' {$\bar u_'+str(i)+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch09/fig_9_03.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/global-curve-interpolation-check.json').write_text(json.dumps({'figure':'9.3','representative_data_points':[[str(x) for x in q] for q in Q],'exact_chord_lengths':list(map(str,LENGTHS)),'total_chord_length':str(TOTAL),'exact_chord_parameters':list(map(str,PARAMS)),'averaged_knots':list(map(str,U)),'degree':3,'solved_controls':[[str(x) for x in p] for p in P],'all7interpolation_equations_exact':True,'interior_Schoenberg_Whitney_inequalities':True,'C2_native_piece_checks':nc,'ruler_coordinate_length':str(length),'repeated_endpoint_knot_ticks_slightly_separated_for_readability':True,'point_and_knot_ruler_positions_from_computed_values':True},indent=2)+'\n')
print('PASS:exact7point solve,chord lengths/parameters and3averaged knots,C2native cubic pieces;parameter circles and knot ticks computed from the same vectors.')
