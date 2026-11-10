"""9.22:exact two-parabola construction for parallel/inflection tangents and isosceles case."""
from fractions import Fraction as F
from pathlib import Path
from math import degrees,atan2
import json
from native_bspline import segments,check,cubic_path,point
from bspline_math import derivative,evaluate
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (27,28):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex')['applied']
def add(A,B,t=F(1)):return tuple(a+t*b for a,b in zip(A,B))
def mix(A,B,t):return tuple((1-t)*a+t*b for a,b in zip(A,B))
def cross(A,B):return A[0]*B[1]-A[1]*B[0]
def paired(A,B,Ts,Te,gs,ge):
    assert sum(x*x for x in Ts)==sum(x*x for x in Te)==1 and gs>0 and ge>0
    Rs=add(A,Ts,gs);Re=add(B,Te,-ge);beta=gs/(gs+ge);J=mix(Rs,Re,beta)
    K=(F(0),)*3+(beta,beta)+(F(1),)*3;P=(A,Rs,J,Re,B);ss=segments(K,P,2);nc=check(K,P,2,ss)
    assert ss[0]['bern']==(A,Rs,J) and ss[1]['bern']==(J,Re,B)
    assert tuple(evaluate(derivative(c),beta) for c in ss[0]['power'])==tuple(evaluate(derivative(c),beta) for c in ss[1]['power'])
    return dict(A=A,B=B,Ts=Ts,Te=Te,gs=gs,ge=ge,Rs=Rs,Re=Re,J=J,beta=beta,ss=ss,native_checks=nc)
a=paired((F(0),F(0)),(F(6),F(0)),(F(3,5),F(4,5)),(-F(3,5),-F(4,5)),F(3),F(3))
assert a['J']==(F(24,5),F(12,5)) and cross(a['Ts'],a['Te'])==0
Ts=(F(12,13),F(5,13));Te=(F(4,5),-F(3,5));alpha=F(2,3);coss, cose=F(5,13),F(3,5)
gs=1/(alpha*cose+(1-alpha)*coss);ge=1/(alpha*coss+(1-alpha)*cose)
assert (gs,ge)==(F(195,103),F(195,89))
b=paired((F(3),F(3)),(F(3),-F(1)),Ts,Te,gs,ge)
assert b['J']==(F(25,8),F(103,48))
R=(F(-3,7),F(11,7))
assert add(b['A'],Ts,-F(26,7))==R==add(b['B'],Te,-F(30,7))
cs=(F(3,5),F(4,5));ce=(F(3,5),-F(4,5));gamma=F(6)/(4*F(3,5));assert gamma==F(5,2)
c=paired((F(0),F(0)),(F(6),F(0)),cs,ce,gamma,gamma)
apex=(F(3),F(4));assert c['Rs']==mix(c['A'],apex,F(1,2)) and c['Re']==mix(apex,c['B'],F(1,2))
assert c['J']==mix(c['Rs'],c['Re'],F(1,2))==(F(3),F(2))
reports=[]
def line(A,B,style='book grid'):return r'\draw['+style+'] '+point(A)+'--'+point(B)+';'
def marker(q,name,anchor):return [r'\draw '+point(q)+r' circle[radius=2.4pt];',r'\node['+anchor+r'=6pt] at '+point(q)+' {$'+name+'$};']
def panel(case,letter,shift=0):
    A,B,Rs,Re,J=(case[k] for k in ('A','B','Rs','Re','J'))
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-1.5,-2.2) rectangle (9,5.2);']
    if letter=='a':
        M=mix(A,B,F(1,2));out.extend([line(A,B,'book grid,dashed'),line(Rs,Re,'book grid,dashed'),line(M,J,'book grid,dashed'),line(B,Re,'book grid,dashed')])
        out+=marker(M,r'\mathbf M','below')
    elif letter=='b':
        out.extend([line(R,Rs,'book grid,dashed'),line(R,Re,'book grid,dashed'),line(Rs,Re,'book grid'),line(A,B,'book grid,dashed')])
        out+=marker(R,r'\mathbf R_k','left')
    else:
        M=(F(3),F(0));out.extend([line(A,apex),line(apex,B),line(A,B),line(apex,M),line(Rs,Re)])
        out+=marker(apex,r'\mathbf R_k','above');out+=marker(M,r'\mathbf M','below')
        theta=degrees(atan2(4,3));out.append(r'\draw[book grid] (.65,0) arc[start angle=0,end angle='+f'{theta:.12f}'+r',radius=.65];')
        out.append(r'\node at (.75,.3) {$\theta$};')
    out.extend(cubic_path(s) for s in case['ss'])
    if letter!='c':
        # Each visible arrow segment is exactly one UNIT tangent vector;the preceding line is a guide.
        out.append(line(A,Rs));out.append(line(Rs,add(Rs,case['Ts']),'book axis'))
        out.append(r'\node[above right=6pt] at '+point(add(Rs,case['Ts']))+r' {$\mathbf T_{k-1}$};')
        out.append(line(B,add(B,case['Te']),'book axis'))
        out.append(r'\node['+('above right' if letter=='b' else 'below right')+r'=6pt] at '+point(add(B,case['Te']))+r' {$\mathbf T_k$};')
    for q,name,anchor in [(A,r'\mathbf Q_{k-1}','below left' if letter!='b' else 'above left'),(B,r'\mathbf Q_k','right' if letter!='c' else 'below right'),(Rs,r'\mathbf R_k^{\prime}','left' if letter!='b' else 'above left'),(Re,r'\mathbf R_{k+1}^{\prime}','above' if letter=='a' else 'left' if letter=='b' else 'right'),(J,r'\mathbf Q_k^{\prime}','above' if letter=='a' else 'right' if letter=='b' else 'above right')]:
        out+=marker(q,name,anchor)
    out.extend([r'\node at (4,-1.7) {('+letter+')};',r'\end{scope}'])
    reports.append(dict(panel=letter,start=list(map(str,A)),end=list(map(str,B)),unit_tangents=[list(map(str,case['Ts'])),list(map(str,case['Te']))],gammas=[str(case['gs']),str(case['ge'])],new_controls=[list(map(str,Rs)),list(map(str,Re))],weighted_join=list(map(str,J)),C1_join_parameter=str(case['beta']),both_quadratic_Bezier_triples_exact=True,join_derivatives_equal_after_parameter_scaling=True,native_curve_checks=case['native_checks']))
    return out
header=['% Exact Eq9.41..44 constructions;unit tangent arrow segments have true common unit length.',r'\begin{tikzpicture}[book line,x=1.7cm,y=1.7cm]']
for n,lines in [(27,header+panel(a,'a')+[r'\end{tikzpicture}']),(28,header+panel(b,'b')+panel(c,'c',18.5)+[r'\end{tikzpicture}'])]:
    (root/f'image_tex/ch09/fig_9_{n:02}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/exceptional-quadratic-tangent-cases-check.json').write_text(json.dumps(dict(figure='9.22',representative_cases=reports,parallel_case_half_chord_gamma_exact=True,inflection_alpha=str(alpha),inflection_acute_line_angle_cosines=[str(coss),str(cose)],inflection_original_intersection=list(map(str,R)),inflection_original_intersection_coefficients=['-26/7','-30/7'],isosceles_apex=list(map(str,apex)),isosceles_gamma_formula_exact=True,isosceles_two_halves_equal_single_original_quadratic=True,all_arrow_segments_true_unit_tangents=True,common_coordinate_scale_cm='17/10'),indent=2)+'\n')
print('PASS:parallel/inflection Eq9.41..44 exact,newcontrols/weightedjoins,C1scaled derivatives,isosceles halfsubdivision/gamma;all tangent arrows true unit length.')
