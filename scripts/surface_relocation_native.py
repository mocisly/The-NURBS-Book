"""Shared native surface relocation panel primitives at the established camera."""
from fractions import Fraction as F
from surface_relocation_example_data import U,V,P,BASE,view
from surface_geometry import isocurve,surface
from native_bspline import segments,check,cubic_path,point,de_boor
def panel(new,data,letter,shift,indices,title):
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-9,-7) rectangle (9,8);'];nc=cross=pieces=arrows=0;Q=new[4];indices=set(indices)
    def curve(net,variable,t,style='',clip=None):
        nonlocal nc,cross,pieces
        K,p,C=isocurve(*net,variable,t);ss=segments(K,C,p);nc+=check(K,C,p,ss,steps=3)
        for z in (F(0),F(1,3),F(2,3),F(1)):
            assert de_boor(K,C,p,z)==(surface(*net,z,t) if variable=='u' else surface(*net,t,z));cross+=1
        for s in ss:
            if clip and not clip[0]<=s['a']<s['b']<=clip[1]:continue
            B=tuple(view(a) for a in s['bern']);assert all(-9<a[0]<9 and -7<a[1]<8 for a in B);out.append(cubic_path(dict(bern=B),style));pieces+=1
    if letter=='a':
        for row in P:out.append(r'\draw[book grid] '+'--'.join(point(view(a)) for a in row)+';')
        for j in range(7):out.append(r'\draw[book grid] '+'--'.join(point(view(row[j])) for row in P)+';')
        for row in P:
            for a in row:out.append(r'\fill '+point(view(a))+r' circle[radius=1pt];')
        for i in range(9):
            for j in range(7):
                for h,k in ((i+1,j),(i,j+1)):
                    if h<9 and k<7 and ((i,j) in indices or (h,k) in indices):out.append(r'\draw[book grid,dashed] '+point(view(Q[i][j]))+'--'+point(view(Q[h][k]))+';')
        for i,j in sorted(indices):out.extend([r'\draw '+point(view(P[i][j]))+r' circle[radius=2.3pt];',r'\draw[book axis] '+point(view(P[i][j]))+'--'+point(view(Q[i][j]))+';',r'\fill '+point(view(Q[i][j]))+r' circle[radius=1.5pt];'])
    else:
        for variable in ('u','v'):
            for t in (F(i,10) for i in range(11)):curve(BASE,variable,t,'book grid')
        u0,u1,v0,v1=data['local_support']
        for t in tuple(map(F,('.3','.4','.5','.6','.7'))):curve(new,'u',t,'dashed',(u0,u1))
        for t in tuple(map(F,('.35','.45','.55','.65','.75'))):curve(new,'v',t,'dashed',(v0,v1))
        for u in tuple(map(F,('.35','.45','.55','.65','.75'))):
            for v in tuple(map(F,('.3','.4','.5','.6','.7'))):
                a,b=surface(*BASE,u,v),surface(*new,u,v);delta=tuple(y-x for x,y in zip(a,b));assert delta[0]==delta[1]==0
                if delta[2]<F(1,10):continue
                out.append(r'\draw[book grid,-{Stealth[length=3pt]}] '+point(view(a))+'--'+point(view(b))+';');arrows+=1
        a,b=data['selected_point'],data['modified_selected_point'];out.extend([r'\draw[book axis] '+point(view(a))+'--'+point(view(b))+';',r'\draw '+point(view(a))+r' circle[radius=2pt];',r'\draw '+point(view(b))+r' circle[radius=2pt];'])
    origin=(-F(15,2),-F(11,2))
    for end,label,anchor in [((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:
        to=tuple(a+b for a,b in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(to)+r' node['+anchor+r'=4pt] {$'+label+'$};')
    out.extend([r'\node at (0,7.4) {$'+title+'$};',r'\node at (0,-6.6) {('+letter+')};',r'\end{scope}'])
    return out,dict(panel=letter,native_curve_checks=nc,tensor_crosschecks=cross,exact_Bezier_pieces=pieces,actual_displacement_arrows=arrows)
