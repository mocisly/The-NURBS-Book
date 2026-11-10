"""9.10:traditional C2spline solved by tridiagonal elimination vs ordinary interpolation."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
from global_interpolation_data import interpolate
from inverse_knot_projection import solve
from surface_geometry import weights
from bspline_math import piece,derivative,evaluate
from native_bspline import segments,check,de_boor,cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_10.tex')['applied']
Q=tuple(tuple(map(F,p)) for p in [('0','0'),('.4','1.4'),('3','2.1'),('3.7','.7'),('4.4','0'),('7.8','1.8'),('6.5','3.5')])
squares=tuple(sum((b-a)**2 for a,b in zip(A,B)) for A,B in zip(Q,Q[1:]));scale=10**12
lo=tuple(F(isqrt(x.numerator*scale**2//x.denominator),scale) for x in squares);hi=tuple(x+F(1,scale) for x in lo)
assert all(a*a<=s<b*b for a,b,s in zip(lo,hi,squares))
params=(F(0),)+tuple(sum(lo[:i])/sum(lo) for i in range(1,6))+(F(1),)
bounds=tuple((sum(lo[:i])/sum(hi),sum(hi[:i])/sum(lo)) for i in range(1,6))
assert all(a<=t<=b and b-a<F(1,10**11) for t,(a,b) in zip(params[1:-1],bounds))
alpha=sum(lo);D0=(F(0),alpha);Dn=(-alpha,F(0))
U=(F(0),)*4+params[1:-1]+(F(1),)*4
W=tuple(tuple(weights(U,3,t)) for t in params)
rows=W+tuple(tuple(evaluate(derivative(piece(U,i,3,span)),u) for i in range(9)) for span,u in [(3,F(0)),(8,F(1))])
P=solve(rows,Q+(D0,Dn))
fixed={0:Q[0],1:tuple(a+U[4]*b/3 for a,b in zip(Q[0],D0)),7:tuple(a-(1-U[8])*b/3 for a,b in zip(Q[-1],Dn)),8:Q[-1]}
A=tuple(tuple(W[k][i] for i in range(2,7)) for k in range(1,6))
B=tuple(tuple(Q[k][dim]-sum(W[k][i]*q[dim] for i,q in fixed.items()) for dim in range(2)) for k in range(1,6))
assert all(A[i][j]==0 for i in range(5) for j in range(5) if abs(i-j)>1)
diag=[A[i][i] for i in range(5)];rhs=list(B)
for i in range(1,5):
    factor=A[i][i-1]/diag[i-1];diag[i]-=factor*A[i-1][i]
    rhs[i]=tuple(a-factor*b for a,b in zip(rhs[i],rhs[i-1]))
X=[None]*5;X[-1]=tuple(a/diag[-1] for a in rhs[-1])
for i in range(3,-1,-1):X[i]=tuple((a-A[i][i+1]*b)/diag[i] for a,b in zip(rhs[i],X[i+1]))
assert tuple(X)==P[2:7] and all(P[i]==q for i,q in fixed.items())
ss=segments(U,P,3);nc=check(U,P,3,ss)
assert all(de_boor(U,P,3,t)==q for t,q in zip(params,Q))
assert tuple(evaluate(derivative(c),F(0)) for c in ss[0]['power'])==D0
assert tuple(evaluate(derivative(c),F(1)) for c in ss[-1]['power'])==Dn
V,R=interpolate(Q,params);rr=segments(V,R,3);rc=check(V,R,3,rr)
lines=['% Traditional tridiagonal spline compared to ordinary averaged-knot interpolation.',
       r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-.7,-1.1) rectangle (9,4.5);']
lines.extend(cubic_path(s) for s in ss);lines.extend(cubic_path(s,'dashed') for s in rr)
for q,D in [(Q[0],D0),(Q[-1],Dn)]:lines.append(r'\draw[book axis] '+point(q)+'--'+point(tuple(a+b/5 for a,b in zip(q,D)))+';')
for q in Q:lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_10.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/traditional-spline-comparison-check.json').write_text(json.dumps(dict(figure='9.10',representative_data=[[str(x) for x in q] for q in Q],chord_parameters=list(map(str,params)),parameter_enclosures=[[str(x) for x in b] for b in bounds],traditional_knots=list(map(str,U)),ordinary_averaged_knots=list(map(str,V)),traditional_9x9_solve_equals_independent_5x5_Thomas_solve_exactly=True,traditional_all7point_and2derivative_constraints_exact=True,ordinary_all7point_constraints_exact=True,native_C2_checks=[nc,rc],endpoint_derivatives=[list(map(str,D0)),list(map(str,Dn))],derivative_magnitude_is_represented_total_chord_length=str(alpha),total_chord_length_enclosure=[str(sum(lo)),str(sum(hi))],arrow_common_scale='1/5',arrows_belong_to='solid traditional spline'),indent=2)+'\n')
print('PASS:traditional9x9solve equals independent5x5Thomas solution;ordinary7x7solve;allpoint/derivative constraints,C2native checks.')
