"""9.55: actual noncoplanar cubic and exact auxiliary-point construction."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_67.tex')['applied']
P0=(F(4),F(0),F(0));P1=(F(4),F(4),F(0));P2=(F(0),F(3),F(0));P3=(F(0),F(0),F(4));controls=(P0,P1,P2,P3)
Ts=(F(0),F(1),F(0));Te=(F(0),-F(3,5),F(4,5));alpha=F(4);beta=-F(5)
def add(a,b,t=F(1)):return tuple(x+t*y for x,y in zip(a,b))
def mul(a,t):return tuple(t*x for x in a)
assert add(P0,Ts,alpha)==P1 and add(P3,Te,beta)==P2
assert sum(x*x for x in Ts)==sum(x*x for x in Te)==1
u=F(1,2);B=(F(1,8),F(3,8),F(3,8),F(1,8));a=alpha*B[1];b=beta*B[2]
P=tuple(sum(B[i]*controls[i][d] for i in range(4)) for d in range(3))
Pc=add(mul(P0,B[0]+B[1]),mul(P3,B[2]+B[3]));Pd=add(Pc,Ts,a)
assert P==add(Pd,Te,b) and Pc==(2,0,2) and Pd==(2,F(3,2),2) and P==(2,F(21,8),F(1,2))
assert Pc[0]+Pc[2]==Pd[0]+Pd[2]==4 and P[0]+P[2]!=4
assert alpha==a/B[1] and beta==b/B[2] and B[0]+B[1]==F(1,2)
def det(v,w,z):return v[0]*(w[1]*z[2]-w[2]*z[1])-v[1]*(w[0]*z[2]-w[2]*z[0])+v[2]*(w[0]*z[1]-w[1]*z[0])
independence=det(Ts,Te,add(P3,P0,-1));assert independence!=0
assert det(add(P1,P0,-1),add(P2,P0,-1),add(P3,P0,-1))!=0
# Gamma(u)=1-3u²+2u³ has negative derivative6u(u-1) for0<u<1.
assert 1-3*u*u+2*u*u*u==F(1,2)
U=(F(0),)*4+(F(1),)*4;ss=segments(U,controls,3);nc=check(U,controls,3,ss)
def view(p):
    x,y,z=p;return(F(12,5)*(-F(17,20)*x+F(19,20)*y),F(12,5)*(-F(21,50)*x-F(1,4)*y+z))
def line(a,b,style='book grid'):return r'\draw['+style+'] '+point(view(a))+'--'+point(view(b))+';'
O=(F(0),)*3;top=(F(0),F(4),F(4))
out=['% Exact noncoplanar cubic P0(4,0,0),P1(4,4,0),P2(0,3,0),P3(0,0,4);pi:x+z=4.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-12,-8) rectangle (11,14);']
out.append(r'\draw[book grid] '+'--'.join(point(view(p)) for p in (P0,P1,top,P3,P0))+';')
out.extend([line(P1,P2),line(P2,P3,'book grid,dashed')])
for q,end,name,anchor in [(P0,(F(26,5),0,0),'x','below left'),(P2,(0,F(21,5),0),'y','right'),(P3,(0,0,F(26,5)),'z','above')]:
    out.append(line(O,q,'book grid,dashed'));out.append(line(q,end,'book grid,book axis'))
    out.append(r'\node['+anchor+r'=5pt] at '+point(view(end))+' {$'+name+'$};')
out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern'])),'dashed') for s in ss)
out.extend([line(Pc,Pd,'book grid,book axis'),line(Pd,P,'book grid,dashed,book axis')])
out.extend([line(add(P0,Ts,F(4,5)),add(P0,Ts,F(9,5)),'book grid,book axis'),r'\node[below=7pt] at '+point(view(add(P0,Ts,F(11,5))))+r' {$\mathbf T_s$};',line(P3,add(P3,Te),'book grid,book axis'),r'\node[above left=6pt] at '+point(view(add(P3,Te)))+r' {$\mathbf T_e$};'])
for i,(q,anchor) in enumerate([(P0,'below left'),(P1,'below right'),(P2,'right'),(P3,'left')]):
    out.extend([r'\draw '+point(view(q))+r' circle[radius=2.3pt];',r'\node['+anchor+r'=6pt] at '+point(view(q))+r' {$\mathbf P_'+str(i)+'$};'])
for q,name,anchor in [(Pc,r'\mathbf P_c','left'),(Pd,r'\mathbf P_d','above'),(P,r'\mathbf P','below right')]:
    out.extend([r'\fill '+point(view(q))+r' circle[radius=1.6pt];',r'\node['+anchor+r'=7pt] at '+point(view(q))+' {$'+name+'$};'])
out.extend([r'\node at '+point(view((0,F(18,5),F(15,4))))+r' {$\pi$};',r'\end{tikzpicture}'])
(root/'image_tex/ch09/fig_9_67.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report=dict(figure='9.55',representative_controls=[list(map(str,p)) for p in controls],unit_Ts=list(map(str,Ts)),unit_Te=list(map(str,Te)),alpha=str(alpha),beta=str(beta),u=str(u),bernstein=list(map(str,B)),P=list(map(str,P)),Pc=list(map(str,Pc)),Pd=list(map(str,Pd)),a=str(a),b=str(b),plane='x+z=4',both_line_plane_intersections_exact=True,endpoint_tangent_chord_determinant=str(independence),noncoplanar=True,inferred_alpha_beta_exact=True,unique_parameter_proof='gamma=1-3u^2+2u^3,derivative6u(u-1)<0for0<u<1;gamma1/2=>u1/2',native_cubic_checks=nc,camera_scale='2.4',font_rescaling=False)
(root/'image_tex/build/spatial-cubic-point-construction-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.55:noncoplanar cubic;exactP/Pc/Pd/intersections,a1.5,b-1.875,alpha4,beta-5;uniqueu.5;unitTsTe;',nc,'nativechecks.')
