"""Native parameter diagram and actual tensor polynomial surface mesh."""
from fractions import Fraction as F
from region_surface_data import K,G
from surface_relocation_example_data import view
from surface_geometry import isocurve,surface
from native_bspline import segments,check,cubic_path,point,de_boor
def domain(polygon,r,letter='a'):
    out=[r'\begin{tikzpicture}[book line,x=12cm,y=12cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-.1,-.15) rectangle (1.1,1.15);',r'\draw (0,0) rectangle (1,1);'];lo=min(p[0]for p in polygon);hi=max(p[0]for p in polygon);bot=min(p[1]for p in polygon);top=max(p[1]for p in polygon)
    for a,b in[((lo,0),(lo,1)),((hi,0),(hi,1)),((0,bot),(1,bot)),((0,top),(1,top))]:out.append(r'\draw[book grid,dashed] '+point(a)+'--'+point(b)+';')
    for i,j in r['selected_controls']:
        u,v=G[i],G[j];h=F(1,400)
        out.append(r'\draw[book grid] '+point((u-h,v))+'--'+point((u+h,v))+' '+point((u,v-h))+'--'+point((u,v+h))+';')
    out.append(r'\draw '+'--'.join(point(p)for p in polygon)+r'--cycle;')
    for p in polygon:out.append(r'\draw '+point(p)+r' circle[radius=1.5pt];')
    out.extend([r'\node[right=5pt] at (1,0) {$u$};',r'\node[above=5pt] at (0,1) {$v$};',r'\node at (.5,-.1) {('+letter+')};',r'\end{tikzpicture}']);return out
def mesh(P,r,letter='b'):
    out=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-9,-7) rectangle (9,8);'];nc=cross=paths=0
    for variable,values in [('u',tuple(F(i,32)for i in range(33))),('v',tuple(F(i,8)for i in range(9)))]:
        for t in values:
            U,p,C=isocurve(K,K,3,3,P,variable,t);ss=segments(U,C,p);nc+=check(U,C,p,ss,steps=2)
            for z in(F(0),F(1,3),F(2,3),F(1)):
                assert de_boor(U,C,p,z)==(surface(K,K,3,3,P,z,t)if variable=='u'else surface(K,K,3,3,P,t,z));cross+=1
            for s in ss:
                B=tuple(view(a)for a in s['bern']);assert all(-9<a[0]<9 and -7<a[1]<8 for a in B);out.append(cubic_path(dict(bern=B),'book grid'));paths+=1
    origin=(-F(15,2),-F(11,2))
    for end,label,anchor in[((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tuple(a+b for a,b in zip(origin,view(end))))+r' node['+anchor+r'=4pt] {$'+label+'$};')
    out.extend([r'\node at (0,7.4) {$d=6/5,\quad W=(0,0,1)$};',r'\node at (0,-6.6) {('+letter+')};',r'\end{tikzpicture}']);return out,dict(native_checks=nc,tensor_isocurve_checks=cross,exact_native_Bezier_paths=paths,native_curve_error=0)
