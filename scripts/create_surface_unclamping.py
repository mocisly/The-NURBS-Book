from pathlib import Path
from fractions import Fraction as F
import json
from surface_constraint_data import U,V,P as FULL
from surface_relocation_example_data import view
from unclamp_algorithm import unclamp
from surface_geometry import local_patch,isocurve,surface
from unclamped_geometry import verified_segments
from native_bspline import cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];P=tuple(tuple(tuple(x/2 for x in q)for q in row)for row in FULL);BASE=(U,V,3,2,P)
def along(S,var):
    ku,kv,p,q,net=S
    if var=='u':
        cols=[unclamp(ku,tuple(net[i][j]for i in range(6)),p)for j in range(5)];assert all(k==cols[0][0]for k,c in cols)
        return(cols[0][0],kv,p,q,tuple(tuple(cols[j][1][i]for j in range(5))for i in range(6)))
    rows=[unclamp(kv,row,q)for row in net];assert all(k==rows[0][0]for k,c in rows)
    return(ku,rows[0][0],p,q,tuple(c for k,c in rows))
BU,CV=along(BASE,'u'),along(BASE,'v');BOTH=along(BU,'v');assert BOTH==along(CV,'u');CASES=(BASE,BU,CV,BOTH);identities=0
for S in CASES[1:]:
    for i in range(3,6):
        for j in range(2,5):
            a=local_patch(*BASE,i,j)[0];b=local_patch(*S,i,j)[0];assert a==b;identities+=12
nc=cross=0
for source,panels in[(9,[0]),(10,[1]),(11,[2,3])]:
    xmax=F(15,2)+17*(len(panels)-1);lines=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-7.5,-6.5) rectangle '+point((xmax,F(13,2)))+';']
    for local,j in enumerate(panels):
        S=CASES[j];net=S[4];lines.append(r'\begin{scope}[xshift='+str(17*local)+'cm]')
        for i in range(6):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(view(q))for q in net[i])+';')
        for k in range(5):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(view(net[i][k]))for i in range(6))+';')
        for row in net:
            for q in row:
                x,y=view(q);assert -F(15,2)<x<F(15,2)and-F(13,2)<y<F(13,2);lines.append(r'\fill '+point((x,y))+' circle[radius=1.4pt];')
        for variable in('u','v'):
            for fixed in(F(0),F(1,3),F(2,3),F(1)):
                K,p,C=isocurve(*S,variable,fixed);ss,c=verified_segments(K,C,p,steps=4);nc+=c
                for t in(F(0),F(1,3),F(2,3),F(1)):
                    assert de_boor(K,C,p,t)==(surface(*S,t,fixed)if variable=='u'else surface(*S,fixed,t));cross+=1
                for s in ss:lines.append(cubic_path(dict(bern=tuple(view(q)for q in s['bern']))))
        origin=(-F(11,2),-F(51,10))
        for d,label,anchor in[((1,0,0),'x','below left'),((0,1,0),'y','below right'),((0,0,1),'z','above')]:lines.append(r'\draw[book grid,book axis] '+point(origin)+'--'+point(tuple(a+b for a,b in zip(origin,view(d))))+r' node['+anchor+r'=4pt] {$'+label+'$};')
        lines.extend([r'\node at (0,6) {'+(r'$U,V$',r'$\widehat U,V$',r'$U,\widehat V$',r'$\widehat U,\widehat V$')[j]+'};',r'\node at (0,-6.1) {('+chr(97+j)+')};',r'\end{scope}'])
    lines.append(r'\end{tikzpicture}');(root/f'image_tex/ch12/fig_12_{source:02d}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-unclamping-check.json').write_text(json.dumps(dict(original_degrees=(3,2),cases=[dict(knots=(s[0],s[1]),controls=s[4])for s in CASES],exact_whole_tensor_vector_coefficient_identities=identities,UV_VU_commute_exactly=True,native_checks=nc,tensor_isocurve_checks=cross,unchanged_domain=((0,1),(0,1)),no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS A12.1tensoru/v/both,324wholevectorBeziercoefficients; UV==VUexact; samewholeS;',nc,'native',cross,'tensor checks')
