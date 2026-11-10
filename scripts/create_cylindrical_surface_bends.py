from pathlib import Path
from fractions import Fraction as F
import argparse,json
from cylindrical_surface_bending_data import U,V,BASE,make
from native_bspline import segments,check,cubic_path,point,de_boor,number
from surface_geometry import isocurve,surface
parser=argparse.ArgumentParser();parser.add_argument('figure',type=int,choices=(33,34));fig=parser.parse_args().figure;root=Path(__file__).resolve().parents[1]
H=F(3)if fig==33 else F(2);radius=F(2);lambdas=(F(1,2),F(3,2),-F(3))if fig==33 else(F(3,10),F(1),-F(1));cases=[make(l,H,radius)for l in lambdas]
def view(p):
    x,y,z=p;return F(6,5)*(-F(4,5)*x+F(3,5)*y),F(6,5)*(-F(9,25)*x-F(12,25)*y+F(4,5)*z)
lines=['% Actual tensor surfaces from rowwise cylindrical projective bending and rigid exterior motions.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-9,-7) rectangle (10,8);'];nc=cross=0;reports=[]
for y in(-F(3),F(3)):
    o=view((0,y,H));a,b=view((radius,0,0)),view((0,0,radius));lines.extend([r'\begin{scope}[cm={'+','.join(number(x)for x in(a[0],a[1],b[0],b[1]))+','+point(o)+'}]',r'\draw[book grid,dashed] (0,0) circle[radius=1cm];',r'\end{scope}'])
for x,z in[(radius,H),(-radius,H),(0,H-radius)]:lines.append(r'\draw[book grid,dashed] '+point(view((x,-3,z)))+'--'+point(view((x,3,z)))+';')
lines.append(r'\draw[book grid,dotted] '+point(view((0,-3,H)))+'--'+point(view((0,3,H)))+';')
corners=tuple(view((x,y,0))for x,y in[(-4,-3),(4,-3),(4,3),(-4,3)]);lines.append(r'\draw[book grid,dotted] '+'--'.join(point(p)for p in corners)+'--cycle;')
for S,r in cases:
    for variable,values in[('u',(F(0),F(1,3),F(2,3),F(1))),('v',(F(0),F(1,4),F(3,4),F(1)))]:
        for fixed in values:
            K,p,C=isocurve(*S,variable,fixed);ss=segments(K,C,p);nc+=check(K,C,p,ss,steps=2)
            for t in(F(0),F(1,3),F(2,3),F(1)):
                assert de_boor(K,C,p,t)==(surface(*S,t,fixed)if variable=='u'else surface(*S,fixed,t));cross+=1
            for s in ss:
                B=tuple(view(x)for x in s['bern']);assert all(-9<x<10 and -7<y<8 for x,y in B);lines.append(cubic_path(dict(bern=B),'book line'if fixed in(0,1)else'book grid'))
    label={F(1,2):r'\frac12',F(3,2):r'\frac32',-F(3):'-3',F(3,10):r'\frac3{10}',F(1):'1',-F(1):'-1'}[r['lambda_value']];corner=view(S[4][0][-1])
    if fig==34 and r['lambda_value']==F(3,10):
        lines.append(r'\draw[book grid] '+point(corner)+r'--(7,6.5) node[right=6pt] {$\lambda='+label+'$};')
    else:
        lines.append(r'\node[right=8pt] at '+point(corner)+r' {$\lambda='+label+'$};')
    reports.append(r)
origin=(-F(15,2),-F(11,2))
for end,label,anchor in[((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:lines.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tuple(a+b for a,b in zip(origin,view(end))))+r' node['+anchor+r'=4pt] {$'+label+'$};')
lines.extend([r'\node[below=8pt] at '+point(view((4,3,0)))+r' {$S(u,v)$};',r'\end{tikzpicture}']);(root/f'image_tex/ch11/fig_11_{fig+6}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/f'image_tex/build/cylindrical-surface-bends-{fig}-check.json').write_text(json.dumps(dict(degrees=(3,2),u_knots=U,v_knots=V,original_controls=BASE,cases=reports,native_checks=nc,tensor_isocurve_checks=cross,native_curve_error=0,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS',fig,nc,'nativechecks;',cross,'tensorchecks; true3x2surfaces/rigidrows/lambdas',list(map(str,lambdas)))
