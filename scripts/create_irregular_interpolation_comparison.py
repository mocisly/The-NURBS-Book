"""9.5:three true interpolants of seven deliberately unevenly spaced points."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
from global_interpolation_data import interpolate
from native_bspline import segments,check,de_boor,cubic_path,point
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_05.tex')['applied']
Q=tuple(tuple(map(F,p)) for p in [('0','0'),('7/25','24/25'),('67/25','49/25'),('82/25','29/25'),('97/25','9/25'),('157/25','53/50'),('339/50','-7/50')])
lengths=tuple(map(F,['1','13/5','1','1','5/2','13/10']))
assert all(sum((b-a)**2 for a,b in zip(A,B))==ell**2 for A,B,ell in zip(Q,Q[1:],lengths))
chord=(F(0),)+tuple(sum(lengths[:i])/sum(lengths) for i in range(1,7))
scale=10**12
lo=tuple(F(isqrt(x.numerator*scale**2//x.denominator),scale) for x in lengths)
hi=tuple(x+F(1,scale) for x in lo)
assert all(a*a<=ell<b*b for a,b,ell in zip(lo,hi,lengths))
cent=(F(0),)+tuple(sum(lo[:i])/sum(lo) for i in range(1,6))+(F(1),)
bounds=tuple((sum(lo[:i])/sum(hi),sum(hi[:i])/sum(lo)) for i in range(1,6))
assert all(a<=t<=b and b-a<F(1,10**11) for t,(a,b) in zip(cent[1:-1],bounds))
cases=[('uniform',tuple(F(i,6) for i in range(7)),'uniform',''),('chord',chord,'average','dashed'),('centripetal',cent,'average','dash dot')]
lines=['% Independent representative scattered data;exact Pythagorean lengths.',
       r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',
       r'\path[use as bounding box] (-1,-3.6) rectangle (8,3.2);']
reports=[]
for name,params,mode,style in cases:
    U,P=interpolate(Q,params,mode=mode);ss=segments(U,P,3);nc=check(U,P,3,ss)
    assert all(de_boor(U,P,3,t)==q for t,q in zip(params,Q))
    lines.extend(cubic_path(s,style) for s in ss)
    reports.append(dict(method=name,parameters=list(map(str,params)),knots=list(map(str,U)),all7interpolation_constraints_exact=True,C2_native_checks=nc))
for q in Q:lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
for k,(name,params,mode,style) in enumerate(cases):
    y=-F(13,10)-F(9,10)*k;U,_=interpolate(Q,params,mode=mode)
    lines.append(r'\draw[book grid] '+point((-F(1,5),y))+'--'+point((F(349,50),y))+';')
    for t in U[4:7]:
        x=F(339,50)*t;lines.append(r'\draw[book grid] '+point((x,y-F(3,25)))+'--'+point((x,y+F(3,25)))+';')
    for end in (F(0),F(1)):
        for offset in (-F(3,25),-F(3,50),F(3,50),F(3,25)):
            x=F(339,50)*end+offset;lines.append(r'\draw[book grid] '+point((x,y-F(3,25)))+'--'+point((x,y+F(3,25)))+';')
    for t in params:lines.append(r'\draw '+point((F(339,50)*t,y))+r' circle[radius=2pt];')
    lines.append(r'\draw['+(style or 'solid')+'] '+point((F(1,5),y-F(3,10)))+'--'+point((F(4,5),y-F(3,10)))+';')
    lines.append(r'\node[anchor=west] at '+point((F(9,10),y-F(3,10)))+' {'+name+'};')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_05.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/irregular-interpolation-comparison-check.json').write_text(json.dumps(dict(figure='9.5',representative_data=[[str(x) for x in q] for q in Q],exact_chord_lengths=list(map(str,lengths)),methods=reports,centripetal_parameter_enclosures=[[str(x) for x in b] for b in bounds],parameter_enclosure_width_less_than='1e-11',all_rulers_use_actual_computed_parameters_and_knots=True),indent=2)+'\n')
print('PASS:exact unequal chord lengths;three seven-point solves and C2 native checks;centripetal enclosures<1e-11.')
