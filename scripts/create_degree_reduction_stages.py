"""Fig5.39: real quartic reduction errors and real inverse-insertion errors."""
from pathlib import Path
from fractions import Fraction as F
from math import sqrt,ceil
import json
from native_bspline import segments,check,cubic_path,point,de_boor,number
from native_polynomial_drawing import paths
from rational_geometry import elevate,evaluate,split
from degree_reduction_geometry import reduce_bezier
from inverse_knot_projection import remove_to
from knot51_data import insert

root=Path(__file__).resolve().parents[1]
U=(F(0),)*5+(F('.3'),)*2+(F('.7'),)*2+(F(1),)*5
P=tuple(tuple(F(str(t)) for t in pt) for pt in [(3,0),(.6,1.2),(0,3.8),(1.4,6.7),(5,8),(8.6,6.7),(10,3.8),(9.4,1.2),(7,0)])
old=segments(U,P,4);checks=check(U,P,4,old);B=[s['bern'] for s in old]
reduced=[];reduction_proofs=[]
for b in B:
    q,proof=reduce_bezier(b);reduced.append(q);reduction_proofs.append(proof)
K,Q=U,P
for j in range(2):K,Q,_=insert(K,Q,4,F('.3'))
first=Q
for j in range(2):K,Q,_=insert(K,Q,4,F('.7'))
assert Q==B[0]+B[1][1:]+B[2][1:]
two=reduced[0]+reduced[1][1:]
K2=(F(0),)*4+(F('.3'),)*3+(F('.7'),)*4
Kf,Qf,first_remove=remove_to(K2,two,3,[F('.3')]);assert first_remove['curve_exactly_unchanged']
Kf,Qf,second_remove=remove_to(Kf,Qf,3,[F('.3')]);assert not second_remove['curve_exactly_unchanged']
Qg=Qf+reduced[2][1:];Kg=Kf[:-4]+(F('.7'),)*3+(F(1),)*4
Kh,Qh,third_remove=remove_to(Kg,Qg,3,[F('.7')]);assert third_remove['curve_exactly_unchanged']
Kh,Qh,fourth_remove=remove_to(Kh,Qh,3,[F('.7')]);assert not fourth_remove['curve_exactly_unchanged']
assert Kh==(F(0),)*4+(F('.3'),F('.7'))+(F(1),)*4
controls=[P,first,reduced[0]+first[5:],reduced[0]+Q[5:],
          two+B[2][1:],Qf+B[2][1:],Qg,Qh]
assert list(map(len,controls))==[9,11,10,12,11,9,8,6]
single=lambda i:dict(a=old[i]['a'],b=old[i]['b'],bern=reduced[i])
approx=[[],[],[single(0)],[single(0)],[single(0),single(1)],
        segments(Kf,Qf,3),segments(Kg,Qg,3),segments(Kh,Qh,3)]
for k,q in [(Kf,Qf),(Kg,Qg),(Kh,Qh)]:checks+=check(k,q,3,segments(k,q,3))
residuals=[];bound=F(0);identity_points=0
for state in approx:
    ds=[]
    for s in state:
        ref=next(o for o in old if o['a']==s['a'] and o['b']==s['b'])
        elevated=elevate(s['bern']);D=tuple(tuple(a-b for a,b in zip(x,y)) for x,y in zip(ref['bern'],elevated))
        for i in range(81):
            t=F(i,80);u=s['a']+(s['b']-s['a'])*t
            assert tuple(a-b for a,b in zip(de_boor(U,P,4,u),evaluate(s['bern'],t)))==evaluate(D,t)
            identity_points+=1
        refined=[D]
        for j in range(3):refined=[half for d in refined for half in split(d)]
        whole=max(sum(map(abs,pt)) for d in refined for pt in d);bound=max(bound,whole)
        ds.append(dict(a=s['a'],b=s['b'],bern=D,certified_L1_bound=whole))
    residuals.append(ds)
axis_max=F(ceil(bound*10),10);scale=F(6,5)/axis_max
base_paths,render_certificate=paths(old);chart_tolerance=F(1,100)
chart_reports=[]
for pair in range(4):
    target=root/f'image_tex/ch05/fig_5_{57+pair}.tex';assert not target.exists()
    lines=['% Actual mathematical reduction and knot-removal stages; common Euclidean-error scale.',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-1.2,-4.3) rectangle (24.8,8.6);']
    for col in range(2):
        j=2*pair+col;lines.append(r'\begin{scope}[xshift='+str(13.4*col)+'cm]')
        lines.append(r'\draw[book grid] '+'--'.join(map(point,controls[j]))+';')
        lines+=base_paths
        for s in approx[j]:lines.append(cubic_path(s,'book line,dashed'))
        for pt in controls[j]:lines.append(r'\draw '+point(pt)+r' circle[radius=1.6pt];')
        for t in (F('.3'),F('.7')):
            x,y=de_boor(U,P,4,t);d=F(7,100)
            lines.append(r'\draw '+point((x-d,y))+'--'+point((x+d,y))+' '+point((x,y-d))+'--'+point((x,y+d))+';')
        y0=F(-5,2)
        lines += [r'\draw[book axis] (0,-2.5)--(10.7,-2.5) node[right=3pt] {$u$};',
                  r'\draw[book axis] (0,-2.5)--(0,-.8) node[above=3pt] {$E$};',
                  r'\draw[book grid] (-.08,-1.3)--(.08,-1.3);',
                  r'\node[left=4pt] at (0,-1.3) {$'+number(axis_max)+'$};']
        for t,label in [(F(0),'0'),(F('.3'),r'u_1'),(F('.7'),r'u_2'),(F(1),'1')]:
            x=10*t;lines.append(r'\draw[book grid] '+point((x,y0-F('.07')))+'--'+point((x,y0+F('.07')))+';')
            lines.append(r'\node[below=4pt] at '+point((x,y0))+' {$'+label+'$};')
        certificates=[]
        for d in residuals[j]:
            D=d['bern'];L=max(sum(abs(4*(b-a)) for a,b in zip(x,y)) for x,y in zip(D,D[1:]))
            n=max(80,ceil(L*scale/(2*chart_tolerance)))
            coords=[]
            for i in range(n+1):
                t=F(i,n);u=d['a']+(d['b']-d['a'])*t;v=evaluate(D,t)
                e=sqrt(sum(float(x)**2 for x in v));assert e<=float(axis_max)+1e-12
                coords.append(point((10*u,y0+F(str(e))*scale)))
            lines.append(r'\draw[book line] '+'--'.join(coords)+';')
            certificates.append({'span':[str(d['a']),str(d['b'])],'segments':n,
                                 'local_error_norm_Lipschitz_bound':str(L),
                                 'display_linear_interpolation_error_cm':str(L*scale/(2*n)),
                                 'exact_error_Bernstein_controls':[[str(x) for x in pt] for pt in D],
                                 'whole_span_L1_bound':str(d['certified_L1_bound'])})
        chart_reports.append(certificates)
        lines.append(r'\node at (5,-3.8) {('+chr(97+j)+r') $N='+str(len(controls[j]))+'$};')
        lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/degree-reduction-stages-check.json').write_text(json.dumps({
    'figure':'5.39','original_U':list(map(str,U)),'representative_original_controls':[[str(x) for x in pt] for pt in P],
    'state_control_counts':list(map(len,controls)),'final_knots':list(map(str,Kh)),
    'final_controls':[[str(x) for x in pt] for pt in Qh],'Bezier_reduction_proofs':reduction_proofs,
    'removal_proofs':[first_remove,second_remove,third_remove,fourth_remove],
    'native_checks':checks,'exact_error_polynomial_identity_points':identity_points,
    'original_native_render_certificate':render_certificate,'common_error_axis_max':str(axis_max),
    'error_graphs_are_actual_Euclidean_parameter_errors':True,'certified_error_graphs':chart_reports,
    'removal_method':'local rational least-squares inverse insertion, unaffected controls fixed; representative not recovered source data'},indent=2)+'\n')
print(f'PASS:{checks} native checks,{identity_points} exact error identities; real nonzero reduction/removal errors, chart interpolation<={float(chart_tolerance)}cm.')
