"""6.18: exact Bezier extraction, M3/R3 conversion and global power coefficient arrows."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from bspline_math import compose_affine,evaluate

root=Path(__file__).resolve().parents[1];data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/fig_6_23.tex')['applied']
def matrix(p):return tuple(tuple(F((-1)**(j-k)*comb(p,k)*comb(p-k,j-k)) if j>=k else F(0) for k in range(p+1)) for j in range(p+1))
for p in range(1,9):
    M=matrix(p)
    assert all(sum(row)==F(j==0) for j,row in enumerate(M))
    assert all(sum(M[j][k] for j in range(p+1))==F(k==p) for k in range(p+1))
    assert all(M[j][k]==M[p-k][p-j] for j in range(p+1) for k in range(p+1))
U=(F(0),)*4+(F(3,10),F(7,10))+(F(1),)*4
P=((-F(6),F(4)),(-F(3),F(4)),(-F(3),F(8)),(F(3),F(8)),(F(3),F(4)),(F(6),F(4)))
ss=segments(U,P,3);checks=check(U,P,3,ss);middle=ss[1];a,b=middle['a'],middle['b'];h=b-a
assert (a,b)==(F(3,10),F(7,10));B=middle['bern'];M=matrix(3)
A=tuple(tuple(sum(M[i][j]*B[j][d] for j in range(4)) for d in range(2)) for i in range(4))
offset,scale=-a/h,1/h
R=tuple(tuple(F(comb(j,i))*scale**i*offset**(j-i) if j>=i else F(0) for j in range(4)) for i in range(4))
coeff=tuple(tuple(sum(R[i][j]*A[j][d] for j in range(4)) for d in range(2)) for i in range(4))
assert tuple(tuple(coeff[i][d] for i in range(4)) for d in range(2))==middle['power']
for d in range(2):
    written=compose_affine(tuple(A[i][d] for i in range(4)),offset,scale)
    assert written+(F(0),)*(4-len(written))==middle['power'][d]
for i in range(101):
    u=a+h*F(i,100)
    assert tuple(sum(coeff[k][d]*u**k for k in range(4)) for d in range(2))==de_boor(U,P,3,u)
markers=[de_boor(U,P,3,a+h*F(i,20)) for i in range(21)]
tips=[tuple(x/10 for x in pt) for pt in coeff]
xlo=min(-F(7),*(x for x,y in tips))-F(4,5);xhi=max(F(7),*(x for x,y in tips))+F(4,5)
ylo=min(-F(1),*(y for x,y in tips))-F(4,5);yhi=max(F(9),*(y for x,y in tips))+F(4,5)
lines=['% Representative six-point cubic hat curve, U0quad,.3,.7,1quad; unit weights.',
       '% Middle Bezier controls extracted exactly, then b=R3*M3*B computed in global u.',
       '% Coefficient arrows display b_i/10, not endpoint derivatives or local-t coefficients.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] '+point((xlo,ylo))+' rectangle '+point((xhi,yhi))+';',
       r'\draw[book grid] '+'--'.join(map(point,P))+';']
lines.extend(cubic_path(s) for s in ss)
for pt in P:lines.append(r'\draw '+point(pt)+r' circle[radius=1.7pt];')
for pt in markers:lines.append(r'\node[rectangle,draw,line width=.35pt,inner sep=1.6pt] at '+point(pt)+' {};')
lines += [r'\draw[book axis] (0,0)--(6.8,0) node[right=4pt] {$x$};',
          r'\draw[book axis] (0,0)--(0,5.2) node[above=4pt] {$y$};']
anchors=['above right','above left','below right','below']
for i,(tip,anchor) in enumerate(zip(tips,anchors)):
    lines.append(r'\draw[book axis] (0,0)--'+point(tip)+r' node['+anchor+r'=6pt] {$\mathbf b_'+str(i)+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch06/fig_6_23.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/curve-power-conversion-check.json').write_text(json.dumps({
    'figure':'6.18','representative_controls':[[str(x) for x in pt] for pt in P],
    'knots':list(map(str,U)),'middle_interval':list(map(str,(a,b))),
    'extracted_Bezier_controls':[[str(x) for x in pt] for pt in B],
    'M3':[[str(x) for x in row] for row in M],'R3':[[str(x) for x in row] for row in R],
    'local_power_coefficients':[[str(x) for x in pt] for pt in A],
    'global_power_coefficients':[[str(x) for x in pt] for pt in coeff],
    'native_checks':checks,'exact_global_power_evaluation_checks':101,
    'matrix_row_column_sums_and_antidiagonal_symmetry_checked_degrees':list(range(1,9)),
    'display_coefficient_factor':'1/10'},indent=2)+'\n')
print(f'PASS:{checks} native checks,101 exact global power evaluations;M/R conversion identical to extracted spline polynomial.')
print('Global b_i/10:'+str([tuple(map(float,t)) for t in tips]))
