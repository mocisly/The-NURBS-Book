"""6.20: exact global power -> Bezier -> minimal cubic spline, no image fitting."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
from native_bspline import segments,check,cubic_path,point,number,de_boor
from bspline_math import compose_affine,derivative,evaluate
from knot51_data import insert
from inverse_knot_projection import solve,remove_to

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for name in ('fig_6_26.tex','fig_6_27.tex'):
    assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch06/'+name)['applied']
U=(F(0),)*4+(F(3,10),F(3,5),F(3,5))+(F(1),)*4
Q=tuple(tuple(map(F,p)) for p in [(0,0),(3,F(1,5)),(F(7,5),F(7,2)),(F(26,5),F(43,10)),(F(32,5),F(14,5)),(F(24,5),F(3,10)),(9,0)])
original=segments(U,Q,3);checks=check(U,Q,3,original)
M=tuple(tuple(F((-1)**(i-j)*comb(3,j)*comb(3-j,i-j)) if i>=j else F(0) for j in range(4)) for i in range(4))
pieces=[];controls=[]
for seg in original:
    # Input is the explicit global power coefficients. First apply R^-1,
    # then solve M*B=local_power, independently of native Bezier extraction.
    local=tuple(compose_affine(c,seg['a'],seg['b']-seg['a']) for c in seg['power'])
    B=solve(M,tuple(tuple(local[d][i] if i<len(local[d]) else F(0) for d in range(2)) for i in range(4)))
    assert B==seg['bern']
    controls.extend(B if not controls else B[1:])
    pieces.append({'interval':list(map(str,(seg['a'],seg['b']))),'global_power':[[str(x) for x in c] for c in seg['power']],'recovered_Bezier':[[str(x) for x in pt] for pt in B]})
K=(F(0),)*4+(F(3,10),)*3+(F(3,5),)*3+(F(1),)*4;P=tuple(controls)
bez=segments(K,P,3);checks+=check(K,P,3,bez)
R,V,proof=remove_to(K,P,3,(F(3,10),F(3,10),F(3,5)))
assert R==U and V==Q and proof['curve_exactly_unchanged']
W,T=U,Q
for t in (F(3,10),F(3,10),F(3,5)):W,T,_=insert(W,T,3,t)
assert W==K and T==P
continuity=[]
for a,b,order in zip(original,original[1:],(2,1)):
    knot=a['b'];differences=[]
    for k in range(4):
        left=list(a['power']);right=list(b['power'])
        for _ in range(k):left=[derivative(c) for c in left];right=[derivative(c) for c in right]
        differences.append(tuple(evaluate(x,knot)-evaluate(y,knot) for x,y in zip(left,right)))
    assert all(all(v==0 for v in d) for d in differences[:order+1])
    assert any(differences[order+1])
    continuity.append({'knot':str(knot),'exact_continuity':order,'next_derivative_jump':list(map(str,differences[order+1]))})
for i in range(101):assert de_boor(U,Q,3,F(i,100))==de_boor(K,P,3,F(i,100))

def panel(mode,shift=0):
    lines=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-1.1,-3.2) rectangle (10.1,5.2);']
    pts=P if mode=='b' else Q
    if mode!='a':
        lines.append(r'\draw[book grid] '+'--'.join(map(point,pts))+';')
    lines.extend(cubic_path(s) for s in original)
    if mode!='a':
        anchors=(['below left','below right','left','left','above left','above','right','right','below left','below right'] if mode=='b' else
                 ['below left','below right','above left','above','right','below left','below right'])
        for i,(pt,anchor) in enumerate(zip(pts,anchors)):
            lines.append(r'\draw '+point(pt)+r' circle[radius=1.7pt] node['+anchor+r'=6pt] {$\mathbf '+('P' if mode=='b' else 'Q')+'_'+str(i)+'$};')
    for t in (F(0),F(3,10),F(3,5),F(1)):
        lines.append(r'\node[rectangle,draw,line width=.35pt,inner sep=1.8pt] at '+point(de_boor(U,Q,3,t))+' {};')
    lines.append(r'\draw[book grid] (0,-1.4)--(9,-1.4);')
    labels=([r's_0',r's_1',r's_2',r's_3'] if mode=='a' else
            [r'u_0\!\! -\!\! u_3',r'u_4\!\! -\!\! u_6',r'u_7\!\! -\!\! u_9',r'u_{10}\!\! -\!\! u_{13}'] if mode=='b' else
            [r'u_0\!\! -\!\! u_3',r'u_4',r'u_5,u_6',r'u_7\!\! -\!\! u_{10}'])
    mults=[1,1,1,1] if mode=='a' else [4,3,3,4] if mode=='b' else [4,1,2,4]
    for t,label,m in zip((F(0),F(3,10),F(3,5),F(1)),labels,mults):
        x=9*t
        for j in range(m):
            xx=x+F(7,100)*(F(j)-F(m-1,2))
            lines.append(r'\draw[book grid] '+point((xx,-F(31,20)))+'--'+point((xx,-F(5,4)))+';')
        lines.append(r'\node[below=5pt] at '+point((x,-F(31,20)))+' {$'+label+'$};')
    lines += [r'\node at (4.5,-2.8) {('+mode+')};',r'\end{scope}']
    return lines
header=['% Explicit representative cubic; input is global piecewise power coefficients.',
        '% Exact inverse M/R conversion, common-basis knot removal, and minimal continuity verified.',r'\begin{tikzpicture}[book line]']
(root/'image_tex/ch06/fig_6_26.tex').write_text('\n'.join(header+panel('a')+[r'\end{tikzpicture}'])+'\n',encoding='utf-8')
(root/'image_tex/ch06/fig_6_27.tex').write_text('\n'.join(header+panel('b')+panel('c',12.2)+[r'\end{tikzpicture}'])+'\n',encoding='utf-8')
(root/'image_tex/build/power-curve-reconstruction-check.json').write_text(json.dumps({'figure':'6.20','representative_minimal_controls':[[str(x) for x in pt] for pt in Q],'minimal_knots':list(map(str,U)),'Bezier_knots':list(map(str,K)),'input_power_pieces_and_inverse_conversion':pieces,'removal_proof':proof,'minimality_by_nonzero_derivative_jumps':continuity,'native_checks':checks,'exact_deBoor_equalities':101},indent=2)+'\n')
print(f'PASS:{checks} native checks;101 exact geometry equalities; M/R inversion and exact knot removal recover seven controls; continuity exactly C2/C1.')
