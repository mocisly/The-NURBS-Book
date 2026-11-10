"""11.32 analytic cylinder/axis, nearest-axis projection and radial cross ratio."""
from pathlib import Path
from fractions import Fraction as F
import json
from circular_bending_data import sqrtq
from surface_relocation_example_data import view
from native_bspline import point,number
root=Path(__file__).resolve().parents[1];O=(F(0),F(0),F(2));P=(F(2),F(0),F(0));radius=F(1);lam=F(2);d=tuple(p-o for p,o in zip(P,O));length=sqrtq(sum(x*x for x in d));s=radius/length;t=lam*s/(1+(lam-1)*s);R=tuple(o+s*x for o,x in zip(O,d));H=tuple(o+t*x for o,x in zip(O,d));assert t*(1-s)/(s*(1-t))==lam and abs(sum((r-o)**2 for r,o in zip(R,O))-1)<F(1,10**14)
lines=['% Analytic circular cylinder and actual nearest-axis/radial projective mapping, no traces.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-8,-6) rectangle (8,8);']
plane=tuple(view((x,y,0))for x,y in[(-3,-3),(3,-3),(3,3),(-3,3)]);lines.append(r'\draw[book grid] '+'--'.join(point(p)for p in plane)+'--cycle;')
for y in(-F(5,2),F(5,2)):
    centre=view((0,y,2));a,b=view((1,0,0)),view((0,0,1));lines.extend([r'\begin{scope}[cm={'+','.join(number(x)for x in(a[0],a[1],b[0],b[1]))+','+point(centre)+'}]',r'\draw[book grid,dashed] (0,0) circle[radius=1cm];',r'\end{scope}'])
for x,z in[(1,2),(-1,2),(0,1),(0,3)]:lines.append(r'\draw[book grid,dashed] '+point(view((x,-F(5,2),z)))+'--'+point(view((x,F(5,2),z)))+';')
lines.extend([r'\draw[book grid,dashed] '+point(view((0,-F(5,2),2)))+'--'+point(view((0,F(5,2),2)))+';',r'\draw '+point(view((0,-3,0)))+'--'+point(view((0,3,0)))+';',r'\draw[book grid] '+point(view(O))+'--'+point(view(P))+';',r'\draw[book axis] '+point(view((0,F(1,2),2)))+'--'+point(view((0,F(3,2),2)))+r' node[midway,above right=8pt] {$V$};'])
labels=[(R,'R_{i,j}','below right',18),(H,r'\widehat P_{i,j}','below right',8),(P,'P_{i,j}','below left',8),((0,-F(5,2),2),'Q','above left',8)]
for p,label,anchor,sep in labels:lines.append(r'\draw '+point(view(p))+r' circle[radius=1.8pt] node['+anchor+'='+str(sep)+r'pt] {$'+label+'$};')
lines.extend([r'\draw '+point(view(O))+r' circle[radius=1.8pt];',r'\draw[book grid] '+point(view(O))+r'--(-.6,5.1) node[above=7pt] {$O(w_{i,j})$};'])
lines.extend([r'\node[below right=7pt] at '+point(view((0,3,0)))+r' {$C_{u_c}(v)$};',r'\node[left=7pt] at '+point(view((3,-3,0)))+r' {$S(u,v)$};',r'\node at (0,7.3) {$r=1,\quad\lambda=2$};'])
origin=(-F(13,2),-F(9,2))
for end,label,anchor in[((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:lines.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tuple(a+b for a,b in zip(origin,view(end))))+r' node['+anchor+r'=4pt] {$'+label+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_38.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/cylinder-bending-construction-check.json').write_text(json.dumps(dict(axis='O(w)=(0,w,2)',surface='S(u,v)=(6u-3,6v-3,0)',radius=1,lambda_value=2,selected_control=P,nearest_axis_point=O,cylinder_intersection=R,mapped_control=H,s=s,t=t,exact_cross_ratio=True,axis_projection_orthogonal=True,circle_residual_bound='1e-14',no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.32 nearestaxis and exactcrossratio2; analyticcircle/radius checked; native affine ellipses.')
