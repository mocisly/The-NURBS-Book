"""7.27: exact parabola focus/vertex and ellipse/hyperbola principal geometry."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from native_bspline import point,cubic_path
from rational_geometry import approximate,project,evaluate
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (34,35):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch07/fig_7_{n}.tex')['applied']
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(v,a):return tuple(a*x for x in v)
def rotate(v,sign):return ((12*v[0]-sign*5*v[1])/13,(sign*5*v[0]+12*v[1])/13)
def exact_sqrt(v):
    n,m=isqrt(v.numerator),isqrt(v.denominator);assert n*n==v.numerator and m*m==v.denominator;return F(n,m)
models=[('a',[(4,4),(-2,1),(1,-2)],F(1),-1),
        ('b',[(0,2),(-F(16,3),2),(-F(96,25),-F(14,25))],F(3,5),1),
        ('c',[(F(10,3),F(4,3)),(F(6,5),0),(F(10,3),-F(4,3))],F(5,3),-1)]
panels=[];reports=[]
for label,raw,w,sign in models:
    P=tuple(rotate(tuple(map(F,p)),sign) for p in raw);H=tuple(tuple(ww*x for x in p)+(ww,) for p,ww in zip(P,(F(1),w,F(1))))
    U=rotate((F(1),F(0)),sign);Vaxis=rotate((F(0),F(1)),sign);S=minus(P[0],P[1]);T=minus(P[2],P[1]);alpha,beta,gamma=dot(S,S),dot(S,T),dot(T,T)
    zeta=alpha+gamma+2*beta;delta=alpha*gamma-beta*beta;eta=alpha+gamma-2*beta
    record={'panel':label,'controls':[[str(x) for x in p] for p in P],'weight':str(w),'S_T_dot_data':list(map(str,(alpha,beta,gamma)))}
    if label=='a':
        axis=scale(plus(S,T),1/exact_sqrt(zeta));focus=plus(P[1],scale(plus(scale(S,gamma),scale(T,alpha)),1/zeta))
        vertex=plus(P[1],plus(scale(S,((gamma+beta)/zeta)**2),scale(T,((alpha+beta)/zeta)**2)))
        assert axis==U and focus==U and vertex==(0,0)
        record.update({'vertex':list(map(str,vertex)),'focus':list(map(str,focus)),'axis':list(map(str,axis)),'formulas7_58_to7_60_exact':True})
    else:
        k=1/(w*w);eps=k/(2*(k-1));center=plus(P[1],scale(plus(S,T),eps));assert center==(0,0)
        r1,r2=(F(4),F(2)) if label=='b' else (F(2),F(1));l1=eps/r1**2;l2=(eps if label=='b' else -eps)/r2**2
        assert l1<l2 and all(2*delta*l*l-(k*eta+4*beta)*l+2*(k-1)==0 for l in (l1,l2))
        if abs(k/2-gamma*l1)>abs(k/2-alpha*l1):bx,by=k/2-gamma*l1,beta*l1-k/2+1
        else:bx,by=beta*l1-k/2+1,k/2-alpha*l1
        rho2=alpha*bx*bx+2*beta*bx*by+gamma*by*by;rho=exact_sqrt(rho2);direction=scale(plus(scale(S,bx),scale(T,by)),1/rho)
        assert dot(direction,direction)==1 and abs(dot(direction,U))==1
        # Without the square root the manuscript OCR normalization is not a unit vector.
        wrong=scale(plus(scale(S,bx),scale(T,by)),1/rho2);assert dot(wrong,wrong)!=1
        record.update({'center':list(map(str,center)),'principal_radii':list(map(str,(r1,r2))),'lambda_roots':list(map(str,(l1,l2))),'rho_squared':str(rho2),'rho_correct_length':str(rho),'unit_principal_direction':list(map(str,direction)),'wrong_OCR_normalization_squared_norm':str(dot(wrong,wrong)),'center_radii_unit_direction_formulas_exact':True})
    for i in range(101):
        q=project(evaluate(H,F(i,100)));x,y=dot(q,U),dot(q,Vaxis)
        if label=='a':assert x==y*y/4 and (x-1)**2+y*y==(x+1)**2
        elif label=='b':assert x*x/16+y*y/4==1
        else:assert x*x/4-y*y==1 and x>=2
    paths=approximate(H,F(1,200000));record['exact_implicit_and_geometry_checks']=101;record['native_L1_error']=str(max(s['certified_l1_error'] for s in paths));reports.append(record)
    bbox={'a':((-F(23,10),-4),(6,3)),'b':((-F(13,2),-4),(F(4,5),3)),'c':((-F(6,5),-4),(F(11,2),3))}[label]
    lines=[r'\begin{scope}[x=1.5cm,y=1.5cm]',r'\path[use as bounding box] '+point(bbox[0])+' rectangle '+point(bbox[1])+';',r'\draw[book grid] '+'--'.join(map(point,P))+';']
    lines.extend(cubic_path(s) for s in paths)
    anchors=('below right','above left','below right') if label=='c' else ('above right','left','below right')
    for i,(p,anchor) in enumerate(zip(P,anchors)):lines.append(r'\draw '+point(p)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$\mathbf P_'+str(i)+'$};')
    if label=='a':
        lines += [r'\draw[book axis,book grid] (0,0)--'+point(scale(U,F(9,2)))+r' node[pos=.85,above=7pt] {$\mathbf A$};',
                  r'\draw (0,0) circle[radius=2pt] node[above left=7pt] {$\mathbf V$};',r'\draw '+point(U)+r' circle[radius=2pt] node[below=7pt] {$\mathbf F$};']
    elif label=='b':
        lines += [r'\draw[book axis,book grid] (0,0)--'+point(scale(U,-4))+r' node[pos=.65,above=7pt] {$-\mathbf U$};',
                  r'\draw[book axis,book grid] (0,0)--'+point(scale(Vaxis,2))+r' node[pos=.5,right=7pt] {$\mathbf V$};',
                  r'\draw (0,0) circle[radius=2pt] node[below right=7pt] {$\mathbf C$};']
    else:
        AU=scale(U,2);B=Vaxis;corner1,corner2=plus(AU,B),minus(AU,B)
        assert dot(corner1,U)**2/4-dot(corner1,Vaxis)**2==0 and dot(corner2,U)**2/4-dot(corner2,Vaxis)**2==0
        lines += [r'\draw[book grid,dashed] '+'--'.join(map(point,(scale(B,-1),corner2,corner1,B)))+'--cycle;',
                  r'\draw[book grid,dashed] (0,0)--'+point(scale(corner1,2))+r' node[above=7pt] {$\mathcal A_1$};',
                  r'\draw[book grid,dashed] (0,0)--'+point(scale(corner2,F(3,2)))+r' node[left=8pt] {$\mathcal A_2$};',
                  r'\draw[book axis,book grid] (0,0)--'+point(AU)+';',r'\node at (.9,-.7) {$\mathbf U$};',
                  r'\draw[book axis,book grid] (0,0)--'+point(B)+r' node[pos=.8,left=7pt] {$\mathbf V$};',
                  r'\draw (0,0) circle[radius=2pt] node[left=7pt] {$\mathbf C$};']
    captionx=(bbox[0][0]+bbox[1][0])/2;lines += [r'\node at '+point((captionx,-F(73,20)))+' {('+label+')};',r'\end{scope}'];panels.append(lines)
for n,ll in [(34,panels[0]),(35,panels[1]+[r'\begin{scope}[xshift=4cm]']+panels[2]+[r'\end{scope}'])]:
    (root/f'image_tex/ch07/fig_7_{n}.tex').write_text('% Exact representative conic data and principal geometry; proper rho length normalization.\n'+r'\begin{tikzpicture}[book line]'+'\n'+'\n'.join(ll)+'\n'+r'\end{tikzpicture}'+'\n',encoding='utf-8')
(root/'image_tex/build/conic-geometric-data-check.json').write_text(json.dumps({'figure':'7.27','models':reports,'rho_OCR_missing_square_root_proved':True,'hyperbola_asymptote_null_quadratic_form_exact':True},indent=2)+'\n')
print('PASS:303exact implicit checks,parabola focus/directrix,center/radii/eigenvalues and unit axes,hyperbola asymptotes; rho OCR missing square root verified.')
