from pathlib import Path
from fractions import Fraction as F
import json
from control_relocation_data import U,P,PHAT,BASIS,UBAR,make
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];m=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'));assert not next(e for e in m['images'] if e['tex']=='image_tex/ch11/fig_11_01.tex')['applied']
r=make();out=['% Exact cubic control-point relocation and its actual basis function; representative data in control_relocation_data.py.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm]',r'\path[use as bounding box] (-.7,-2.6) rectangle (8.7,3.8);'];nc=0
for controls,style in [(P,''),(PHAT,'dashed')]:
    ss=segments(U,controls,3);nc+=check(U,controls,3,ss,steps=7);out.extend(cubic_path(s,style) for s in ss)
out.append(r'\draw[book grid] '+'--'.join(point(p) for p in P)+';')
out.append(r'\draw[book grid,dashed] '+point(P[3])+'--'+point(PHAT[4])+'--'+point(P[5])+';')
for i,p in enumerate(P):
    anchor='below' if i in (0,1,7,8) else 'above left' if i in (2,3) else 'above right' if i in (5,6) else 'above'
    out.append(r'\draw '+point(p)+r' circle[radius=1.6pt] node['+anchor+r'=6pt] {$P_'+str(i)+'$};')
out.extend([r'\draw[book axis] '+point(P[4])+'--'+point(PHAT[4])+';',r'\draw '+point(PHAT[4])+r' circle[radius=1.8pt] node[below=6pt] {$\widehat P_4$};'])
A=r['selected_point'];B=r['modified_selected_point']
out.extend([r'\draw[book grid,dashed] '+point(A)+'--'+point(B)+r' node[midway,right=5pt] {$d$};',r'\draw '+point(A)+r' circle[radius=1.7pt] node[above right=8pt] {$P$};',r'\draw '+point(B)+r' circle[radius=1.7pt] node[below right=6pt] {$\widehat P$};'])
umax=r['peak_parameter'];A=de_boor(U,P,3,umax);B=de_boor(U,PHAT,3,umax);C=(A[0]-F(7,20),A[1]);D=(B[0]-F(7,20),B[1])
out.extend([r'\draw[book grid] '+point(A)+'--'+point(C)+' '+point(B)+'--'+point(D)+';',r'\draw[book grid,{Stealth[length=3pt]}-{Stealth[length=3pt]}] '+point(C)+'--'+point(D)+r' node[midway,left=4pt] {$d_{\max}$};'])
for p in (A,B):out.append(r'\draw '+point(p)+r' circle[radius=1.5pt];')
base=-F(17,10)
out.append(r'\draw[book grid] (0,-1.7)--(8,-1.7);')
for knot,label in [(F(1,5),'u_4'),(F(7,20),'u_5'),(F(1,2),None),(F(71,100),'u_7'),(F(9,10),'u_8')]:
    x=8*knot;out.append(r'\draw[book grid] '+point((x,base-F(1,20)))+'--'+point((x,base+F(1,20)))+';')
    if label:out.append(r'\node[below=6pt] at '+point((x,base))+r' {$'+label+'$};')
for x in (F(0),F(8)):
    for dx in (F(-3,100),F(-1,100),F(1,100),F(3,100)):out.append(r'\draw[book grid] '+point((x+dx,base-F(1,20)))+'--'+point((x+dx,base+F(1,20)))+';')
ss=segments(U,BASIS,3);nc+=check(U,BASIS,3,ss,steps=7)
for s in ss:
    if not any(p[0] for p in s['bern']):continue
    # Add u itself to this scalar curve using its exact linear Bernstein values.
    B=tuple((8*(s['a']+(s['b']-s['a'])*F(i,3)),base+F(7,5)*p[0]) for i,p in enumerate(s['bern']))
    out.append(cubic_path(dict(bern=B)))
x=8*umax;y=base+F(7,5)*r['basis_peak_midpoint_value'];out.extend([r'\draw[book grid] '+point((x,base))+'--'+point((x,y))+';',r'\draw '+point((x,y))+r' circle[radius=1.5pt];',r'\node[below=7pt] at '+point((x,base))+r' {$u_{\max}$};',r'\node at (5.6,-.8) {$N_{4,3}(u)$};',r'\end{tikzpicture}'])
(root/'image_tex/ch11/fig_11_01.tex').write_text('\n'.join(out)+'\n',encoding='utf-8');r.update(native_curve_checks=nc,native_curve_error=0,no_contour_tracing=True)
(root/'image_tex/build/control-relocation-check.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.1:',nc,'nativechecks/',r['exact_whole_power_coefficient_identities'],'wholepowercoefficients;uniquepeak',float(umax),'distance',float(r['selected_distance']),'dmax',float(r['dmax_midpoint_value']))
