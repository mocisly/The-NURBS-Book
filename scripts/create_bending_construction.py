"""11.28 exact projective point mapping toward a parabolic bending curve."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
root=Path(__file__).resolve().parents[1];O=(F(2),F(4));lam=F(3);ws=tuple(-1+F(i,4)for i in range(9));R=tuple((2+w,2+w*w/2)for w in ws);s=tuple((2-w*w/2)/4 for w in ws);P=tuple(tuple(o+(r-o)/v for o,r in zip(O,p))for p,v in zip(R,s));t=tuple(lam*v/(1+(lam-1)*v)for v in s);Q=tuple(tuple(o+v*(p-o)for o,p in zip(O,pt))for pt,v in zip(P,t));U=(F(0),)*4+tuple(F(i,6)for i in range(1,6))+(F(1),)*4
assert all(y==0 for x,y in P)
for a,b,c,v,z in zip(P,R,Q,s,t):
    assert b[1]==2+(b[0]-2)**2/2 and tuple(o+v*(p-o)for o,p in zip(O,a))==b
    assert z*(1-v)/(v*(1-z))==lam and tuple(o+z*(p-o)for o,p in zip(O,a))==c
lines=['% Explicit parabola B(w)=(2+w,2+w^2/2), exact ray intersections/cross ratio3.',r'\begin{tikzpicture}[book line,x=3cm,y=3cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-1.4,-.6) rectangle (5.4,4.5);'];nc=0
for C,style in[(P,''),(Q,'')]:
    ss=segments(U,C,3);nc+=check(U,C,3,ss,steps=7);lines.extend(cubic_path(a,style)for a in ss);lines.append(r'\draw[book grid,dashed] '+'--'.join(point(p)for p in C)+';')
    for p in C:lines.append(r'\draw '+point(p)+r' circle[radius=1.5pt];')
B=((F(3,5),F(149,50)),(F(2),F(51,50)),(F(17,5),F(149,50)));lines.append(cubic_path(dict(bern=B)));lines.append(r'\node[right=7pt] at (3.4,2.98) {$B(w)$};')
for i in(0,4,8):
    lines.append(r'\draw[book grid] '+point(O)+'--'+point(P[i])+';');lines.append(r'\draw '+point(R[i])+r' circle[radius=1.8pt];')
for label,p,anchor,sep in [('O',O,'above',8),(r'R_i',R[4],'below right',7),(r'P_i',P[4],'below',8),(r'\widehat P_i',Q[4],'below right',12),(r'P_s=C(u_s)',P[0],'below left',8),(r'P_t=C(u_e)',P[-1],'below right',8),(r'\widehat P_s',Q[0],'left',12),(r'\widehat P_t',Q[-1],'right',12)]:lines.append(r'\draw '+point(p)+r' circle[radius=1.8pt] node['+anchor+'='+str(sep)+r'pt] {$'+label+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_34.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/bending-construction-check.json').write_text(json.dumps(dict(centre=O,bending_curve='B(w)=(2+w,2+w^2/2)',lambda_value=lam,knots=U,controls=P,mapped_controls=Q,ray_intersections=R,s=s,t=t,exact_cross_ratio_checks=9,native_checks=nc,native_curve_error=0,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.28 9exactparabolaintersections/crossratios;',nc,'nativechecks.')
