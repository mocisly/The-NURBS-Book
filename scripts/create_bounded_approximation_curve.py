"""9.2:representative normal-offset data with exact globally nearest projections."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
from polynomial_native import multiply
from bspline_math import add,evaluate
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_02.tex')['applied']
U=(F(0),)*3+(F(1),)*3;P=((F(0),F(0)),(F(4),F(25,4)),(F(8),F(1,2)))
ss=segments(U,P,2);nc=check(U,P,2,ss);X,Y=ss[0]['power'];assert X==(0,8,0) and Y==(0,F(25,2),-12)
parameters=tuple(map(F,('0','1/10','1/4','3/8','1/2','5/8','3/4','9/10','1')))
lambdas=tuple(map(F,('0','1/50','-1/50','1/50','-1/40','1/40','-1/25','1/50','0')))
E=F(1,2);Q=[];proofs=[]
for a,lam in zip(parameters,lambdas):
    c=(evaluate(X,a),evaluate(Y,a));dy=F(25,2)-24*a;normal=(-dy,F(8));q=tuple(x+lam*n for x,n in zip(c,normal));Q.append(q)
    error2=sum((x-y)**2 for x,y in zip(q,c));assert error2<E*E
    assert sum((x-y)*v for x,y,v in zip(q,c,(F(8),dy)))==0
    dx=add(X,(-q[0],));yy=add(Y,(-q[1],));dist=add(multiply(dx,dx),multiply(yy,yy));diff=add(dist,(-error2,))
    delta=(-a,F(1));bracket=add((F(64)+192*lam,),multiply((F(25,2)-12*a,-F(12)),(F(25,2)-12*a,-F(12))))
    expected=multiply(multiply(delta,delta),bracket)
    assert not any(add(diff,tuple(-x for x in expected)))
    lower=F(64)+192*lam;assert lower>0
    proofs.append({'projection_parameter':str(a),'normal_offset_lambda':str(lam),'data_point':list(map(str,q)),'footpoint':list(map(str,c)),'exact_squared_distance':str(error2),'global_distance_difference_factorization_exact':True,'positive_quadratic_factor_lower_bound':str(lower)})
Q=tuple(Q);assert Q[0]==P[0] and Q[-1]==P[-1]
index=6;foot=(evaluate(X,parameters[index]),evaluate(Y,parameters[index]));qi=Q[index];gap=tuple(c-q for c,q in zip(foot,qi))
top=tuple(c+2*v for c,v in zip(foot,gap));bottom=tuple(q-2*v for q,v in zip(qi,gap))
lines=['% Representative bounded approximation:C(u)=(8u,25u/2-12u^2),nine normal-offset data points.',
       '% Global closest-point proof:distance^2(u)-distance^2(a)=(u-a)^2[64+192lambda+(25/2-12a-12u)^2]>0.',
       r'\begin{tikzpicture}[book line,x=2.2cm,y=2.2cm]',r'\path[use as bounding box] (-.8,-.8) rectangle (9,4.5);']
lines.extend(cubic_path(s) for s in ss)
lines.extend([r'\draw[book grid] '+point(qi)+'--'+point(foot)+';',r'\draw[book axis] '+point(top)+'--'+point(foot)+';',r'\draw[book axis] '+point(bottom)+'--'+point(qi)+';',r'\node[above right=6pt] at '+point(top)+r' {$e_i$};'])
for q in Q:lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
for q,label,anchor in [(Q[0],'0','below right'),(Q[-1],'m','below left'),(qi,'i','below right')]:
    lines.append(r'\node['+anchor+r'=7pt] at '+point(q)+r' {$\mathbf Q_'+label+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch09/fig_9_02.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/bounded-approximation-curve-check.json').write_text(json.dumps({'figure':'9.2','representative_curve_power':[[str(x) for x in p] for p in (X,Y)],'degree':2,'data_count':9,'m':8,'E':str(E),'all_exact_squared_errors_strictly_below_E_squared':True,'max_squared_error':str(max(F(p['exact_squared_distance']) for p in proofs)),'endpoint_constraints_exact':True,'projection_proofs':proofs,'shown_error_index':index,'native_curve_checks':nc,'native_coordinate_scale_cm':'11/5','all_feet_are_unique_global_minima_not_only_stationary_points':True},indent=2)+'\n')
print('PASS:all9unique global normal projections proved by full distance-polynomial factorization,allerrors<E=1/2,endpoints exact;true representative quadratic curve.')
