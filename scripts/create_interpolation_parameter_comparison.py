"""9.4:solve three cubic interpolants of exactly the same seven data points."""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json
from global_interpolation_data import Q,LENGTHS,PARAMS,interpolate
from native_bspline import segments,check,de_boor,cubic_path,point
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_04.tex')['applied']
scale=10**12
lo=tuple(F(isqrt(x.numerator*scale**2//x.denominator),scale) for x in LENGTHS)
hi=tuple(x+F(1,scale) for x in lo)
assert all(a*a<=ell<b*b for a,b,ell in zip(lo,hi,LENGTHS))
cent=(F(0),)+tuple(sum(lo[:i])/sum(lo) for i in range(1,6))+(F(1),)
bounds=tuple((sum(lo[:i])/sum(hi),sum(hi[:i])/sum(lo)) for i in range(1,6))
assert all(a<=t<=b and b-a<F(1,10**11) for t,(a,b) in zip(cent[1:-1],bounds))
uniform=tuple(F(i,6) for i in range(7))
cases=[('uniform',uniform,'uniform',''),('chord',PARAMS,'average','dashed'),('centripetal',cent,'average','dash dot')]
lines=['% Three independently solved interpolants;same representative data as9.3.',
       '% Centripetal square roots enclosed by exact rational bounds;parameter width<1e-11.',
       r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',
       r'\path[use as bounding box] (-.8,-3.6) rectangle (8,3.8);']
reports=[]
for name,params,mode,style in cases:
    U,P=interpolate(Q,params,mode=mode);ss=segments(U,P,3);nc=check(U,P,3,ss)
    assert all(de_boor(U,P,3,t)==q for t,q in zip(params,Q))
    lines.extend(cubic_path(s,style) for s in ss)
    reports.append(dict(method=name,parameters=list(map(str,params)),knots=list(map(str,U)),all7interpolation_constraints_exact=True,C2_native_checks=nc))
for q in Q:lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
for k,(name,params,mode,style) in enumerate(cases):
    y=-F(13,10)-F(9,10)*k;U,_=interpolate(Q,params,mode=mode)
    lines.append(r'\draw[book grid] '+point((-F(1,5),y))+'--'+point((F(37,5),y))+';')
    for t in U[4:7]:
        x=F(36,5)*t;lines.append(r'\draw[book grid] '+point((x,y-F(3,25)))+'--'+point((x,y+F(3,25)))+';')
    for end in (F(0),F(1)):
        for offset in (-F(3,25),-F(3,50),F(3,50),F(3,25)):
            x=F(36,5)*end+offset;lines.append(r'\draw[book grid] '+point((x,y-F(3,25)))+'--'+point((x,y+F(3,25)))+';')
    for t in params:lines.append(r'\draw '+point((F(36,5)*t,y))+r' circle[radius=2pt];')
    lines.append(r'\draw['+(style or 'solid')+'] '+point((F(1,5),y-F(3,10)))+'--'+point((F(4,5),y-F(3,10)))+';')
    lines.append(r'\node[anchor=west] at '+point((F(9,10),y-F(3,10)))+' {'+name+'};')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_04.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/interpolation-parameter-comparison-check.json').write_text(json.dumps(dict(figure='9.4',same_representative_data_as='9.3',methods=reports,centripetal_sqrt_lower=list(map(str,lo)),centripetal_sqrt_upper=list(map(str,hi)),centripetal_parameter_enclosures=[[str(x) for x in b] for b in bounds],parameter_enclosure_width_less_than='1e-11',all_rulers_use_actual_computed_parameters_and_knots=True),indent=2)+'\n')
print('PASS:three7x7solves,same seven data,exact interpolation and native C2 checks;certified centripetal parameter enclosures<1e-11.')
