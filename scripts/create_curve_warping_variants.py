"""11.20 genuine Eq11.48 weight, direction and distance variants."""
from pathlib import Path
from fractions import Fraction as F
import json
from curve_warping_data import U,P,K,Q,US,UE,warp
from native_bspline import segments,check,cubic_path,point
root=Path(__file__).resolve().parents[1];unit=F(1,5)
scale=lambda C:tuple(tuple(unit*x for x in p)for p in C)
base=scale(P);refined=scale(Q);nc=0;reports=[];lines=['% Same parabolic shape/refinement as11.19, coordinate unit scaled1/5, native physical scale preserved.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]']
directions=((-F(3,5),-F(4,5)),(F(0),-F(1)),(F(3,5),-F(4,5)))
cases=[[(F(1,5),F(3,25),directions[1],r'w_3=1/5'),(F(1),F(3,25),directions[1],r'w_3=1'),(F(30),F(3,25),directions[1],r'w_3=30')],[(F(20),F(3,25),D,'W_'+str(i+1))for i,D in enumerate(directions)],[(F(20),d,directions[1],'d='+str(float(d)))for d in(F(1,20),F(1,10),F(3,20))]]
for index,(cx,cy)in enumerate([(0,0),(18,0),(9,-8)]):
    lines.extend([r'\begin{scope}[xshift='+str(cx)+r'cm,yshift='+str(cy)+r'cm]',r'\begin{scope}[x=20cm,y=20cm]',r'\path[use as bounding box] (-.036,-.09) rectangle (.836,.29);'])
    for s in segments(U,base,3):lines.append(cubic_path(s,'book grid'))
    for j,(w,d,D,label)in enumerate(cases[index]):
        C=scale(warp(w,d/unit,D));ss=segments(K,C,3);nc+=check(K,C,3,ss,steps=3);style=('dotted','dashed','')[j];lines.extend(cubic_path(s,style)for s in ss)
        assert sum(x*x for x in D)==1 and all(sum((x-y)**2 for x,y in zip(a,b))<=d*d for a,b in zip(C,refined))
        for s in ss:
            if s['b']<=US or s['a']>=UE:assert s['power']==next(t for t in segments(U,base,3)if t['a']<=s['a']<s['b']<=t['b'])['power']
        x=F(1,10)+j*F(6,25);lines.extend([r'\draw['+style+'] '+point((x,-F(3,100)))+'--'+point((x+F(1,25),-F(3,100)))+';',r'\node[anchor=west] at '+point((x+F(1,20),-F(3,100)))+r' {$'+label+'$};'])
        if index==1:lines.append(r'\draw[book grid,'+style+r',-{Stealth[length=4pt]}] (.4,.2)--'+point((F(2,5)+d*D[0],F(1,5)+d*D[1]))+';')
        reports.append(dict(panel=index,weight=w,distance_upper_bound=d,direction=D,controls=C,whole_exterior_polynomial_spans_unchanged=True,control_displacement_bound_verified=True))
    lines.extend([r'\node at (.4,-.078) {('+chr(97+index)+')};',r'\end{scope}',r'\end{scope}'])
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_23.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/curve-warping-variants-check.json').write_text(json.dumps(dict(original_curve='C(u)=(4u/5,4u(1-u)/5)',knots=K,controls=refined,parameter_interval=(US,UE),cases=reports,native_checks=nc,native_curve_error=0,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.20',nc,'nativechecks,9 actual variants, unit directions and bounds verified; exterior whole spans unchanged.')
