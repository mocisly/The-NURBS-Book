"""9.7:true global cubic interpolation exposes failure to preserve straight data runs."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
from global_interpolation_data import interpolate
from native_bspline import segments,check,de_boor,cubic_path,point
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_07.tex')['applied']
Q=tuple(tuple(map(F,p)) for p in [('0','-3'),('0','-2.4'),('0','0'),('0','.6'),('1.2','1.8'),('2.4','1.8'),('3','1.2'),('3','.6'),('3','0'),('3.6','-.6'),('4.2','-.6'),('6.6','-.6'),('7.2','-.6')])
squares=tuple(sum((b-a)**2 for a,b in zip(A,B)) for A,B in zip(Q,Q[1:]))
scale=10**12
lo=tuple(F(isqrt(x.numerator*scale**2//x.denominator),scale) for x in squares)
hi=tuple(x+F(1,scale) for x in lo)
assert all(a*a<=s<b*b for a,b,s in zip(lo,hi,squares))
params=(F(0),)+tuple(sum(lo[:i])/sum(lo) for i in range(1,len(Q)-1))+(F(1),)
bounds=tuple((sum(lo[:i])/sum(hi),sum(hi[:i])/sum(lo)) for i in range(1,len(Q)-1))
assert all(a<=t<=b and b-a<F(1,10**11) for t,(a,b) in zip(params[1:-1],bounds))
U,P=interpolate(Q,params);ss=segments(U,P,3);nc=check(U,P,3,ss)
assert all(de_boor(U,P,3,t)==q for t,q in zip(params,Q))
middle=(params[10]+params[11])/2;actual=de_boor(U,P,3,middle)
assert Q[9][1]==Q[10][1]==Q[11][1]==Q[12][1]==-F(3,5)
assert actual[1]!=-F(3,5)
lines=['% Representative data with exact vertical/horizontal runs;actual global interpolation solve.',
       r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-.9,-3.7) rectangle (8,2.6);',
       r'\draw[book grid,dashed] '+'--'.join(map(point,Q))+';']
lines.extend(cubic_path(s) for s in ss)
for q in Q:lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_07.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/collinear-data-interpolation-check.json').write_text(json.dumps(dict(figure='9.7',representative_data=[[str(x) for x in q] for q in Q],parameters=list(map(str,params)),knots=list(map(str,U)),all13interpolation_constraints_exact=True,C2_native_checks=nc,chord_parameter_enclosures=[[str(x) for x in b] for b in bounds],parameter_enclosure_width_less_than='1e-11',horizontal_data_run_indices=[9,10,11,12],witness_parameter=str(middle),witness_curve_point=list(map(str,actual)),nonzero_horizontal_line_deviation=str(actual[1]+F(3,5)),solid='actual globally solved cubic',dashed='data polyline reference'),indent=2)+'\n')
print('PASS:13point exact global cubic solve,C2native checks;nonzero exact deviation from horizontal four-point data run.')
