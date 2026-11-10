"""Common exact orthographic rendering for10.7/10.8 comparison; font/camera fixed."""
from fractions import Fraction as F
from spine_skinning_example_data import view,SECTION_K
from native_bspline import segments,check,cubic_path,point,de_boor
from surface_geometry import surface,isocurve
def panel(base,VP,sections,letter,shift,with_derivatives,top=F(5),control_net=None,title_override=None):
    U,V,p,q,net=base;nc=cross=pieces=0
    assert all(-F(7,2)<view(x)[0]<12 and -F(123,10)<view(x)[1]<top for row in net for x in row)
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-3.5,-12.3) rectangle (12,'+str(float(top))+');']
    if control_net if control_net is not None else letter=='a':
        for rows in (net,tuple(zip(*net))):
            for row in rows:out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(v)) for v in row)+';')
        out.extend(r'\fill '+point(view(v))+r' circle[radius=1pt];' for row in net for v in row)
        title=r'$7\times'+str(len(net[0]))+r'\ \mathrm{control\ net}$'
    else:
        for variable,fixed in [('u',tuple(sorted(set(tuple(F(i,32) for i in range(33))+VP)))),('v',tuple(F(i,20) for i in range(21)))]:
            for t in fixed:
                K,degree,P=isocurve(*base,variable,t);ss=segments(K,P,degree);nc+=check(K,P,degree,ss,steps=3)
                for s in (F(0),F(1,3),F(2,3),F(1)):
                    assert de_boor(K,P,degree,s)==(surface(*base,s,t) if variable=='u' else surface(*base,t,s));cross+=1
                out.extend(cubic_path(dict(bern=tuple(view(p) for p in z['bern'])),'book grid') for z in ss);pieces+=len(ss)
        title=r'$S_v(u,\bar v_k)\parallel D_k$' if with_derivatives else r'$S(u,\bar v_k)=C_k(u)$'
    for section in sections:
        ss=segments(SECTION_K,section,3);nc+=check(SECTION_K,section,3,ss,steps=3)
        out.extend(cubic_path(dict(bern=tuple(view(p) for p in z['bern']))) for z in ss)
    origin=(-F(2),-F(9))
    for end,name,anchor in [((F(6,5),0,0),'x','below'),((0,F(6,5),0),'y','right'),((0,0,F(6,5)),'z','above')]:
        to=tuple(a+b for a,b in zip(origin,view(end)))
        out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(to)+r' node['+anchor+r'=4pt] {$'+name+'$};')
    if title_override is not None:title=title_override
    out.extend([r'\node at (4.25,'+str(float(top-F(1,2)))+') {'+title+'};',r'\node at (4.25,-11.9) {('+letter+')};',r'\end{scope}'])
    return out,dict(panel=letter,native_curve_checks=nc,isocurve_tensor_identities=cross,native_cubic_pieces=pieces,camera_scale='1.8',font_rescaling=False,common_bounds=[[-3.5,-12.3],[12,float(top)]])
