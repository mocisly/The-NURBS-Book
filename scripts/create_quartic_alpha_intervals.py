"""Fig5.23: exact first extraction and denominator intervals for second segment."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point,number,de_boor
from native_polynomial_drawing import paths
from knot51_data import insert

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_29.tex';assert not target.exists()
U=(F(0),)*5+tuple(F(i,5) for i in range(1,5))+(F(1),)*5
P=tuple(tuple(F(str(t)) for t in pt) for pt in [(0,0),(3.3,0),(2.8,4.6),(5.7,6.2),(8.5,4.6),(7.8,0),(10.9,0),(11.6,3.7),(10.2,5.5)])
ss=segments(U,P,4);checks=check(U,P,4,ss);K,R=U,P
for i in range(3):K,R,_=insert(K,R,4,F(1,5))
assert K==(F(0),)*5+(F(1,5),)*4+tuple(F(i,5) for i in range(2,5))+(F(1),)*5
assert R[:5]==ss[0]['bern'] and R[4]==ss[1]['bern'][0]
# Exact knot insertion matches the independent extraction coefficients on all spans.
refined=segments(K,R,4);checks+=check(K,R,4,refined)
for s,t in zip(ss,refined):assert s['power']==t['power']
rows=[[(6,1,6,10),(7,1,7,11),(8,1,8,12)],[(7,2,7,10),(8,2,8,11)],[(8,3,8,10)]]
ratios=[]
for row in rows:
    values=[]
    for i,r,lo,hi in row:
        numerator=K[9]-K[lo];denominator=K[hi]-K[lo]
        assert numerator==F(1,5);value=numerator/denominator
        assert value in (F(1,2),F(1,3),F(1,4));values.append(str(value))
    ratios.append(values)
assert ratios==[['1/2','1/3','1/4'],['1/2','1/3'],['1/2']]
curve,report=paths(ss)
lines=['% Fig5.23: quartic control coefficients and exact alpha knot intervals.',
       '% Original does not supply coordinates; explicit representative data stored in report.',
       '% Curve paths approximate exact degree4 polynomials with certified error<=0.0001cm, no image contours.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-1.3,-6.4) rectangle (13.4,7);',
       r'\draw[book grid] '+'--'.join(map(point,P))+';']+curve
lines += [r'\draw[book grid] '+'--'.join(map(point,R[:7]))+';']
for pt in P:lines.append(r'\draw '+point(pt)+' circle[radius=1.6pt];')
for i,pt in enumerate(R[:7]):
    lines.append((r'\fill ' if i<=4 else r'\draw ')+point(pt)+' circle[radius=1.7pt];')
for i,pos in [(0,'below left=5pt'),(1,'below=5pt'),(2,'left=6pt'),(3,'below right=7pt'),(4,'right=7pt')]:
    label=r'\mathbf Q_'+str(i)+'^0'+(r'=\mathbf Q_0^1' if i==4 else '')
    lines.append(r'\node['+pos+'] at '+point(R[i])+' {$'+label+'$};')
for i,pos in [(5,'above=8pt'),(6,'above right=7pt')]:lines.append(r'\node['+pos+'] at '+point(R[i])+r' {$\mathbf Q_'+str(i-4)+'^1$};')
lines.append(r'\draw[book grid] (0,-1.4)--(12,-1.4);')
for t in sorted(set(K)):
    m=K.count(t)
    for j in range(m):
        x=12*t+F(13,100)*(F(j)-F(m-1,2))
        lines.append(r'\draw[book grid] '+point((x,F(-3,2)))+'--'+point((x,F(-13,10)))+';')
    label='0' if t==0 else '1' if t==1 else r'\frac{'+str(t.numerator)+'}{'+str(t.denominator)+'}'
    lines.append(r'\node[below=5pt] at '+point((12*t,F(-7,5)))+' {$'+label+'$};')
lines.append(r'\draw[book axis] (4.8,-.6)--(4.8,-1.2);')
for r,row in enumerate(rows,1):
    y=F(-5,2)-F(5,4)*(r-1)
    lines.append(r'\node[left=8pt] at '+point((F(19,10),y-F(1,5)))+' {$r='+str(r)+'$};')
    for j,(_,_,lo,hi) in enumerate(row):
        yy=y-F(7,20)*j;left,right=12*K[lo],12*K[hi]
        lines.append(r'\draw[book grid] '+point((left,yy+F(1,10)))+'--'+point((left,yy))+'--'+point((right,yy))+'--'+point((right,yy+F(1,10)))+';')
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/quartic-alpha-intervals-check.json').write_text(json.dumps({
    'figure':'5.23','degree':4,'original_U':list(map(str,U)),'U_after_first_extraction':list(map(str,K)),
    'representative_control_points':[[str(t) for t in pt] for pt in P],
    'refined_control_points':[[str(t) for t in pt] for pt in R],
    'native_curve_checks':checks,'unchanged_polynomial_spans':5,
    'first_extracted_five_controls_match_exactly':True,'alpha_rows':ratios,
    'common_numerator':'1/5','denominators_first_round':['2/5','3/5','4/5'],
    'analytic_native_rendering':report},indent=2)+'\n')
print('PASS:410 exact quartic checks,5 identical spans, first5 Bezier controls exact; alpha rows1/2,1/3,1/4;1/2,1/3;1/2; bound='+report['maximum_certified_L1_error_cm'])
