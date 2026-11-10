"""11.17 positive single surface weight, exact push distance1 at(.55,.55)."""
from pathlib import Path
from fractions import Fraction as F
import json
from surface_relocation_example_data import U,V,P as INITIAL,view
from surface_geometry import surface,weights,isocurve,local_patch
from native_bspline import segments,check,cubic_path,point,de_boor
from rational_geometry import project,approximate
root=Path(__file__).resolve().parents[1];u=v=F(11,20);N=weights(U,3,u)[4]*weights(V,2,v)[3]
def homogeneous(P,w):return tuple(tuple(tuple((w if(i,j)==(4,3)else 1)*x for x in p)+(w if(i,j)==(4,3)else F(1),) for j,p in enumerate(row)) for i,row in enumerate(P))
R=project(surface(U,V,3,2,homogeneous(INITIAL,F(0)),u,v));target=(R[0],R[1],R[2]+2/N)
P=tuple(tuple(target if(i,j)==(4,3)else p for j,p in enumerate(row)) for i,row in enumerate(INITIAL));w=(1-N)/(2-N);OLD=homogeneous(P,F(1));NEW=homogeneous(P,w)
A=project(surface(U,V,3,2,OLD,u,v));Z=project(surface(U,V,3,2,NEW,u,v));assert tuple(z-a for a,z in zip(A,Z))==(0,0,-1);assert 0<w<1
whole=exterior=0
NI=segments(U,tuple((F(i==4),)for i in range(9)),3);NJ=segments(V,tuple((F(j==3),)for j in range(7)),2)
for a in NI:
    for b in NJ:
        old=local_patch(U,V,3,2,OLD,a['span'],b['span'])[0];new=local_patch(U,V,3,2,NEW,a['span'],b['span'])[0]
        for i in range(4):
            for j in range(3):
                assert tuple(y-x for x,y in zip(old[i][j],new[i][j]))==tuple((w-1)*a['bern'][i][0]*b['bern'][j][0]*z for z in target+(1,));whole+=1
        if a['b']<=U[4] or a['a']>=U[8] or b['b']<=V[3] or b['a']>=V[6]:assert old==new;exterior+=1
lines=['% Actual rational surface weight push; representative raised P43, fixed controls, no contours.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-9,-7) rectangle (9,8);'];nc=cross=arrows=0;maxerr=F(0)
def draw(net,variable,t,style,clip=None):
    global nc,cross,maxerr
    K,p,C=isocurve(U,V,3,2,net,variable,t);ss=segments(K,C,p);nc+=check(K,C,p,ss,steps=3)
    for z in(F(0),F(1,3),F(2,3),F(1)):
        assert de_boor(K,C,p,z)==(surface(U,V,3,2,net,z,t) if variable=='u'else surface(U,V,3,2,net,t,z));cross+=1
    for s in ss:
        if clip and not clip[0]<=s['a']<s['b']<=clip[1]:continue
        H=tuple(view(a[:3])+(a[-1],) for a in s['bern'])
        for q in approximate(H,F(1,100000)):
            maxerr=max(maxerr,q['certified_l1_error']);assert all(-9<a[0]<9 and -7<a[1]<8 for a in q['bern']);lines.append(cubic_path(q,style))
for variable in('u','v'):
    for t in(F(i,10)for i in range(11)):draw(OLD,variable,t,'book grid')
for t in map(F,('.3','.4','.5','.6','.7')):draw(NEW,'u',t,'dashed',(U[4],U[8]))
for t in map(F,('.35','.45','.55','.65','.75')):draw(NEW,'v',t,'dashed',(V[3],V[6]))
for a in map(F,('.35','.45','.55','.65','.75')):
    for b in map(F,('.3','.4','.5','.6','.7')):
        x,y=project(surface(U,V,3,2,OLD,a,b)),project(surface(U,V,3,2,NEW,a,b));d=tuple(v-u for u,v in zip(x,y));ray=tuple(u-v for u,v in zip(x,target))
        assert all(d[i]*ray[j]==d[j]*ray[i] for i in range(3)for j in range(3))
        xx,yy=view(x),view(y)
        if sum((a-b)**2 for a,b in zip(xx,yy))<F(1,100):continue
        lines.append(r'\draw[book grid,-{Stealth[length=3pt]}] '+point(xx)+'--'+point(yy)+';');arrows+=1
lines.extend([r'\draw[book axis] '+point(view(A))+'--'+point(view(Z))+';',r'\draw '+point(view(A))+r' circle[radius=2pt];',r'\draw '+point(view(Z))+r' circle[radius=2pt];',r'\node at (0,7.4) {$\bar u=\bar v=0.55,\quad d=1,\quad w_{4,3}:1\to\frac{1-N}{2-N}$};'])
origin=(-F(15,2),-F(11,2))
for end,label,anchor in[((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:lines.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tuple(a+b for a,b in zip(origin,view(end))))+r' node['+anchor+r'=4pt] {$'+label+'$};')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_19.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8');(root/'image_tex/build/surface-weight-push-check.json').write_text(json.dumps(dict(controls=P,u_knots=U,v_knots=V,parameter=(u,v),tensor_basis_at_target=N,old_weight=1,new_weight=w,selected_control=target,old_point=A,new_point=Z,exact_displacement=(0,0,-1),whole_homogeneous_coefficient_vector_identities=whole,unchanged_whole_exterior_patches=exterior,whole_boundaries_unchanged=True,native_checks=nc,tensor_isocurve_checks=cross,actual_perspective_arrows=arrows,certified_screen_error_cm=maxerr,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.17',whole,'whole homogeneous identities/',nc,'nativechecks; exact push1, positiveweight',float(w))
