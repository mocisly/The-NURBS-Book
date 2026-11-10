from pathlib import Path
from fractions import Fraction as F
import json
from surface_constraint_data import U,V,P,ACTIVE,constrained,value
from surface_relocation_example_data import view
from surface_geometry import isocurve,surface
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];Du,Dv=value(P,1,0),value(P,0,1)
R=((F(0),F(0),-F(1)),(F(0),F(1),F(0)),(F(1),F(0),F(0)))
assert all(sum(R[k][i]*R[k][j]for k in range(3))==F(i==j)for i in range(3)for j in range(3))
def rotate(d):return tuple(sum(a*b for a,b in zip(row,d))for row in R)
targets=[(tuple(2*x for x in Du),tuple(2*x for x in Dv)),(rotate(Du),rotate(Dv))]
lines=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-9,-7) rectangle (28,8);'];nc=cross=0;proofs=[]
for panel,(tu,tv) in enumerate(targets):
    Q,proof=constrained(ACTIVE,[(0,0,(F(0),)*3),(1,0,tuple(b-a for a,b in zip(Du,tu))),(0,1,tuple(b-a for a,b in zip(Dv,tv)))]);proofs.append(proof)
    assert value(Q)==value(P)and value(Q,1,0)==tu and value(Q,0,1)==tv
    lines.append(r'\begin{scope}[xshift='+str(panel*19)+'cm]')
    for net,style in[(P,'book grid'),(Q,'book line,dashed')]:
        for variable in('u','v'):
            for fixed in tuple(F(i,6)for i in range(7)):
                K,p,C=isocurve(U,V,3,2,net,variable,fixed);ss=segments(K,C,p);nc+=check(K,C,p,ss,steps=4)
                for t in(F(0),F(1,3),F(2,3),F(1)):
                    assert de_boor(K,C,p,t)==(surface(U,V,3,2,net,t,fixed)if variable=='u'else surface(U,V,3,2,net,fixed,t));cross+=1
                for s in ss:
                    B=tuple(view(q)for q in s['bern']);assert all(-9<x<9 and -7<y<8 for x,y in B);lines.append(cubic_path(dict(bern=B),style))
    o=value(P)
    for d,style in[(Du,'book line,book axis'),(Dv,'book line,book axis'),(tu,'book line,book axis,dashed'),(tv,'book line,book axis,dashed')]:
        end=tuple(a+b/4 for a,b in zip(o,d));lines.append(r'\draw['+style+'] '+point(view(o))+'--'+point(view(end))+';')
    lines.append(r'\fill '+point(view(o))+' circle[radius=1.8pt];')
    lines.append(r'\node at (0,7.2) {$'+(r'\widehat D_u=2D_u,\quad\widehat D_v=2D_v'if panel==0 else r'\widehat D_u=R_y(-\pi/2)D_u,\quad\widehat D_v=R_y(-\pi/2)D_v')+'$};')
    origin=(-F(15,2),-F(11,2))
    for d,label,anchor in[((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:lines.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tuple(a+b for a,b in zip(origin,view(d))))+r' node['+anchor+r'=4pt] {$'+label+'$};')
    lines.append(r'\node at (0,-6.5) {('+('a'if panel==0 else'b')+')};');lines.append(r'\end{scope}')
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch11/fig_11_47.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-derivative-constraints-check.json').write_text(json.dumps(dict(knots=(U,V),controls=P,original_derivatives=(Du,Dv),target_derivatives=targets,rotation=R,cases=proofs,native_checks=nc,tensor_isocurve_checks=cross,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS exactfixedpoint/twopartials,minimum norm,fourboundaries;',nc,'native',cross,'tensor checks')
