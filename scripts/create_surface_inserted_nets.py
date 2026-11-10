"""Fig5.10: actual directional knot insertions, including the missing continuation(c)."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point
from surface_geometry import surface,verify_tensor
from knot59_data import U,V,P,insert_surface

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_11.tex';assert not target.exists()
base=(U,V,3,2,P);Au=insert_surface(*base,'u',F(2,5));Av=insert_surface(*base,'v',F(7,10))
Auv=insert_surface(*Au,'v',F(7,10));Avu=insert_surface(*Av,'u',F(2,5));assert Auv==Avu
curvechecks=identical=0
def verify_insertion(before,after,axis):
    global curvechecks,identical
    U,V,p,q,R=before;W,X,_,_,S=after
    pairs=[(U,W,p,tuple(row[j] for row in R),tuple(row[j] for row in S)) for j in range(len(R[0]))] if axis=='u' else [(V,X,q,a,b) for a,b in zip(R,S)]
    for K,L,d,A,B in pairs:
        old,new=segments(K,A,d),segments(L,B,d);curvechecks+=check(L,B,d,new)
        for s in new:
            t=next(t for t in old if t['a']<=s['a'] and s['b']<=t['b']);assert s['power']==t['power'];identical+=1
for before,after,axis in [(base,Au,'u'),(base,Av,'v'),(Au,Auv,'v'),(Av,Avu,'u')]:verify_insertion(before,after,axis)
lines=['% Fig5.10: SAME representative unit-weight surface as5.9; actual exact knot insertions.',
       '% (a)u=2/5,(b)v=7/10,(c)both. The original missing HTML continuation(c) is reconstructed from the stated operations.',
       '% All directional polynomial span coefficients unchanged; u/v insertion orders commute exactly.',
       '% Equal affine camera scale. Font and strokes unchanged; geometry displayed at0.8 of Fig5.9.',
       r'\begin{tikzpicture}[book line]',
       r'\path[use as bounding box] (canvas cs:x=-11.3cm,y=-17cm) rectangle (canvas cs:x=12cm,y=6.7cm);']
reports=[]
for index,(net,shift) in enumerate([(Au,(-6,0)),(Av,(6,0)),(Auv,(0,-12))]):
    W,X,p,q,R=net;n,m=len(R),len(R[0]);tensor=verify_tensor(W,X,p,q,R,10)
    for a in range(11):
        for b in range(11):assert surface(*net,F(a,10),F(b,10))==surface(*base,F(a,10),F(b,10))
    lines += [r'\begin{scope}[shift={'+point(shift)+'}]',
              r'\begin{scope}[x={(-.72cm,-.48cm)},y={(.8cm,-.28cm)},z={(0cm,.8cm)}]',
              r'\draw[book axis] (0,0,0)--(5,0,0) node[below left=4pt] {$x$};',
              r'\draw[book axis] (0,0,0)--(0,6,0) node[right=4pt] {$y$};',
              r'\draw[book axis] (0,0,0)--(0,0,7.1) node[above=4pt] {$z$};']
    for row in R:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
    for j in range(m):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(row[j]) for row in R)+';')
    for row in R:
        for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius=1.2pt];')
    for i,j,anchor in [(0,0,'above left'),(1,0,'below left'),(n-1,0,'below right'),(0,1,'above left'),(0,m-1,'above'),(n-1,m-1,'right')]:
        lines.append(r'\node['+anchor+'=5pt] at '+point(R[i][j])+r' {$\mathbf Q_{'+str(i)+','+str(j)+'}$};')
    parameter=[r'\bar u=\frac25',r'\bar v=\frac7{10}',r'\bar u=\frac25,\quad\bar v=\frac7{10}'][index]
    lines += [r'\end{scope}',r'\node at (.4,-4.25) {('+chr(97+index)+r')\quad $'+parameter+'$};',r'\end{scope}']
    reports.append({'panel':chr(97+index),'U':list(map(str,W)),'V':list(map(str,X)),'control_count':[n,m],'controls':[[list(map(str,p)) for p in row] for row in R],'tensor_vs_nested_deboor_points':tensor,'tensor_invariance_points':121})
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-inserted-nets-check.json').write_text(json.dumps({'figure':'5.10','same_original_controls_as5.9':True,'unit_weights':True,'exact_directional_curve_checks':curvechecks,'identical_directional_polynomial_spans':identical,'u_then_v_equals_v_then_u_control_nets':True,'panels':reports,'missing_continuation_c_reconstructed_from_stated_both_directions':True},indent=2)+'\n')
print(f'PASS:3 real inserted nets,363 invariant surface points,{curvechecks} directional checks,{identical} identical polynomial spans; insertion orders commute.')
