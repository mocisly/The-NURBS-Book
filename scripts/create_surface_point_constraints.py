from fractions import Fraction as F
from pathlib import Path
import json,argparse
from surface_constraint_data import U,V,P,BASE,UV,ACTIVE,constrained,value
from surface_relocation_example_data import view
from surface_geometry import isocurve,surface
from native_bspline import segments,check,cubic_path,point,de_boor
parser=argparse.ArgumentParser();parser.add_argument('figure',type=int,choices=(37,38));fig=parser.parse_args().figure
root=Path(__file__).resolve().parents[1];free=ACTIVE if fig==37 else((1,2),(2,2),(4,2));Q,proof=constrained(free,[(0,0,(F(0),F(0),F(1)))])
lines=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-9,-7) rectangle (28,8);'];nc=cross=0
for panel in (0,1):
    lines.append(r'\begin{scope}[xshift='+str(panel*19)+'cm]')
    if panel==0:
        for net,style in[(P,'book grid'),(Q,'book grid,dashed')]:
            for i in range(6):lines.append(r'\draw['+style+'] '+'--'.join(point(view(q))for q in net[i])+';')
            for j in range(5):lines.append(r'\draw['+style+'] '+'--'.join(point(view(net[i][j]))for i in range(6))+';')
            for row in net:
                for q in row:lines.append(r'\fill '+point(view(q))+' circle[radius=1.4pt];')
        for i,j in free:lines.append(r'\draw[book grid,book axis] '+point(view(P[i][j]))+'--'+point(view(Q[i][j]))+';')
    else:
        for net,style in[(P,'book grid'),(Q,'book line,dashed')]:
            for variable in('u','v'):
                for fixed in tuple(F(i,6)for i in range(7)):
                    K,p,C=isocurve(U,V,3,2,net,variable,fixed);ss=segments(K,C,p);nc+=check(K,C,p,ss,steps=4)
                    for t in(F(0),F(1,3),F(2,3),F(1)):
                        assert de_boor(K,C,p,t)==(surface(U,V,3,2,net,t,fixed)if variable=='u'else surface(U,V,3,2,net,fixed,t));cross+=1
                    for s in ss:lines.append(cubic_path(dict(bern=tuple(view(q)for q in s['bern'])),style))
        old,new=view(value(P)),view(value(Q));lines.append(r'\draw[book grid,book axis] '+point(old)+'--'+point(new)+';');lines.append(r'\node at (0,7.2) {$\Delta S(1/2,1/2)=(0,0,1)$};')
    origin=(-F(15,2),-F(11,2))
    for d,label,anchor in[((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:lines.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tuple(a+b for a,b in zip(origin,view(d))))+r' node['+anchor+r'=4pt] {$'+label+'$};')
    lines.append(r'\node at (0,-6.5) {('+('a'if panel==0 else'b')+')};');lines.append(r'\end{scope}')
lines.append(r'\end{tikzpicture}');(root/f'image_tex/ch11/fig_11_{fig+8}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/f'image_tex/build/surface-point-constraints-{fig}-check.json').write_text(json.dumps(dict(knots=(U,V),degrees=(3,2),controls=P,proof=proof,native_checks=nc,tensor_isocurve_checks=cross,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS',fig,'exactpoint/minimumnorm/fourboundaries;',nc,'native',cross,'tensor checks')
