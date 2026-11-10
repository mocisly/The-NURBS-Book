from pathlib import Path
import json
from fractions import Fraction as F
from curve_constraint_data import U,P,POSITION_CASES
from native_bspline import segments,check,cubic_path,point,de_boor
ROOT=Path(__file__).resolve().parents[1]
nc=0
for source,panels in [(41,[(0,'a',P,None),(1,'b',*POSITION_CASES[0])]),(42,[(2,'c',*POSITION_CASES[1]),(3,'d',*POSITION_CASES[2])])]:
    lines=[r'\begin{tikzpicture}[book line,x=20cm,y=20cm,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] (-.06,-.09) rectangle (1.47,.44);']
    for local,(case,label,Q,proof) in enumerate(panels):
        lines.append(r'\begin{scope}[shift={'+point((F(local)*F(17,20),0))+'}]')
        lines.append(r'\draw[book grid] '+'--'.join(point(q) for q in P)+';')
        for q in P:lines.append(r'\draw[book grid] '+point(q)+' circle[radius=1.6pt];')
        ss=segments(U,P,3);nc+=check(U,P,3,ss,steps=9)
        lines.extend(cubic_path(s) for s in ss)
        old=de_boor(U,P,3,F(1,2));new=de_boor(U,Q,3,F(1,2))
        if proof:
            lines.append(r'\draw[book grid,dashed] '+'--'.join(point(q) for q in Q)+';')
            for i in proof['free']:lines.append(r'\draw[book grid] '+point(Q[i])+' circle[radius=1.6pt];')
            ss=segments(U,Q,3);nc+=check(U,Q,3,ss,steps=9);lines.extend(cubic_path(s,'book line,dashed') for s in ss)
            lines.append(r'\draw[book grid,book axis] '+point(old)+'--'+point(new)+';')
            for i in (3,4):
                lines.append(r'\node[above=7pt] at '+point(P[i])+r' {$P_'+str(i)+'$};')
                if i in proof['free']:
                    anchor='below left=7pt' if i==3 else 'above=7pt'
                    lines.append(r'\node['+anchor+'] at '+point(Q[i])+r' {$\widehat P_'+str(i)+'$};')
            lines.append(r'\node[below right=8pt] at '+point(new)+r' {$\widehat C(1/2)$};')
            lines.append(r'\draw[book grid] '+point(new)+r' node[rectangle,draw,inner sep=1.5pt] {};')
        else:
            lines.append(r'\node[below=10pt] at '+point(old)+r' {$C(1/2)$};')
        lines.append(r'\draw[book grid] '+point(old)+r' node[rectangle,draw,inner sep=1.5pt] {};')
        lines.append(r'\node at (.27,-.065) {('+label+')};')
        lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}')
    (ROOT/f'image_tex/ch11/fig_11_{source}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(ROOT/'image_tex/build/curve-position-constraints-check.json').write_text(json.dumps(dict(knots=U,original_controls=P,cases=[r for _,r in POSITION_CASES],native_checks=nc,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8')
print('PASS exact printed point displacement in all3systems; minimum norm certificates; nativechecks',nc)
