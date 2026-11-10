from pathlib import Path
from fractions import Fraction as F
import json
from polyline_surface_warp_data import *
from native_bspline import segments,check,cubic_path,point,de_boor
from surface_geometry import isocurve,surface
root=Path(__file__).resolve().parents[1];P,r=make();A=['% Five hand-authored semantic centreline polylines; no font or scan contours.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]']
for index in range(2):
    A.extend([r'\begin{scope}[xshift='+str(18*index)+r'cm]',r'\begin{scope}[x=12cm,y=12cm]',r'\path[use as bounding box] (-.1,-.15) rectangle (1.1,1.15);',r'\draw (0,0) rectangle (1,1);'])
    if index:
        for x in(F(13,200),F(37,40)):A.append(r'\draw[book grid,dashed] '+point((x,0))+'--'+point((x,1))+';')
        for y in(F(29,100),F(71,100)):A.append(r'\draw[book grid,dashed] '+point((0,y))+'--'+point((1,y))+';')
        for i,j in r['selected_controls']:
            x,y=G[i],G[j];h=F(1,500);A.append(r'\draw[book grid] '+point((x-h,y))+'--'+point((x+h,y))+' '+point((x,y-h))+'--'+point((x,y+h))+';')
    for line in STROKES:
        A.append(r'\draw '+'--'.join(point(p)for p in line)+';')
        if not index:
            for p in line:A.append(r'\draw '+point(p)+r' circle[radius=1.3pt];')
    A.extend([r'\node[right=5pt] at (1,0) {$u$};',r'\node[above=5pt] at (0,1) {$v$};',r'\node at (.5,-.1) {('+chr(97+index)+')};',r'\end{scope}',r'\end{scope}'])
A.append(r'\end{tikzpicture}')
def view(p):
    x,y,z=p;return F(3,2)*(F(4,5)*x-F(3,5)*y),F(3,2)*(F(9,25)*x+F(12,25)*y+F(4,5)*z)
B=['% Exact bicubic surface from the same nearest-polyline distance mask.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-9,-7) rectangle (9,8);'];nc=cross=paths=0
for variable,values in [('u',tuple(F(i,64)for i in range(65))),('v',(F(0),F(1)))]:
    for t in values:
        U,p,C=isocurve(K,K,3,3,P,variable,t);ss=segments(U,C,p);nc+=check(U,C,p,ss,steps=2)
        for z in(F(0),F(1,3),F(2,3),F(1)):
            assert de_boor(U,C,p,z)==(surface(K,K,3,3,P,z,t)if variable=='u'else surface(K,K,3,3,P,t,z));cross+=1
        for s in ss:
            H=tuple(view(p)for p in s['bern']);assert all(-9<x<9 and -7<y<8 for x,y in H);B.append(cubic_path(dict(bern=H),'book grid'));paths+=1
origin=(-F(15,2),-F(11,2))
for end,label,anchor in[((1,0,0),'x','below right'),((0,1,0),'y','above left'),((0,0,1),'z','above')]:B.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tuple(a+b for a,b in zip(origin,view(end))))+r' node['+anchor+r'=4pt] {$'+label+'$};')
B.extend([r'\node at (0,7.4) {$r=1/100,\quad d=3/5,\quad W=(0,0,1)$};',r'\node at (0,-6.6) {(c)};',r'\end{tikzpicture}'])
for n,lines in[(29,A),(30,B)]: (root/f'image_tex/ch11/fig_11_{n}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
r.update(native_checks=nc,tensor_isocurve_checks=cross,exact_native_Bezier_paths=paths,native_curve_error=0,no_contour_tracing=True)
(root/'image_tex/build/polyline-surface-warp-check.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.24',r['selected_count'],'selected/4489 exactdistancechecks;',nc,'nativechecks/',paths,'exactBezierpaths.')
