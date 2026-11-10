"""Shared mathematical drawing primitives, fixed camera and native typography."""
from fractions import Fraction as F
from gordon_network_data import view,UH,VH,UC,VC,CK,CL,Q
from native_bspline import segments,check,cubic_path,point,de_boor
from surface_geometry import isocurve,surface

def panel(net,letter,title,shift=0,control=False,highlight=None,reference=False):
    U,V,p,q,P=net
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-9,-7) rectangle (9,8);']
    proof=dict(native_curve_checks=0,tensor_isocurve_checks=0,exact_Bezier_pieces=0,control_shape=[len(P),len(P[0])],camera='1.5*(-.8x+.6y,-.36x-.48y+.8z)',native_font='10pt',font_rescaling=False)
    def curve(K,C,d,style=''):
        ss=segments(K,C,d);proof['native_curve_checks']+=check(K,C,d,ss,steps=3)
        for s in ss:
            B=tuple(view(a) for a in s['bern'])
            assert all(-9<a[0]<9 and -7<a[1]<8 for a in B),(title,B)
            out.append(cubic_path(dict(bern=B),style));proof['exact_Bezier_pieces']+=1
    if control:
        for row in P:out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(a)) for a in row)+';')
        for j in range(len(P[0])):out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(row[j])) for row in P)+';')
        for row in P:
            for a in row:out.append(r'\fill '+point(view(a))+r' circle[radius=1.2pt];')
        for a,name,anchor in [(P[0][0],r'P^{'+title+r'}_{0,0}','above right'),(P[-1][-1],r'P^{'+title+'}_{'+str(len(P)-1)+','+str(len(P[0])-1)+'}','below left')]:
            out.append(r'\node['+anchor+r'=6pt] at '+point(view(a))+r' {$'+name+'$};')
        if len(P)==6 and len(P[0])==7:
            at=point(view(P[5][1]));out.append(r'\draw '+at+r' circle[radius=2.8pt];');out.append(r'\node[below left=6pt] at '+at+r' {$P^{'+title+r'}_{5,1}$};')
    else:
        for variable,params in [('v',tuple(F(i,24) for i in range(25))),('u',tuple(F(i,12) for i in range(13)))]:
            for t in params:
                K,d,C=isocurve(*net,variable,t);curve(K,C,d,'book grid')
                for s in (F(0),F(1,3),F(2,3),F(1)):
                    assert de_boor(K,C,d,s)==(surface(*net,s,t) if variable=='u' else surface(*net,t,s));proof['tensor_isocurve_checks']+=1
        if highlight in ('v','both'):
            for C in CL:curve(VC,C,2,'line width=.9pt')
        if highlight in ('u','both'):
            for C in CK:curve(UC,C,3,'line width=.9pt')
        if reference:
            K,curves,d=(UC,CK,3) if highlight=='v' else (VC,CL,2)
            for C in curves:curve(K,C,d,'dashed')
        if highlight=='points':
            for row in Q:
                for a in row:out.append(r'\draw '+point(view(a))+r' circle[radius=2.5pt];')
    origin=(-F(15,2),-F(11,2))
    for end,name,anchor in [((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:
        to=tuple(a+b for a,b in zip(origin,view(end)));out.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(to)+r' node['+anchor+r'=4pt] {$'+name+'$};')
    out.extend([r'\node at (0,7.4) {$'+title+'(u,v)$};',r'\node at (0,-6.6) {('+letter+')};',r'\end{scope}'])
    return out,proof
