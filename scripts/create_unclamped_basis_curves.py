from pathlib import Path
from fractions import Fraction as F
import json
from math import comb
from bspline_math import piece,evaluate,compose_affine,basis
from native_bspline import cubic_path,point,de_boor
from unclamped_geometry import verified_segments
root=Path(__file__).resolve().parents[1];K=tuple(F(i)for i in range(-3,6))
CASES=[(2,[(0,0),(1,F(9,5)),(F(11,5),F(12,5)),(F(17,5),F(3,2)),(4,0),(F(53,10),-F(3,10))]),(3,[(0,0),(F(3,5),F(11,5)),(F(14,5),F(11,5)),(F(17,5),0),(F(53,10),-F(3,10))])]
out=[r'\begin{tikzpicture}[book line,x=2cm,y=2cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-.5,-4.3) rectangle (15,3);'];nc=bc=0;reports=[]
for panel,(p,coords)in enumerate(CASES):
    P=tuple(tuple(F(x)for x in q)for q in coords);ss,n=verified_segments(K,P,p);nc+=n
    ends=(de_boor(K,P,p,K[p]),de_boor(K,P,p,K[len(P)]));assert ends[0]!=P[0]and ends[1]!=P[-1]
    out.append(r'\begin{scope}[shift={'+point((F(17,2)*panel,0))+'}]')
    out.append(r'\draw[book grid,dashed] '+'--'.join(point(q)for q in P)+';');out.extend(cubic_path(s)for s in ss)
    for i,q in enumerate(P):out.append(r'\draw[book grid] '+point(q)+r' circle[radius=1.6pt] node['+('below left=5pt'if i in(0,len(P)-2)else'above=5pt')+r'] {$P_'+str(i)+'$};')
    for u in range(int(K[p]),int(K[len(P)])+1):out.append(r'\draw[book grid] '+point(de_boor(K,P,p,F(u)))+r' node[rectangle,draw,inner sep=1.5pt] {};')
    def xy(u,n=0):return(F(3,4)*(u+3),F(3,2)*n-F(14,5))
    for i in range(len(P)):
        for s in range(i,i+p+1):
            a,b=K[s],K[s+1];c=piece(K,i,p,s)
            if not any(c):continue
            local=compose_affine(c,a,b-a)
            vals=[sum((local[k]if k<len(local)else 0)*F(comb(j,k),comb(p,k))for k in range(j+1))for j in range(p+1)]
            B=tuple(xy(a+(b-a)*F(j,p),v)for j,v in enumerate(vals));out.append(cubic_path(dict(bern=B),'book grid'))
            for j in range(7):
                t=F(j,7);u=a+(b-a)*t;q=list(vals)
                for _ in range(p):q=[(1-t)*x+t*y for x,y in zip(q,q[1:])]
                assert q[0]==evaluate(c,u)==basis(K,i,p,u);bc+=1
    out.append(r'\draw[book grid,book axis] '+point(xy(-F(7,2)))+'--'+point(xy(F(11,2)))+r' node[right=4pt] {$u$};')
    out.append(r'\draw[book grid,book axis] '+point(xy(0))+'--'+point(xy(0,F(6,5)))+';')
    for u in range(-3,6):
        x,y=xy(F(u));out.append(r'\draw[book grid] '+point((x,y-F(1,25)))+'--'+point((x,y+F(1,25)))+r' node[below=5pt] {$'+str(u)+'$};')
    for i in(0,len(P)-1):out.append(r'\node[above=5pt] at '+point(xy(K[i]+F(p+1,2),F(4,5)))+r' {$N_{'+str(i)+','+str(p)+'}$};')
    x1,x2=xy(K[p])[0],xy(K[len(P)])[0]
    out.append(r'\draw[book grid] '+point((x1,-F(18,5)))+'--'+point((x2,-F(18,5)))+r' node[midway,below=5pt] {$u\in['+str(int(K[p]))+','+str(int(K[len(P)]))+']$};')
    out.append(r'\node at (3,-4.1) {('+('a'if panel==0 else'b')+')};');out.append(r'\end{scope}')
    reports.append(dict(degree=p,controls=P,domain=(K[p],K[len(P)]),actual_endpoints=ends,endpoint_controls_distinct=True))
out.append(r'\end{tikzpicture}');(root/'image_tex/ch12/fig_12_01.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/unclamped-basis-curves-check.json').write_text(json.dumps(dict(knots=K,cases=reports,native_curve_checks=nc,full_support_basis_checks=bc,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS printedunclampedU; actualquadratic/cubic valid domains, noninterpolatingends;',nc,'native',bc,'basis checks')
