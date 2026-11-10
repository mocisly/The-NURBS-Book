"""11.25 actual projection selection rules, exact flat spans and local bumps."""
from pathlib import Path
from fractions import Fraction as F
import json
from curve_warping_data import U,P,K,Q,US,UE,ELIGIBLE,identities
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];height=F(3,4)
global_ids=tuple(i for i,p in enumerate(Q)if p[1]>height);local_ids=ELIGIBLE
project=lambda ids:tuple((x,height)if i in ids else(x,y)for i,(x,y)in enumerate(Q))
B,C=project(global_ids),project(local_ids);flat={};nc=0;panels=[]
for index,R in enumerate((Q,B,C)):
    ss=segments(K,R,3);nc+=check(K,R,3,ss,steps=3);flat[index]=tuple((s['a'],s['b'])for s in ss if s['power'][1]==(height,0,0,0))
    out=[r'\begin{scope}[x=4cm,y=4cm]',r'\path[use as bounding box] (-.2,-.35) rectangle (4.3,1.45);',r'\draw[book grid] (-.1,.75)--(4.1,.75) node[right=4pt] {$L$};']
    out.extend(cubic_path(s,'book grid,dotted')for s in segments(U,P,3));out.extend(cubic_path(s)for s in ss)
    if index==0:
        out.append(r'\draw[book grid,dashed] '+'--'.join(point(p)for p in Q)+';')
        for p in Q:out.append(r'\draw '+point(p)+r' circle[radius=1.3pt];')
        for i in global_ids[::3]:out.append(r'\draw[book grid,book axis] '+point(Q[i])+'--'+point(B[i])+';')
        i=len(Q)//2;out.extend([r'\node[above=8pt] at '+point(Q[i])+r' {$P_i$};',r'\node[below=8pt] at '+point(B[i])+r' {$\widehat P_i$};',r'\node[right=7pt] at '+point((Q[i][0],(Q[i][1]+height)/2))+r' {$W$};'])
    for t,name,anchor in[(US,r'C(u_s)','above left'),(UE,r'C(u_e)','above right')]:
        p=de_boor(U,P,3,t);out.append(r'\draw '+point(p)+r' rectangle ++(.025,.025);')
        if index==0:out.append(r'\node['+anchor+r'=8pt] at '+point(p)+r' {$'+name+'$};')
    out.extend([r'\node at (2,-.28) {('+chr(97+index)+')};',r'\end{scope}']);panels.append(out)
assert flat[1] and flat[2]
for s in segments(K,C,3):
    if s['b']<=US or s['a']>=UE:assert s['power']==next(z for z in segments(U,P,3)if z['a']<=s['a']<s['b']<=z['b'])['power']
bump=de_boor(K,C,3,F(9,32))[1]-height;assert bump>0
lines=['% Exact control projection onto y=3/4: one-side versus support-local selection, not traced.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]']
for i,(x,y)in enumerate([(0,0),(F(37,2),0),(F(37,4),-F(38,5))]):lines+=[r'\begin{scope}[xshift='+str(float(x))+r'cm,yshift='+str(float(y))+r'cm]']+panels[i]+[r'\end{scope}']
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_31.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/intersecting-curve-flattening-check.json').write_text(json.dumps(dict(original_knots=U,original_controls=P,refined_knots=K,refined_controls=Q,line_y=height,one_side_indices=global_ids,local_support_indices=local_ids,one_side_controls=B,local_controls=C,exact_flat_polynomial_spans=flat,local_bump_at_9_32=bump,local_entire_exterior_spans_unchanged=True,refinement_whole_coefficients=identities,native_checks=nc,native_curve_error=0,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.25',nc,'nativechecks; flatspans',len(flat[1]),len(flat[2]),'localbump',float(bump))
