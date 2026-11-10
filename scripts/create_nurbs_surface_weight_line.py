"""Fig4.12: three actual rational surfaces and exact collinear fixed-parameter marks."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from rational_geometry import approximate,project
from surface_geometry import isocurve
from nurbs412_data import K,P,TARGET,CAMERA_NORM,homogeneous,rational,factor,verify

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch04/fig_4_14.tex';assert not target.exists()
family=(F(0),F(1),F(6));u0,v0=F(3,5),F(1,2)
marks=[rational(u0,v0,w) for w in family]
reports=[verify(w) for w in family]
lines=['% Fig4.12: representative5x5 bicubic dome, raised P22, all other weights1.',
       '% K=(0,0,0,0,1/2,1,1,1,1), fixed(u,v)=(3/5,1/2); w22=0,1,6.',
       '% Actual untranslated controls; S=C(w22=0), M=C(1), S22=C(6) lie exactly on the line to P22.',
       '% Curves computed from homogeneous tensor basis; certified native cubic paths, no image contours.',
       r'\begin{tikzpicture}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)},book line]',
       r'\path[use as bounding box] (canvas cs:x=-6.9cm,y=-4.6cm) rectangle (canvas cs:x=8.1cm,y=6.2cm);',
       r'\draw[book axis] (0,0,0)--(5,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis] (0,0,0)--(0,7,0) node[right=4pt] {$y$};',
       r'\draw[book axis] (0,0,0)--(0,0,5.6) node[above=4pt] {$z$};']
for row in P:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
for j in range(5):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(P[i][j]) for i in range(5))+';')
lines.append(r'\draw[book grid,dashed] '+point(marks[0])+'--'+point(TARGET)+';')
exact=points=paths=0;maximum=F(0)
for w in family:
    H=homogeneous(w)
    for var in ('u','v'):
        for t in (F(0),v0 if var=='u' else u0,F(1)):
            if t in (0,1) and w!=0:continue # all three boundary curves coincide exactly
            k,d,c=isocurve(K,K,3,3,H,var,t);ss=segments(k,c,d);exact+=check(k,c,d,ss)
            if t==(v0 if var=='u' else u0):
                assert project(de_boor(k,c,d,u0 if var=='u' else v0))==marks[family.index(w)]
            for j in range(11):
                s=F(j,10);val=project(de_boor(k,c,d,s))
                assert val==(rational(s,t,w) if var=='u' else rational(t,s,w));points+=1
            for seg in ss:
                for a in approximate(seg['bern'],F(1,10000)/CAMERA_NORM):
                    lines.append(cubic_path(a,'book line' if t in (0,1) else 'book grid'))
                    paths+=1;maximum=max(maximum,a['certified_l1_error']*CAMERA_NORM)
for row in P:
    for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius=1.1pt];')
lines += [r'\draw '+point(TARGET)+' circle[radius=2.5pt];',
          r'\node[above right=6pt] at '+point(TARGET)+r' {$\mathbf P_{2,2}$};']
for pt,label,yy in [(marks[0],r'\mathbf S','1'),(marks[1],r'\mathbf M','2'),(marks[2],r'\mathbf S_{2,2}','3.2')]:
    lines += [r'\fill '+point(pt)+' circle[radius=1.6pt];',
              r'\draw[book grid] '+point(pt)+'--(canvas cs:x=6cm,y='+yy+'cm) node[right=4pt] {$'+label+'$};']
lines.append(r'\end{tikzpicture}')
prev=None;fixed=[];f=factor(u0,v0);B=marks[0]
for w in (F(0),F(1,10),F(1),F(6),F(20),F(100)):
    c=rational(u0,v0,w);alpha=w*f/(1-f+w*f)
    assert c==tuple((1-alpha)*B[d]+alpha*TARGET[d] for d in range(3))
    for i,j in ((0,1),(0,2),(1,2)):assert (c[i]-B[i])*(TARGET[j]-B[j])==(c[j]-B[j])*(TARGET[i]-B[i])
    distance=sum((c[d]-TARGET[d])**2 for d in range(3));assert prev is None or distance<prev;prev=distance
    fixed.append({'w22':str(w),'point':list(map(str,c)),'alpha':str(alpha)})
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/nurbs-surface-weight-line-check.json').write_text(json.dumps({
    'figure':'4.12','representative_controls':[[[str(v) for v in pt] for pt in row] for row in P],
    'degrees':[3,3],'knots':list(map(str,K)),'fixed_parameter':[str(u0),str(v0)],'surface_cases':reports,
    'exact_homogeneous_isocurve_checks':exact,'isocurve_vs_tensor_points':points,
    'native_cubic_paths':paths,'maximum_certified_projected_l1_error_cm':str(maximum),
    'fixed_parameter_collinearity_and_monotonicity':fixed,'common_boundary_curves_drawn_once':True,'only_selected_isocurves_through_fixed_parameter':True},indent=2)+'\n')
print(f'PASS:363 tensor/weight-line points,{exact} exact isocurve checks,{points} curve/tensor comparisons; six exact collinear/monotone marks,{paths} certified paths.')
