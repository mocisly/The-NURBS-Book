"""11.26 support-local orthogonal projection to a disjoint slanted line."""
from pathlib import Path
from fractions import Fraction as F
import json
from knot51_data import insert
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];U=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
P=tuple(tuple(map(F,p))for p in [('.5','-.6'),('.1','.15'),('.6','.95'),('1.6','1.4'),('2.5','.8'),(3,'.15'),(4,'.15')]);us,ue=F(1,8),F(1,2);K,Q,_=insert(U,P,3,us)
for _ in range(3):
    mid=tuple((a+b)/2 for a,b in zip(K,K[1:])if us<=a<b<=ue)
    for t in mid:K,Q,_=insert(K,Q,3,t)
ids=tuple(i for i in range(len(Q))if K[i]>=us and K[i+4]<=ue)
def project(p):
    x,y=p;alpha=(1+4*x-3*y)/25;return x-4*alpha,y+3*alpha
R=tuple(project(p)if i in ids else p for i,p in enumerate(Q));assert max(-4*x+3*y for x,y in P)<1
flat=[];nc=0
for s in segments(K,R,3):
    if tuple(-4*x+3*y for x,y in zip(*s['power']))==(1,0,0,0):flat.append((s['a'],s['b']))
    if s['b']<=us or s['a']>=ue:assert s['power']==next(z for z in segments(U,P,3)if z['a']<=s['a']<s['b']<=z['b'])['power']
assert flat
lines=['% Explicit representative hooked cubic; exact orthogonal projection to -4x+3y=1.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]']
for index,C in enumerate((Q,R)):
    ss=segments(K,C,3);nc+=check(K,C,3,ss,steps=3);lines.extend([r'\begin{scope}[xshift='+str(18*index)+r'cm]',r'\begin{scope}[x=3.5cm,y=3.5cm]',r'\path[use as bounding box] (-.5,-.9) rectangle (4.4,2.7);',r'\draw[book grid] (-.4,-.2)--(1.5,2.3333333333) node[above right=5pt] {$L$};'])
    if index==0:
        lines.append(r'\draw[book grid,dashed] '+'--'.join(point(p)for p in P)+';')
        for p in P:lines.append(r'\draw '+point(p)+r' circle[radius=1.5pt];')
    else:lines.extend(cubic_path(s,'book grid,dotted')for s in segments(U,P,3))
    lines.extend(cubic_path(s)for s in ss)
    for t,label in[(us,r'C(u_s)'),(ue,r'C(u_e)')]:
        p=de_boor(U,P,3,t);lines.append(r'\draw '+point(p)+r' rectangle ++(.025,.025);')
        if index==0:lines.append(r'\node['+('right' if t==us else 'below right')+r'=9pt] at '+point(p)+r' {$'+label+'$};')
    lines.extend([r'\node at (2,-.8) {('+chr(97+index)+')};',r'\end{scope}',r'\end{scope}'])
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_32.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/nonintersecting-curve-flattening-check.json').write_text(json.dumps(dict(original_knots=U,original_controls=P,refined_knots=K,refined_controls=Q,modified_controls=R,interval=(us,ue),eligible_indices=ids,line=(-4,3,1),original_curve_entirely_strictly_below_line=True,flat_whole_polynomial_spans=flat,entire_exterior_spans_unchanged=True,native_checks=nc,native_curve_error=0,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.26',nc,'nativechecks/',len(flat),'exact flatspans; entire curve disjoint fromL by convexhull.')
