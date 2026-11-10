from pathlib import Path
from fractions import Fraction as F
import json
from coons_hermite_data import make,derivative
from coons_patch_data import U,V,C0U,C1U,C0V,C1V,CORNERS,view
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];data=make();out=['% True compatible derivative fields and twists, from exact Coons boundary data.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-10,-8) rectangle (11,10);'];nc=arrows=0
for K,C,p,D,label,anchor in [(U,C0U,3,data['DK'][0],r'C_0(u),D_0(u)','above left'),(U,C1U,3,data['DK'][1],r'C_1(u),D_1(u)','below right'),(V,C0V,2,data['DL'][0],r'C_0(v),D_0(v)','above right'),(V,C1V,2,data['DL'][1],r'C_1(v),D_1(v)','below left')]:
    ss=segments(K,C,p);nc+=check(K,C,p,ss,steps=5);out.extend(cubic_path(dict(bern=tuple(view(a) for a in s['bern']))) for s in ss)
    for t in (F(i,8) for i in range(1,8)):
        a=de_boor(K,C,p,t);d=de_boor(K,D,p,t);b=tuple(x+F(3,25)*y for x,y in zip(a,d));out.append(r'\draw[book axis] '+point(view(a))+'--'+point(view(b))+';');arrows+=1
    pos=view(de_boor(K,C,p,F(1,2)))
    if label.startswith('C_1(u)'):out.append(r'\node at (4,-3.5) {$'+label+'$};')
    elif label.startswith('C_1(v)'):out.append(r'\node at (-5.5,-4.5) {$'+label+'$};')
    else:out.append(r'\node['+anchor+r'=18pt] at '+point(pos)+r' {$'+label+'$};')
for a in (0,1):
    for b in (0,1):
        start=CORNERS[a][b];tw=data['twists'][a][b];end=tuple(x+F(3,50)*y for x,y in zip(start,tw));sp,ep=view(start),view(end)
        out.append(r'\fill '+point(sp)+r' circle[radius=1.5pt];');out.append(r'\draw[book axis,dashed] '+point(sp)+'--'+point(ep)+r' node['+('above' if ep[1]>=sp[1] else 'below')+r'=5pt] {$T_{'+str(a)+','+str(b)+r'}$};')
origin=(-F(17,2),-F(13,2))
for end,label,anchor in [((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:
    to=tuple(x+y for x,y in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(to)+r' node['+anchor+r'=4pt] {$'+label+'$};')
out.append(r'\end{tikzpicture}');(root/'image_tex/ch10/fig_10_36.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
data.update(native_curve_checks=nc,actual_cross_boundary_derivative_arrows=arrows,actual_corner_twist_arrows=4,derivative_drawing_scale='3/25',twist_drawing_scale='3/50',no_normalization_or_manual_arrow_directions=True,no_contour_tracing=True)
(root/'image_tex/build/coons-hermite-data.json').write_text(json.dumps(data,default=str,indent=2)+'\n',encoding='utf-8');print('PASS10.26:',arrows,'actualderivativearrows/4exacttwists/56wholeboundaryandfieldcontrolidentities/48wholesurfacecoefficients;truecubicv.')
