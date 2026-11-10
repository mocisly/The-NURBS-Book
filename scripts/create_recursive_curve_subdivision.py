"""Fig5.7: exact recursive subdivision with clamped child knot vectors."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from knot51_data import insert

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_08.tex';assert not target.exists()
K=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
P=tuple(tuple(F(str(c)) for c in pt) for pt in [(-5,0),(-2.5,0),(-1.5,2),(0,3),(1.5,2),(2.5,0),(5,0)])
def split(U,R,u):
    while U.count(u)<3:U,R,_=insert(U,R,3,u)
    last=max(i for i,a in enumerate(U) if a==u);shared=last-3
    left=(tuple(a for a in U if a<=u)+(u,),R[:shared+1])
    right=((u,)+tuple(a for a in U if a>=u),R[shared:])
    assert left[1][-1]==right[1][0]==de_boor(U,R,3,u)
    for knots,controls in (left,right):assert len(knots)==len(controls)+4
    return left,right
C1,C2=split(K,P,F(1,2));C11,C12=split(*C1,F(1,8));C21,C22=split(*C2,F(7,8))
cases=[('C',K,P,(F(0),F(9))),('C_1',*C1,(F(-3,5),F(24,5))),('C_2',*C2,(F(3,5),F(24,5))),
       ('C_{1,1}',*C11,(F(-6,5),F(-3,10))),('C_{1,2}',*C12,(F(-3,5),F(11,10))),
       ('C_{2,1}',*C21,(F(3,5),F(11,10))),('C_{2,2}',*C22,(F(6,5),F(-3,10)))]
original=segments(K,P,3);exact=0;invariance=0;reports=[]
lines=['% Fig5.7: specified cubic knot vector, representative symmetric7-point control polygon.',
       '% Exact knot-insertion splits at GLOBAL parameters1/2,1/8,7/8.',
       '% Each child has a genuine clamped knot vector and unchanged original parameterization.',
       '% Diagram translations separate the levels only; no curve scaling or contour tracing.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',r'\path[use as bounding box] (-7,-1.1) rectangle (7,13.3);']
for label,U,R,offset in cases:
    ss=segments(U,R,3);exact+=check(U,R,3,ss)
    for s in ss:
        parent=next(t for t in original if t['a']<=s['a'] and s['b']<=t['b']);assert s['power']==parent['power']
    for j in range(101):
        u=U[3]+(U[len(R)]-U[3])*F(j,100);assert de_boor(U,R,3,u)==de_boor(K,P,3,u);invariance+=1
    lines.append(r'\begin{scope}[shift={'+point(offset)+'}]')
    lines.append(r'\draw[book grid] '+'--'.join(map(point,R))+';')
    for s in ss:lines.append(cubic_path(s))
    for pt in R:lines.append(r'\draw '+point(pt)+' circle[radius=1.5pt];')
    lines.append(r'\end{scope}')
    reports.append({'name':label,'global_domain':list(map(str,(U[3],U[len(R)]))),'knots':list(map(str,U)),'controls':[[str(c) for c in p] for p in R],'display_translation':list(map(str,offset)),'same_polynomial_spans_as_original':len(ss)})
for label,pos in [('C',(0,F(25,2))),('C_1',(-3,F(79,10))),('C_2',(3,F(79,10))),('C_{1,1}',(-5,F(13,10))),('C_{1,2}',(-2,F(17,4))),('C_{2,1}',(2,F(17,4))),('C_{2,2}',(5,F(13,10)))]:
    lines.append(r'\node at '+point(pos)+r' {$\mathbf '+label+'$};')
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/recursive-curve-subdivision-check.json').write_text(json.dumps({'figure':'5.7','representative_controls':[[str(c) for c in p] for p in P],'original_knots':list(map(str,K)),'global_split_parameters':['1/2','1/8','7/8'],'native_span_checks':exact,'child_vs_original_deboor_points':invariance,'children':reports,'source_text_ambiguity':'OCR prose says3/8 for right branch, which is outside[1/2,1]; reconstruction explicitly uses7/8 in original global parameter domain.'},indent=2)+'\n')
print(f'PASS:7 clamped curves,{exact} exact native span checks,{invariance} original-parameter invariance points; six child-domain restrictions.')
