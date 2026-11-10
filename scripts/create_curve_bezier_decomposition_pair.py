"""Fig5.18/5.19: common exact cubic, control polygons and equation-based bases."""
from pathlib import Path
from fractions import Fraction as F
import json,argparse
from native_bspline import segments,check,cubic_path,point,de_boor
from surface_geometry import extraction,weights
from rational_geometry import evaluate
from knot518_data import U,P,decomposed

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--decomposed',action='store_true');args=parser.parse_args()
figure='5.19' if args.decomposed else '5.18';source=23 if args.decomposed else 22
root=Path(__file__).resolve().parents[1];target=root/f'image_tex/ch05/fig_5_{source}.tex';assert not target.exists()
K,R=decomposed() if args.decomposed else (U,P);n=len(R);old=segments(U,P,3);ss=segments(K,R,3);curvechecks=check(K,R,3,ss)
for s in ss:
    original=next(t for t in old if t['a']<=s['a'] and s['b']<=t['b']);assert s['power']==original['power']
if args.decomposed:
    expected=old[0]['bern']+tuple(pt for s in old[1:] for pt in s['bern'][1:]);assert R==expected and len(R)==13
for j in range(201):assert de_boor(K,R,3,F(j,50))==de_boor(U,P,3,F(j,50))
unit=tuple(tuple(F(i==j) for j in range(n)) for i in range(n))
for j in range(101):
    u=F(j,25);rr=weights(K,3,u);assert min(rr)>=0 and sum(rr)==1 and tuple(rr)==de_boor(K,unit,3,u)
lines=['% Fig'+figure+': exact SAME representative7-control cubic and original parameter domain[0,4].',
       '% Native cubic Bezier paths, editable basis graphs; no raster contours.',
       '% '+('Each original internal knot has multiplicity3,13 controls equal the four extracted Bezier nets.' if args.decomposed else 'Original U=(0,0,0,0,1,2,3,4,4,4,4), seven controls.'),
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',r'\path[use as bounding box] (-.8,-1.7) rectangle (12.1,13.1);',
       r'\begin{scope}[yshift=6.8cm]',r'\draw[book grid] '+'--'.join(map(point,R))+';']
for s in old:lines.append(cubic_path(s))
for pt in R:lines.append(r'\draw '+point(pt)+' circle[radius=1.6pt];')
lines += [r'\node at (5.25,-1) {(a)};',r'\end{scope}',r'\draw[book axis] (0,0)--(11.8,0) node[right=4pt] {$u$};',r'\draw[book axis] (0,0)--(0,4.2);',r'\draw[book grid] (-.08,3.2)--(.08,3.2) node[left=5pt] {$1$};']
graphs=graphchecks=0
for s in range(3,n):
    a,b=K[s:s+2]
    if a==b:continue
    B=extraction(K,3,s)
    for i in range(n):
        if not any(row[i] for row in B):continue
        controls=tuple((F(21,8)*(a+(b-a)*F(r,3)),F(16,5)*B[r][i]) for r in range(4))
        for j in range(11):
            t=F(j,10);u=a+(b-a)*t;assert evaluate(controls,t)==(F(21,8)*u,F(16,5)*weights(K,3,u)[i]);graphchecks+=1
        lines.append(cubic_path({'bern':controls}));graphs+=1
for u in range(5):
    m=K.count(F(u))
    for j in range(m):
        x=F(21,8)*u+F(3,50)*(F(j)-F(m-1,2));lines.append(r'\draw[book grid] '+point((x,F(-2,25)))+'--'+point((x,F(2,25)))+';')
    lines.append(r'\node[below=5pt] at '+point((F(21,8)*u,F(0)))+' {$'+str(u)+'$};')
lines += [r'\node at (5.25,-1.3) {(b)};',r'\end{tikzpicture}'];target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/('image_tex/build/curve-bezier-decomposed-check.json' if args.decomposed else 'image_tex/build/curve-bezier-original-check.json')).write_text(json.dumps({'figure':figure,'degree':3,'representative_original_controls':[[str(c) for c in pt] for pt in P],'knots':list(map(str,K)),'controls':[[str(c) for c in pt] for pt in R],'native_curve_checks':curvechecks,'unchanged_polynomial_spans':len(ss),'curve_invariance_points':201,'basis_partition_vs_unit_control_deboor_points':101,'exact_native_basis_graph_points':graphchecks,'native_basis_graph_paths':graphs,'four_extracted_bezier_nets_equal_inserted_controls':args.decomposed},indent=2)+'\n')
print(f'PASS:{figure},{n} controls,{curvechecks} native curve checks,201 invariant curve points,101 independent partition/deBoor points,{graphchecks} exact graph checks.')
