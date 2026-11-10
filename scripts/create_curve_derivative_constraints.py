from pathlib import Path
from fractions import Fraction as F
import json
from curve_constraint_data import U,P,row,constrained
from native_bspline import segments,check,cubic_path,point,de_boor
ROOT=Path(__file__).resolve().parents[1];u=F(139,250)
r=row(u,1);D=tuple(sum(r[i]*P[i][d] for i in range(8)) for d in range(2));zero=(F(0),F(0))
cases=[]
for free,factor,fixed in [((3,4,5),F(8,5),False),((4,),F(8,5),False),((3,4),F(3,5),True)]:
    cons=[(u,1,tuple((factor-1)*x for x in D))]
    if fixed:cons.insert(0,(u,0,zero))
    Q,proof=constrained(free,cons);proof['derivative_factor']=factor
    old=de_boor(U,P,3,u);new=de_boor(U,Q,3,u)
    assert (new==old) if fixed else (new!=old)
    cases.append((Q,proof))
nc=0
for source,ids in [(43,[0]),(44,[1,2])]:
    xmax=F(39,50) if len(ids)==1 else F(171,100)
    lines=[r'\begin{tikzpicture}[book line,x=20cm,y=20cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-.1,-.09) rectangle '+point((xmax,F(23,50)))+';']
    for local,j in enumerate(ids):
        Q,proof=cases[j];old=de_boor(U,P,3,u);new=de_boor(U,Q,3,u)
        lines.append(r'\begin{scope}[shift={'+point((F(local)*F(93,100),0))+'}]')
        for ctrl,style in [(P,'book grid'),(Q,'book grid,dashed')]:
            lines.append(r'\draw['+style+'] '+'--'.join(point(q) for q in ctrl)+';')
            for q in ctrl:lines.append(r'\draw[book grid] '+point(q)+' circle[radius=1.6pt];')
            ss=segments(U,ctrl,3);nc+=check(U,ctrl,3,ss,steps=9)
            lines.extend(cubic_path(s,'book line'+(',dashed' if ctrl==Q else '')) for s in ss)
        for pt,v,style,label,anchor in [(old,D,'book grid,book axis','D','above right=4pt'),(new,tuple(proof['derivative_factor']*x for x in D),'book grid,book axis,dashed',r'\widehat D','below right=7pt')]:
            end=tuple(a+b/4 for a,b in zip(pt,v));lines.append(r'\draw['+style+'] '+point(pt)+'--'+point(end)+r' node['+anchor+r'] {$'+label+'$};')
            lines.append(r'\draw[book grid] '+point(pt)+r' node[rectangle,draw,inner sep=1.5pt] {};')
        for i in proof['free']:
            lines.append(r'\node[above=8pt] at '+point(P[i])+r' {$P_'+str(i)+'$};')
            anchor='above right=12pt' if j==0 and i==4 else ('above left=12pt'if i==4 else 'below left=10pt')
            lines.append(r'\node['+anchor+'] at '+point(Q[i])+r' {$\widehat P_'+str(i)+'$};')
        lines.append(r'\node at (.28,-.065) {('+chr(97+j)+')};');lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}');(ROOT/f'image_tex/ch11/fig_11_{source}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(ROOT/'image_tex/build/curve-derivative-constraints-check.json').write_text(json.dumps(dict(knots=U,controls=P,u=u,original_derivative=D,cases=[r for _,r in cases],native_checks=nc,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8')
print('PASS exact derivative multiples8/5,8/5,3/5; position fixed onlyC; minimum norm certificates; nativechecks',nc)
