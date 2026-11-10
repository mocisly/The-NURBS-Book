"""Create ONE reviewed-in-order tolerance comparison of the Fig5.30 surface."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json
from knot530_data import BASE,P,CAMERA
from surface_tolerance_experiment import prepared_examples
from native_sparse_surface import sparse
from native_bspline import point

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('figure',type=int,choices=range(531,535));a=parser.parse_args()
index=a.figure-531;number=43+index;root=Path(__file__).resolve().parents[1]
target=root/f'image_tex/ch05/fig_5_{number}.tex';assert not target.exists()
net,proof=prepared_examples()[index];Q=net[-1]
for R in (P,Q):
    for row in R:
        for x,y,z in row:
            sx=-F(3,4)*x+F(17,20)*y;sy=-F(3,4)*x-F(3,10)*y+F(7,10)*z
            assert F(-28,5)<=sx<=F(32,5) and F(-26,5)<=sy<=F(73,10)

def net_lines(R,style,markers):
    lines=[]
    for row in R:lines.append(r'\draw['+style+'] '+'--'.join(map(point,row))+';')
    for j in range(len(R[0])):lines.append(r'\draw['+style+'] '+'--'.join(point(row[j]) for row in R)+';')
    if markers:
        for row in R:
            for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius=1pt];')
    return lines

panels=[];curve_reports={}
for panel in (0,1):
    lines=[r'\begin{scope}['+CAMERA+']']
    if panel==0:lines+=net_lines(P,'book grid,dashed',False)+net_lines(Q,'book line',True)
    else:
        old,r=sparse(BASE,'book grid,dashed');lines+=old;curve_reports['original']=r
        new,r=sparse(net,'book line');lines+=new;curve_reports['approximation']=r
    lines += [r'\draw[book axis] (0,0,0)--(5.5,0,0) node[below left=4pt] {$x$};',
              r'\draw[book axis] (0,0,0)--(0,6.2,0) node[right=4pt] {$y$};',
              r'\draw[book axis] (0,0,0)--(0,0,9.5) node[above=4pt] {$z$};',
              r'\end{scope}',r'\node at (.3,-4.65) {('+chr(97+panel)+')};'];panels.append(lines)
lines=['% Fig5.'+str(a.figure-500)+': SAME original data as5.30; independent whole-surface tolerance '+proof['tolerance']+'.',
       '% Native approximate net and actual sparse original/new isocurves; mathematical coefficients only.',
       '% Whole original-surface error verified in common tensor basis, not accumulated per-step budgets.',
       '% Same camera, physical scale and isoparametric values as5.30; font10pt remains unscaled.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-5.6,-5.2) rectangle (19.4,7.3);']
for panel,shift in zip(panels,(0,13)):lines+=[r'\begin{scope}[xshift='+str(shift)+'cm]']+panel+[r'\end{scope}']
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/f'image_tex/build/surface-tolerance-{a.figure}-check.json').write_text(json.dumps({
    'figure':'5.'+str(a.figure-500),'same_original_as530':True,'original_control_count':[9,8],
    'new_control_count':[len(Q),len(Q[0])],'U':list(map(str,net[0])),'V':list(map(str,net[1])),
    'controls':[[list(map(str,t)) for t in row] for row in Q],
    'whole_original_surface_error_proof':proof,'native_sparse_curve_proofs':curve_reports},indent=2)+'\n')
print('PASS:'+str(a.figure)+', actual'+str((len(Q),len(Q[0])))+' net, whole-surface bound='+
      str(float(F(proof['certified_common_tensor_basis_L1_bound_cm'])))+' <= '+str(float(F(proof['tolerance'])))+
      '; exact native curve checks='+str(sum(r['exact_native_isocurve_checks'] for r in curve_reports.values())))
