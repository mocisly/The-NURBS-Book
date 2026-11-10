"""7.25: exact de Casteljau subdivision and conic-weight normalization."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import json
from rational_geometry import split,project,evaluate,approximate
from native_bspline import point,cubic_path
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (30,31):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch07/fig_7_{n}.tex')['applied']
panels=[];reports=[]
for label,w in [('a',F(3,5)),('b',-F(1,3)),('c',F(0))]:
    P0=(F(3),F(0));P2=(-F(3),F(0));P1=(F(0),F(4)) if w else (F(1),F(3))
    H=(P0+(F(1),),tuple(w*x for x in P1)+(w,) if w else P1+(F(0),),P2+(F(1),))
    left,right=split(H);Q1=project(left[1]);R1=project(right[1]);S=project(left[-1]);ws=(1+w)/2
    assert left[-1]==right[0] and left[-1][-1]==left[1][-1]==right[1][-1]==ws
    assert S==tuple((x+y)/2 for x,y in zip(Q1,R1))
    if w:
        assert Q1==tuple((x+w*y)/(1+w) for x,y in zip(P0,P1));assert R1==tuple((x+w*y)/(1+w) for x,y in zip(P2,P1))
    else:assert Q1==tuple(x+y for x,y in zip(P0,P1)) and R1==tuple(x+y for x,y in zip(P2,P1))
    # Positive normalized shoulder weights: squared value is exact, root tightly enclosed.
    D=10**40;num=ws.numerator*D*D//ws.denominator;k=isqrt(num);lo,hi=F(k,D),F(k+1,D)
    assert lo*lo<=ws<=hi*hi;wn=(lo+hi)/2
    normalized_left=(P0+(F(1),),tuple(wn*x for x in Q1)+(wn,),S+(F(1),))
    normalized_right=(S+(F(1),),tuple(wn*x for x in R1)+(wn,),P2+(F(1),))
    assert left[0][-1]*left[-1][-1]/left[1][-1]**2==1/ws
    for i in range(101):
        t=F(i,100);assert evaluate(left,t)==evaluate(H,t/2) and evaluate(right,t)==evaluate(H,(1+t)/2)
        # Exact parameter relation for geometric weight normalization, with enclosed sqrt.
        for old,new,alpha in [(left,normalized_left,1/wn),(right,normalized_right,wn)]:
            q=project(evaluate(old,alpha*t/(1-t+alpha*t)));r=project(evaluate(new,t))
            assert sum(abs(x-y) for x,y in zip(q,r))<F(1,10**36)
    paths=approximate(left,F(1,200000))+approximate(right,F(1,200000))
    lower=-F(7,2) if label!='c' else -F(6,5)
    lines=[r'\begin{scope}[x=1.4cm,y=1.4cm]',r'\path[use as bounding box] '+point((-F(57,10),lower))+' rectangle (5.7,4.9);']
    if w:lines += [r'\draw[book grid,dashed] '+point(P0)+'--'+point(P1)+'--'+point(P2)+';']
    lines += [r'\draw[book grid] '+'--'.join(map(point,(P0,Q1,S,R1,P2)))+';']
    if not w:
        lines += [r'\draw[book axis,book grid] '+point(P0)+'--'+point(Q1)+';',r'\draw[book axis,book grid] '+point(P2)+'--'+point(R1)+';',
                  r'\node[right=7pt] at (3.5,1.5) {$\overrightarrow{\mathbf P}_1$};']
    lines.extend(cubic_path(s) for s in paths)
    ends=('above right','above left') if w<0 else ('below right','below left')
    controls=[(P0,r'\mathbf P_0=\mathbf Q_0',ends[0]),(P2,r'\mathbf P_2=\mathbf R_2',ends[1]),
              (Q1,r'\mathbf Q_1','below right' if w<0 else 'above right'),(R1,r'\mathbf R_1','below left' if w<0 else 'above left')]
    if w:controls.append((P1,r'\mathbf P_1','above'))
    for q,text,anchor in controls:lines.append(r'\draw '+point(q)+r' circle[radius=2pt] node['+anchor+r'=7pt] {$'+text+'$};')
    lines += [r'\draw '+point(S)+r' circle[radius=2pt];',r'\node['+('below' if w<0 else 'above')+r'=8pt] at '+point(S)+r' {$\mathbf Q_2=\mathbf R_0$};',
              r'\node['+('above' if w<0 else 'below')+r'=8pt] at '+point(S)+r' {$\mathbf S$};',
              r'\node at '+point((F(0),lower+F(1,4)))+' {('+label+')};',r'\end{scope}']
    panels.append(lines);reports.append({'panel':label,'original_homogeneous_controls':[[str(x) for x in h] for h in H],'Q1':list(map(str,Q1)),'R1':list(map(str,R1)),'S':list(map(str,S)),'subdivision_weight':str(ws),'normalized_middle_weight_squared':str(ws),'normalized_weight_enclosure':list(map(str,(lo,hi))),'exact_homogeneous_split_checks_each_half':101,'normalized_parameter_correspondence_L1_bound':'1e-36','native_L1_error':str(max(s['certified_l1_error'] for s in paths))})
for n,lines in [(30,panels[0]+[r'\begin{scope}[xshift=18cm]']+panels[1]+[r'\end{scope}']),(31,panels[2])]:
    (root/f'image_tex/ch07/fig_7_{n}.tex').write_text('% Exact de Casteljau split and positive conic normalization; representative controls.\n'+r'\begin{tikzpicture}[book line]'+'\n'+'\n'.join(lines)+'\n'+r'\end{tikzpicture}'+'\n',encoding='utf-8')
(root/'image_tex/build/split-conics-check.json').write_text(json.dumps({'figure':'7.25','panels':reports,'all_formulas7_42_to7_50_verified':True},indent=2)+'\n')
print('PASS:three exact homogeneous splits,606half evaluations,normalized conic shapes<1e-36,formulas7.42-7.50 verified.')
