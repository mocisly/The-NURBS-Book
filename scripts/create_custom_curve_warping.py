"""11.21 piecewise cubic shape functions applied to actual local controls."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import json
from curve_warping_data import U,P,US,UE,length
from knot51_data import insert
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];K,Q=U,P
for _ in range(5):
    mid=tuple((a+b)/2 for a,b in zip(K,K[1:])if US<=a<b<=UE)
    for t in mid:K,Q,_=insert(K,Q,3,t)
ids=tuple(i for i in range(len(Q))if K[i]>=US and K[i+4]<=UE);start,end=min(ids)-1,max(ids)+1;L=[Decimal(0)]
for a,b in zip(Q[start:end],Q[start+1:end+1]):L.append(L[-1]+length(tuple(y-x for x,y in zip(a,b))))
params={i:F(str(round(L[i-start]/L[-1],12)))for i in ids}
specs=[(tuple(F(i,6)for i in range(7)),tuple(map(F,('0','.85','.45','1','.45','.85','0')))),(tuple(map(F,('0','.15','.85','1'))),(F(0),F(1),F(1),F(0)))]
def value(t,knots,values):
    j=next((i for i in range(len(knots)-1)if knots[i]<=t<knots[i+1]),len(knots)-2);v=(t-knots[j])/(knots[j+1]-knots[j]);return values[j]+(values[j+1]-values[j])*(3*v*v-2*v**3)
lines=['% Two explicit C1 piecewise cubic shape functions, actual Eq11.48; no raster tracing.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]'];reports=[];nc=0
for index,(nodes,values)in enumerate(specs):
    R=tuple((p[0],p[1]-F(3,5)*value(params[i],nodes,values))if i in params else p for i,p in enumerate(Q));ss=segments(K,R,3);nc+=check(K,R,3,ss,steps=3)
    for s in ss:
        if s['b']<=US or s['a']>=UE:assert s['power']==next(z for z in segments(U,P,3)if z['a']<=s['a']<s['b']<=z['b'])['power']
    lines.extend([r'\begin{scope}[xshift='+str(18*index)+r'cm]',r'\begin{scope}[x=4cm,y=4cm]',r'\path[use as bounding box] (-.2,-1.2) rectangle (4.2,1.4);'])
    lines.extend(cubic_path(s,'book grid,dotted')for s in segments(U,P,3));lines.extend(cubic_path(s)for s in ss)
    for t in(US,UE):lines.append(r'\draw '+point(de_boor(U,P,3,t))+r' rectangle ++(.025,.025);')
    lines.extend([r'\draw[book axis] (.5,-.85)--(3.7,-.85) node[right=5pt] {$t$};',r'\draw[book axis] (.5,-.85)--(.5,-.15) node[above=5pt] {$f$};'])
    for a,b,x,y in zip(nodes,nodes[1:],values,values[1:]):
        B=tuple((F(1,2)+3*(a+(b-a)*F(j,3)),-F(17,20)+F(1,2)*v)for j,v in enumerate((x,x,y,y)));lines.append(cubic_path(dict(bern=B)))
    lines.extend([r'\node[below=5pt] at (.5,-.85) {$0$};',r'\draw[book grid] (3.5,-.88)--(3.5,-.82) node[below=7pt] {$1$};',r'\node at (2,-1.1) {('+chr(97+index)+')};',r'\end{scope}',r'\end{scope}'])
    assert all(0<=value(t,nodes,values)<=1 for t in params.values());reports.append(dict(shape_nodes=nodes,shape_values=values,interpolation='zero-slope cubic Hermite between nodes; C1 at every join',modified_controls=R,control_displacement_upper_bound=F(3,5),whole_exterior_spans_unchanged=True))
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_24.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/custom-curve-warping-check.json').write_text(json.dumps(dict(original_knots=U,original_controls=P,refined_knots=K,refined_controls=Q,eligible_indices=ids,chord_parameters=params,local_control_count=len(Q),native_checks=nc,cases=reports,no_contour_tracing=True,native_curve_error=0),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.21',nc,'nativechecks,',len(Q),'controls; two exactC1 scalar functions, whole exterior unchanged.')
