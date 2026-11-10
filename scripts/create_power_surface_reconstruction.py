"""6.21: exact nine-patch global power inversion and tensor knot removal."""
from pathlib import Path
from fractions import Fraction as F
import json
from tensor_power_conversion import matrix,affine_matrix,convert
from surface_geometry import surface,verify_tensor,isocurve
from native_bspline import segments,check,cubic_path,point
from inverse_knot_projection import solve,remove_to
from knot59_data import insert_surface
from surface_refinement import verify_directional_identity
from bspline_math import derivative,evaluate

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for name in ('fig_6_28.tex','fig_6_29.tex'):
    assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch06/'+name)['applied']
U=(F(0),)*4+(F(1,3),F(2,3))+(F(1),)*4
V=(F(0),)*3+(F(1,3),F(2,3))+(F(1),)*3
xs=tuple(map(F,(3,F(9,5),0,-F(9,5),-3)));ys=tuple(map(F,(-F(5,2),-F(17,10),-F(3,5),F(3,5),F(17,10),F(5,2))))
zu=tuple(map(F,(1,1,F(1,5),-F(3,5),-1,-1)));zv=tuple(map(F,(0,0,F(9,5),2,2)))
P=tuple(tuple((x,y,zu[i]+zv[j]+x*y/50) for j,x in enumerate(xs)) for i,y in enumerate(ys));base=(U,V,3,2,P)
tensorchecks=verify_tensor(*base,steps=10)
def inverse(M):return solve(M,tuple(tuple(F(i==j) for j in range(len(M))) for i in range(len(M))))
def multiply(A,B):return tuple(tuple(sum(x*y for x,y in zip(row,col)) for col in zip(*B)) for row in A)
recovered={};patchproof=[]
for i in range(3):
    for j in range(3):
        Q,A,B=convert(*base,3+i,2+j)
        Lu=multiply(inverse(matrix(3)),inverse(affine_matrix(3,*U[3+i:5+i])))
        Lv=multiply(inverse(matrix(2)),inverse(affine_matrix(2,*V[2+j:4+j])))
        Qback=tuple(tuple(tuple(sum(Lu[a][k]*Lv[b][l]*B[k][l][d] for k in range(4) for l in range(3)) for d in range(3)) for b in range(3)) for a in range(4))
        assert Qback==Q
        recovered[i,j]=Qback
        patchproof.append({'index':[i,j],'global_power':[[list(map(str,t)) for t in row] for row in B],'inverse_conversion_exact':True})
# Assemble exactly overlapping C0 boundary controls: 10x7, not 9 unrelated nets.
BP=[[None for _ in range(7)] for _ in range(10)]
for (i,j),Q in recovered.items():
    for a in range(4):
        for b in range(3):
            old=BP[3*i+a][2*j+b];assert old is None or old==Q[a][b]
            BP[3*i+a][2*j+b]=Q[a][b]
BP=tuple(tuple(row) for row in BP)
BU=(F(0),)*4+(F(1,3),)*3+(F(2,3),)*3+(F(1),)*4
BV=(F(0),)*3+(F(1,3),)*2+(F(2,3),)*2+(F(1),)*3
bezier=(BU,BV,3,2,BP)
refined=base;insertion=[]
for axis,ts in [('u',(F(1,3),F(1,3),F(2,3),F(2,3))),('v',(F(1,3),F(2,3)))]:
    for t in ts:
        new=insert_surface(*refined,axis,t);insertion.append(verify_directional_identity(refined,new,axis));refined=new
assert refined==bezier
columns=[];removals=[]
for j in range(7):
    K,C,proof=remove_to(BU,tuple(row[j] for row in BP),3,(F(1,3),F(1,3),F(2,3),F(2,3)))
    assert K==U and proof['curve_exactly_unchanged'];columns.append(C);removals.append(proof)
UP=tuple(tuple(col[i] for col in columns) for i in range(6));final=[]
for row in UP:
    K,C,proof=remove_to(BV,row,2,(F(1,3),F(2,3)))
    assert K==V and proof['curve_exactly_unchanged'];final.append(C);removals.append(proof)
assert tuple(final)==P
minimality=[]
for axis,t in [('u',F(1,3)),('u',F(2,3)),('v',F(1,3)),('v',F(2,3))]:
    K,p,C=isocurve(*base,axis,F(1,2));ss=segments(K,C,p)
    left=next(s for s in ss if s['b']==t);right=next(s for s in ss if s['a']==t)
    differences=[]
    for order in range(p+1):
        a,b=left['power'],right['power']
        for _ in range(order):a=tuple(derivative(c) for c in a);b=tuple(derivative(c) for c in b)
        differences.append(tuple(evaluate(c,t)-evaluate(d,t) for c,d in zip(a,b)))
    assert all(all(x==0 for x in row) for row in differences[:-1]) and any(differences[-1])
    minimality.append({'axis':axis,'knot':str(t),'first_nonzero_derivative_jump_order':p,'jump':list(map(str,differences[-1]))})
for i in range(11):
    for j in range(11):assert surface(*base,F(i,10),F(j,10))==surface(*bezier,F(i,10),F(j,10))

def panel(mode,shift=0):
    lines=[r'\begin{scope}[xshift='+str(shift)+r'cm]',
           r'\path[use as bounding box] (-6.3,-5.8) rectangle (6.6,8.9);',
           r'\begin{scope}[x={(-.81cm,-.54cm)},y={(.9cm,-.315cm)},z={(0cm,1.5cm)}]']
    if mode!='a':
        points=BP if mode=='b' else P
        for row in points:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
        for col in zip(*points):lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,col))+';')
        for row in points:
            for pt in row:lines.append(r'\fill '+point(pt)+r' circle[radius=1.2pt];')
    nativechecks=0
    for axis in ('u','v'):
        for t in (F(0),F(1,3),F(2,3),F(1)):
            K,d,C=isocurve(*base,axis,t);ss=segments(K,C,d);nativechecks+=check(K,C,d,ss)
            lines.extend(cubic_path(s) for s in ss)
    lines += [r'\draw[book axis] (0,0,0)--(6,0,0) node[below left=4pt] {$x$};',
              r'\draw[book axis] (0,0,0)--(0,5.8,0) node[right=4pt] {$y$};',
              r'\draw[book axis] (0,0,0)--(0,0,5.5) node[above=4pt] {$z$};',
              r'\end{scope}',r'\node at (0,-5.3) {('+mode+')};',r'\end{scope}']
    return lines,nativechecks
header=['% Explicit representative9-patch p3q2 surface; original has no numerical controls.',
        '% Invert GLOBAL tensor power coefficients; assemble shared Bezier boundaries; exact tensor removal.',r'\begin{tikzpicture}[book line]']
a,ca=panel('a');b,cb=panel('b');c,cc=panel('c',13.5)
(root/'image_tex/ch06/fig_6_28.tex').write_text('\n'.join(header+a+[r'\end{tikzpicture}'])+'\n',encoding='utf-8')
(root/'image_tex/ch06/fig_6_29.tex').write_text('\n'.join(header+b+c+[r'\end{tikzpicture}'])+'\n',encoding='utf-8')
(root/'image_tex/build/power-surface-reconstruction-check.json').write_text(json.dumps({'figure':'6.21','representative_controls':[[list(map(str,t)) for t in row] for row in P],'knots':[list(map(str,U)),list(map(str,V))],'nine_global_power_inverse_proofs':patchproof,'assembled_Bezier_net_shape':[10,7],'final_net_shape':[6,5],'independent_tensor_insertion_proofs':insertion,'exact_inverse_knot_removal_proofs':removals,'minimality_certificates':minimality,'native_curve_checks':ca+cb+cc,'exact_tensor_checks':tensorchecks,'exact_geometry_comparisons':121},indent=2)+'\n')
print(f'PASS:9 exact inverse tensor conversions;70 Bezier controls ->30 minimal controls with zero error;{ca+cb+cc} native curve checks and121 geometry comparisons.')
