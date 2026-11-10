"""Fig5.16: six-control cubic and two actual midpoint knot-refinement rounds."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor,number
from midpoint_refinement import refine,polygon_error_bound

root=Path(__file__).resolve().parents[1];targets=[root/f'image_tex/ch05/fig_5_{n}.tex' for n in (18,19)];assert not any(p.exists() for p in targets)
# Six controls, TWO interior ticks in original(a), 9 controls in(b), 15 in(c).
# The OCR caption omitted7/10; both raster panels independently confirm it.
U=(F(0),)*4+(F(3,10),F(7,10))+(F(1),)*4
P=tuple(tuple(F(str(c)) for c in pt) for pt in [(0,0),(3,.3),(1.5,4),(7.5,5.5),(5.5,.8),(9,0)])
states=[(U,P,())]
for _ in range(2):states.append(refine(*states[-1][:2],3))
assert [len(R) for K,R,_ in states]==[6,9,15]
assert states[1][2]==(F(3,20),F(1,2),F(17,20))
assert states[2][2]==(F(3,40),F(9,40),F(2,5),F(3,5),F(31,40),F(37,40))
old=segments(U,P,3);reports=[];paths=[];total=0;invariance=0;bounds=[]
for r,(K,R,newknots) in enumerate(states):
    ss=segments(K,R,3);total+=check(K,R,3,ss)
    for s in ss:
        t=next(t for t in old if t['a']<=s['a'] and s['b']<=t['b']);assert s['power']==t['power']
    for j in range(201):assert de_boor(K,R,3,F(j,200))==de_boor(U,P,3,F(j,200));invariance+=1
    error=polygon_error_bound(K,R,3,ss);bounds.append(error)
    panel=[r'\draw[book grid] '+'--'.join(map(point,R))+';']
    # Same original mathematical curve in each view, without changing its parametrization.
    for seg in old:panel.append(cubic_path(seg))
    for pt in R:panel.append(r'\draw '+point(pt)+' circle[radius=1.6pt];')
    panel.append(r'\draw[book grid] (0,-1.1)--(9,-1.1);')
    for t in sorted(set(K)):
        for j in range(K.count(t)):
            x=9*t+F(1,20)*(F(j)-F(K.count(t)-1,2))
            panel.append(r'\draw[book grid] '+point((x,F(-6,5)))+'--'+point((x,F(-1)))+';')
        if t in U:panel.append(r'\node[below=5pt] at '+point((9*t,F(-11,10)))+' {$'+number(t)+'$};')
        else:panel.append(r'\draw[book axis] '+point((9*t,F(-3,5)))+'--'+point((9*t,F(-49,50)))+';')
    panel.append(r'\node at (4.5,-2) {('+chr(97+r)+')};');paths.append(panel)
    reports.append({'round':r,'knots':list(map(str,K)),'controls':[[str(c) for c in pt] for pt in R],'new_midpoint_knots':list(map(str,newknots)),'unchanged_polynomial_spans':len(ss),'greville_polygon_parametric_L1_error_bound_cm':str(error)})
assert bounds[0]>bounds[1]>bounds[2]>0
for index,target in enumerate(targets):
    panels=(0,1) if index==0 else (2,)
    lines=['% Fig5.16: actual midpoint knot refinements, native exact cubic geometry.',
           '% Original SIX controls require TWO interior knots3/10,7/10; OCR caption omitted7/10.',
           '% Counts6,9,15 and both original knot bars confirm the restored knot vector.',
           '% Representative coordinates; every refined polynomial span identical to original.',
           r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
           r'\path[use as bounding box] (-.6,-2.5) rectangle ('+('22,6.3' if index==0 else '10,5')+');']
    for position,panel in enumerate(panels):
        lines.append(r'\begin{scope}[xshift='+str(position*12)+'cm]');lines+=paths[panel];lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/midpoint-curve-refinement-check.json').write_text(json.dumps({'figure':'5.16','degree':3,'representative_controls':True,'restored_OCR_omission':'interior knot7/10, confirmed by six/nine/fifteen control counts and two original interior knot ticks','native_curve_checks':total,'original_parameter_invariance_points':invariance,'certified_polygon_error_bounds_strictly_decrease':list(map(str,bounds)),'panels':reports},indent=2)+'\n')
print(f'PASS:6/9/15 controls,{total} exact native checks,{invariance} invariant points; certified polygon error bounds '+','.join(f'{float(e):.5f}' for e in bounds)+'cm.')
