"""7.22: MakeNurbsCircle applied to the four stated angular intervals."""
from pathlib import Path
from fractions import Fraction as F
import json
from certified_trig import cos_sin,PI_LO,PI_HI
from native_bspline import segments,check,de_boor,point,cubic_path
from rational_geometry import project,approximate
from polynomial_native import multiply
from bspline_math import add,compose_affine,evaluate,derivative

root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for name in (25,26,27):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch07/fig_7_{name}.tex')['applied']
reports=[];panels=[]
for label,start,end,n in [('a',10,100,1),('b',30,170,2),('c',20,250,3),('d',40,330,4)]:
    delta=F(end-start,n);w=cos_sin(delta/2)[0];assert w>F(7,10)
    H=[]
    for i in range(n):
        first=cos_sin(start+i*delta)+(F(1),)
        middle=cos_sin(start+(F(i)+F(1,2))*delta)+(w,)
        last=cos_sin(start+(i+1)*delta)+(F(1),)
        if i==0:H.append(first)
        H.extend((middle,last))
    H=tuple(H);P=tuple(map(project,H));U=(F(0),)*3+tuple(F(i,n) for i in range(1,n) for j in range(2))+(F(1),)*3
    ss=segments(U,H,2);nc=check(U,H,2,ss);cert=[];paths=[]
    for s in ss:
        X,Y,Z=s['power'];res=add(add(multiply(X,X),multiply(Y,Y)),tuple(-x for x in multiply(Z,Z)))
        local=compose_affine(res,s['a'],s['b']-s['a']);bound=sum(map(abs,local))/w**2;assert bound<F(1,10**27)
        cert.append(str(bound));paths.extend(approximate(s['bern'],F(1,400000)))
    def velocity(s,u):
        h=[evaluate(c,u) for c in s['power']];dh=[evaluate(derivative(c),u) for c in s['power']]
        return tuple((dh[k]*h[-1]-h[k]*dh[-1])/h[-1]**2 for k in range(2))
    for l,r in zip(ss,ss[1:]):assert sum(abs(x-y) for x,y in zip(velocity(l,l['b']),velocity(r,r['a'])))<F(1,10**26)
    for i in range(101):
        u=F(i,100);h=de_boor(U,H,2,u);x,y=project(h);assert h[-1]>=w and abs(x*x+y*y-1)<F(1,10**27)
    lines=[r'\begin{scope}[x=4cm,y=4cm]',r'\path[use as bounding box] (-1.65,-1.8) rectangle (1.65,1.65);',
           r'\draw[book axis,book grid] (-1.4,0)--(1.4,0) node[right=4pt] {$x$};',
           r'\draw[book axis,book grid] (0,-1.4)--(0,1.4) node[above=4pt] {$y$};',
           r'\draw[book grid] '+'--'.join(map(point,P))+';']
    lines.extend(cubic_path(p) for p in paths)
    lines.extend(r'\draw '+point(p)+r' circle[radius=2pt];' for p in P)
    lines.extend([r'\node at (0,-1.6) {('+label+')};',r'\end{scope}']);panels.append(lines)
    reports.append({'panel':label,'start_degrees':start,'end_degrees':end,'segments':n,'controls':[[str(x) for x in p] for p in P],'knots':list(map(str,U)),'middle_weight':str(w),'native_checks':nc,'trig_coordinate_error_bound':'1e-29','circle_squared_radius_error_bounds':cert,'C1_join_L1_mismatch_bound':'1e-26','circle_evaluations':101,'native_path_count':len(paths),'native_L1_error_in_unit_coordinates':str(max(p['certified_l1_error'] for p in paths))})
for number,lines in [(25,panels[0]),(26,panels[1]),(27,panels[2]+[r'\begin{scope}[xshift=15.5cm]']+panels[3]+[r'\end{scope}'])]:
    (root/f'image_tex/ch07/fig_7_{number}.tex').write_text('% Native MakeNurbsCircle construction, certified trigonometric coordinates; unit XY scale4cm.\n'+r'\begin{tikzpicture}[book line]'+'\n'+'\n'.join(lines)+'\n'+r'\end{tikzpicture}'+'\n',encoding='utf-8')
(root/'image_tex/build/sweep-circle-arcs-check.json').write_text(json.dumps({'figure':'7.22','pi_enclosure_width':str(PI_HI-PI_LO),'all_equal_angular_segments_at_most90degrees':True,'panels':reports},indent=2)+'\n')
print('PASS:four prescribed angular intervals,1/2/3/4segments,404circle checks,trig coordinates certified<1e-29,C1joins<1e-26.')
