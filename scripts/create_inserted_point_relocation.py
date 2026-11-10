"""Printed11.4: actual Boehm insertion, then exact point-constrained relocation."""
from pathlib import Path
from fractions import Fraction as F
import json
from point_relocation_example_data import U,P,relocate
from knot51_data import insert
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'));assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch11/fig_11_04.tex')['applied'];t=F(43,100);uhat=3*t-U[5]-U[6];assert uhat==F(11,25)
K,Q,alpha=insert(U,P,3,uhat);assert sum(K[5:8])/3==t
before=segments(U,P,3);after=segments(K,Q,3);identities=0
for s in after:
    old=next(a for a in before if a['a']<=s['a'] and s['b']<=a['b']);assert old['power']==s['power'];identities+=8
R,r=relocate(K,Q,4,t);assert de_boor(U,P,3,t)==r['selected_point'];r.update(inserted_knot=uhat,original_knots=U,original_controls=P,whole_insertion_power_coefficient_identities=identities,old_support=(U[3],U[7]),new_support=(K[4],K[8]),new_greville=t)
out=['% Actual Boehm insertion and subsequent constrained movement; shared curve from11.2/11.3.',r'\begin{tikzpicture}[book line,x=2cm,y=2cm]',r'\path[use as bounding box] (-.7,-.8) rectangle (8.7,3.8);'];nc=lines=0
out.append(r'\draw[book grid] '+'--'.join(point(a) for a in P)+';');out.append(r'\draw[book grid] '+'--'.join(point(a) for a in Q)+';');out.append(r'\draw[book grid,dashed] '+point(Q[3])+'--'+point(R[4])+'--'+point(Q[5])+';')
for v in (K[4]+(K[8]-K[4])*F(i,36) for i in range(1,36)):
    a,b=de_boor(K,Q,3,v),de_boor(K,R,3,v)
    if sum((x-y)**2 for x,y in zip(a,b))<F(1,10000):continue
    assert (b[0]-a[0])*r['unit_direction'][1]==(b[1]-a[1])*r['unit_direction'][0]
    out.append(r'\draw[book grid] '+point(a)+'--'+point(b)+';');lines+=1
for C,style in [(Q,''),(R,'dashed')]:
    ss=segments(K,C,3);nc+=check(K,C,3,ss,steps=7);out.extend(cubic_path(s,style) for s in ss)
for a in P:out.append(r'\draw '+point(a)+r' circle[radius=1.3pt];')
for i in (3,5):out.append(r'\draw '+point(Q[i])+r' circle[radius=1.5pt];')
for pos,label,anchor in [(P[3],'P_3','above'),(P[4],'P_4','above left'),(Q[3],'Q_3','left'),(Q[5],'Q_5','above right')]:out.append(r'\node['+anchor+r'=8pt] at '+point(pos)+r' {$'+label+'$};')
out.extend([r'\draw[book axis] '+point(Q[4])+'--'+point(R[4])+';',r'\draw '+point(R[4])+r' circle[radius=1.7pt] node[below=8pt] {$\widehat Q_4$};',r'\draw '+point(r['selected_point'])+r' circle[radius=2.1pt] node[above=16pt] {$P$};',r'\draw '+point(r['new_selected_point'])+r' circle[radius=2.1pt] node[right=24pt] {$\widehat P$};',r'\end{tikzpicture}'])
(root/'image_tex/ch11/fig_11_04.tex').write_text('\n'.join(out)+'\n',encoding='utf-8');r.update(native_curve_checks=nc,actual_parallel_displacement_segments=lines,no_contour_tracing=True,native_curve_error=0)
(root/'image_tex/build/inserted-point-relocation-check.json').write_text(json.dumps(r,default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.4:',identities,'insertionpoweridentities/',r['exact_whole_power_coefficient_identities'],'relocationpoweridentities;',nc,'nativechecks;newGreville.43/new_support.2..71;maximumratio',float(r['maximum_to_requested_ratio']))
