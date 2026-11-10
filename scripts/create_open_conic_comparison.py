"""7.26: actual MakeOpenConic subdivisions and unchanged-parameter node insertion."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import evaluate,split,project,approximate
from bspline_math import add,derivative,compose_affine
from polynomial_native import multiply
from knot51_data import insert
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (32,33):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch07/fig_7_{n}.tex')['applied']
def sqrt_enclosed(v):
    D=10**40;k=isqrt(v.numerator*D*D//v.denominator);lo,hi=F(k,D),F(k+1,D)
    assert lo*lo<=v<=hi*hi
    return lo if lo*lo==v else (lo+hi)/2
def homogeneous(P,w):return tuple(tuple(ww*x for x in p)+(ww,) for p,ww in zip(P,(F(1),w,F(1))))
split_checks=0
def normalized_split(P,w):
    global split_checks
    old=homogeneous(P,w);l,r=split(old);Q=tuple(map(project,l));R=tuple(map(project,r));wn=sqrt_enclosed((1+w)/2)
    for i in range(41):
        t=F(i,40);assert evaluate(l,t)==evaluate(old,t/2) and evaluate(r,t)==evaluate(old,(1+t)/2)
        for raw,pp,alpha in [(l,Q,1/wn),(r,R,wn)]:
            before=project(evaluate(raw,alpha*t/(1-t+alpha*t)));after=project(evaluate(homogeneous(pp,wn),t))
            assert sum(abs(x-y) for x,y in zip(before,after))<F(1,10**36);split_checks+=1
    return [(Q,wn),(R,wn)]
def assemble(parts):
    H=[]
    for P,w in parts:
        h=homogeneous(P,w)
        if H:assert H[-1]==h[0]
        else:H.append(h[0])
        H.extend(h[1:])
    n=len(parts);U=(F(0),)*3+tuple(F(i,n) for i in range(1,n) for j in range(2))+(F(1),)*3
    return U,tuple(H)
PA=tuple(tuple(map(F,p)) for p in [(0,0),(2,5),(5,1)])
PB=tuple(tuple(map(F,p)) for p in [(-3,2),(0,4),(3,2)])
# Exact Angle tests from A7.3: a angle<=60, b angle>90, hence2 and4segments.
va=tuple(x-y for x,y in zip(PA[0],PA[1]));vb=tuple(x-y for x,y in zip(PA[2],PA[1]));dot=sum(x*y for x,y in zip(va,vb));assert dot>0 and 4*dot*dot>=sum(x*x for x in va)*sum(x*x for x in vb)
v0=tuple(x-y for x,y in zip(PB[0],PB[1]));v2=tuple(x-y for x,y in zip(PB[2],PB[1]));assert sum(x*y for x,y in zip(v0,v2))<0
partsA=normalized_split(PA,F(1,2));firstB=normalized_split(PB,-F(1,2));assert all(w==F(1,2) for pp,w in firstB)
partsB=[part for pp,w in firstB for part in normalized_split(pp,w)]
UA,HA=assemble(partsA);UB,HB=assemble(partsB);QA=tuple(map(project,HA));QB=tuple(map(project,HB));W=tuple(h[-1] for h in HB)
assert QB==tuple(tuple(map(F,q)) for q in [(-3,2),(-4,F(4,3)),(-3,F(2,3)),(-2,0),(0,0),(2,0),(3,F(2,3)),(4,F(4,3)),(3,2)])
KA=(F(0),)*3+(F(1),)*3;oldA=homogeneous(PA,F(1,2));oldB=homogeneous(PB,-F(1,2))
UR,HR,_=insert(KA,oldB,2,F(1,2));R=tuple(map(project,HR));assert R==(PB[0],(-6,0),(6,0),PB[-1])
assert all(s['power']==segments(KA,oldB,2)[0]['power'] for s in segments(UR,HR,2))
def implicit_conic(h,control,w):
    x,y,z=h;P0,P1,P2=control;a,b=P1[0]-P0[0],P2[0]-P0[0];c,e=P1[1]-P0[1],P2[1]-P0[1];det=a*e-b*c
    xx=x-P0[0]*z;yy=y-P0[1]*z;l1=(e*xx-b*yy)/det;l2=(-c*xx+a*yy)/det;l0=z-l1-l2
    return l1*l1-4*w*w*l0*l2
for i in range(201):
    u=F(i,200);assert de_boor(UR,HR,2,u)==evaluate(oldB,u)
    for U,H,pp,w in [(UA,HA,PA,F(1,2)),(UB,HB,PB,-F(1,2))]:
        h=de_boor(U,H,2,u);assert h[-1]>F(4,5) and abs(implicit_conic(h,pp,w))<F(1,10**36)
        weights=[de_boor(U,tuple((hh[-1]*F(k==j),) for k,hh in enumerate(H)),2,u)[0]/h[-1] for j in range(len(H))];assert min(weights)>=0 and sum(weights)==1
    h=evaluate(oldB,u);assert h[-1]>=F(1,4) and implicit_conic(h,PB,-F(1,2))==0
ssA=segments(UA,HA,2);ssB=segments(UB,HB,2);native=check(UA,HA,2,ssA)+check(UB,HB,2,ssB)
def velocity(s,u):
    h=[sum(c*u**k for k,c in enumerate(p)) for p in s['power']];dh=[sum(c*u**k for k,c in enumerate(derivative(p))) for p in s['power']]
    return tuple((dh[k]*h[-1]-h[k]*dh[-1])/h[-1]**2 for k in range(2))
for ss in (ssA,ssB):
    for l,r in zip(ss,ss[1:]):assert velocity(l,l['b'])==velocity(r,r['a'])
def curve_paths(ss):return [part for s in ss for part in approximate(s['bern'],F(1,200000))]
pathsA,pathsB=curve_paths(ssA),curve_paths(ssB)
def dot_node(q,label,anchor):return r'\draw '+point(q)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$'+label+'$};'
def tangents(pp,w):
    lines=[]
    for p,t,label,anchor in [(pp[0],tuple(2*w*(x-y) for x,y in zip(pp[1],pp[0])),r'\mathbf T_0','left'),(pp[2],tuple(2*w*(x-y) for x,y in zip(pp[2],pp[1])),r'\mathbf T_2','right')]:
        end=tuple(x+F(1,2)*y for x,y in zip(p,t));placement='pos=1,above left=7pt' if label==r'\mathbf T_0' else 'pos=.75,'+anchor+'=6pt'
        lines.append(r'\draw[book axis,book grid] '+point(p)+'--'+point(end)+r' node['+placement+'] {$'+label+'$};')
    return lines
panels=[]
for label,Q,pp,w,paths,bbox,caption,anchors in [
    ('a',QA,PA,F(1,2),pathsA,((-1,-2),(7,4.2)),(3,-1.6),['below left','above left','above','above right','right']),
    ('b',QB,PB,-F(1,2),pathsB,((-5.5,-2),(5.5,4.2)),(0,-1.6),['above left','left','below left','below','below','below','below right','right','above right'])]:
    lines=[r'\begin{scope}[x=1.6cm,y=1.6cm]',r'\path[use as bounding box] '+point(bbox[0])+' rectangle '+point(bbox[1])+';',r'\draw[book grid] '+'--'.join(map(point,Q))+';']
    lines.extend(cubic_path(s) for s in paths);lines+=tangents(pp,w)
    for i,(q,anchor) in enumerate(zip(Q,anchors)):
        text=r'\mathbf P_0=\mathbf Q_0' if i==0 else r'\mathbf P_2=\mathbf Q_'+str(i) if i==len(Q)-1 else r'\mathbf Q_'+str(i)
        lines.append(dot_node(q,text,anchor))
    extra=project(evaluate(homogeneous(pp,w),F(1,3) if label=='a' else F(2,5)))
    lines += [dot_node(extra,r'\mathbf P','below right' if label=='a' else 'above left'),r'\node at '+point(caption)+' {('+label+')};',r'\end{scope}'];panels.append(lines)
lines=[r'\begin{scope}[x=1.6cm,y=1.6cm]',r'\path[use as bounding box] (-7.2,-1.5) rectangle (7.2,4.2);',r'\draw[book grid] '+'--'.join(map(point,R))+';',r'\draw[book grid] '+'--'.join(map(point,QB))+';']+tangents(PB,-F(1,2))
for i in range(1,20):
    u=F(i,20)
    if i%5:
        c=project(de_boor(UB,HB,2,u));lines += [r'\begin{scope}[shift={'+point(c)+'}]',r'\draw (-1.7pt,-1.7pt) rectangle (1.7pt,1.7pt);',r'\end{scope}']
    if i!=10:
        c=project(de_boor(UR,HR,2,u));lines += [r'\begin{scope}[shift={'+point(c)+'}]',r'\draw (-1.7pt,0)--(1.7pt,0) (0,-1.7pt)--(0,1.7pt);',r'\end{scope}']
for i in (0,1,2,3,4,5,6,7,8):
    text=r'\mathbf P_0=\mathbf Q_0=\mathbf R_0' if i==0 else r'\mathbf P_2=\mathbf Q_8=\mathbf R_3' if i==8 else r'\mathbf Q_'+str(i)
    anchor='above left' if i==0 else 'above right' if i==8 else 'left' if i in (1,2) else 'right' if i in (6,7) else 'below'
    lines.append(dot_node(QB[i],text,anchor))
lines += [dot_node(R[1],r'\mathbf R_1','below left'),dot_node(R[2],r'\mathbf R_2','below right'),r'\node at (0,-1.15) {(c)};',r'\end{scope}'];panels.append(lines)
for n,ll in [(32,panels[0]+[r'\begin{scope}[xshift=21cm]']+panels[1]+[r'\end{scope}']),(33,panels[2])]:
    (root/f'image_tex/ch07/fig_7_{n}.tex').write_text('% Semantic MakeOpenConic: actual normalized split and Boehm parameter samples.\n'+r'\begin{tikzpicture}[book line]'+'\n'+'\n'.join(ll)+'\n'+r'\end{tikzpicture}'+'\n',encoding='utf-8')
(root/'image_tex/build/open-conic-comparison-check.json').write_text(json.dumps({'figure':'7.26','a_original_controls':[[str(x) for x in p] for p in PA],'a_original_weight':'1/2','b_original_controls':[[str(x) for x in p] for p in PB],'b_original_weight':'-1/2','algorithm_angle_tests_exact':True,'a_segments':2,'b_segments':4,'normalized_common_weight_squared':'3/4','normalization_correspondence_checks':split_checks,'native_deboor_checks':native,'conic_and_partition_checks_each_model':201,'exact_projected_C1_joins':True,'Boehm_insertion_all_homogeneous_coefficients_unchanged':True,'comparison_same_global_parameter_grid':'u=i/20; coincident control-point samples shared with control circles','native_error_bound_unit_coordinates':'1/200000'},indent=2)+'\n')
print('PASS:correct A7.3 angle branches,2/4segments,exact C1joins,201checks permodel,unchanged Boehm coefficients and actual same-u comparison samples.')
