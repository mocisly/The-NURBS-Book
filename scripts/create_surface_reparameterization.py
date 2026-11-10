"""6.14: exact rational tensor reparameterization and equal-new-parameter isocurves."""
from pathlib import Path
from fractions import Fraction as F
import json
from knot59_data import U,V,P
from surface_geometry import surface,isocurve,verify_tensor
from native_bspline import segments,check,cubic_path,point
from rational_geometry import project
from mobius_reparameterization import transform

root=Path(__file__).resolve().parents[1];data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for name in ('fig_6_16.tex','fig_6_17.tex','fig_6_18.tex'):
    assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/'+name)['applied']
H=tuple(tuple(pt+(F(1),) for pt in row) for row in P)
g=lambda u:(2*u+1)/(3*u+2)
inverse=lambda s:(1-2*s)/(3*s-2)
panels=[];reports=[]
for letter,um,vm in [('a',False,False),('b',True,False),('c',False,True),('d',True,True)]:
    K,L,Q=U,V,H;transform_checks=0
    if um:
        columns=[]
        for j in range(4):
            K,col,_,_,proof=transform(U,tuple(row[j] for row in Q),3,(2,1,3,2));columns.append(col)
            transform_checks+=proof['exact_parameter_and_projected_curve_checks']
        Q=tuple(tuple(col[i] for col in columns) for i in range(4))
    if vm:
        rows=[]
        for row in Q:
            L,pts,_,_,proof=transform(V,row,2,(2,1,3,2));rows.append(pts)
            transform_checks+=proof['exact_parameter_and_projected_curve_checks']
        Q=tuple(rows)
    assert all(project(Q[i][j])==P[i][j] for i in range(4) for j in range(4))
    tensor_checks=verify_tensor(K,L,3,2,Q,steps=10)
    for i in range(11):
        for j in range(11):
            u,v=F(i,10),F(j,10);s,t=g(u) if um else u,g(v) if vm else v
            assert project(surface(K,L,3,2,Q,s,t))==surface(U,V,3,2,P,u,v)
    lines=[r'\begin{scope}[x={(-.81cm,-.54cm)},y={(.9cm,-.315cm)},z={(0cm,1.5cm)}]']
    native=0;fixed_values={}
    for fixed_axis,mapped in [('u',um),('v',vm)]:
        # A parameter change along a complete isocurve leaves its locus unchanged.
        # Compute the fixed ORIGINAL parameter by exact inversion of an equal-step
        # NEW parameter. The resulting old isocurve is polynomial and drawn exactly.
        values=[]
        for i in range(11):
            value=F(1,2)+F(i,100) if mapped else F(i,10)
            fixed=inverse(value) if mapped else value;values.append(fixed)
            varying='v' if fixed_axis=='u' else 'u'
            knots,p,C=isocurve(U,V,3,2,P,varying,fixed);ss=segments(knots,C,p);native+=check(knots,C,p,ss)
            style='book line' if i in (0,10) else 'book grid'
            lines.extend(cubic_path(s,style) for s in ss)
        fixed_values[fixed_axis]=list(map(str,values))
    lines += [r'\draw[book axis] (0,0,0)--(5.5,0,0) node[below left=4pt] {$x$};',
              r'\draw[book axis] (0,0,0)--(0,6.3,0) node[right=4pt] {$y$};',
              r'\draw[book axis] (0,0,0)--(0,0,4.8) node[above=4pt] {$z$};',
              r'\end{scope}',r'\node at (0,-5.25) {('+letter+')};']
    panels.append(lines)
    reports.append({'panel':letter,'u_reparameterized':um,'v_reparameterized':vm,
                    'new_u_knots':list(map(str,K)),'new_v_knots':list(map(str,L)),
                    'new_weights':[[str(pt[-1]) for pt in row] for row in Q],
                    'exact_control_point_invariance':True,'exact_tensor_projection_identities':121,
                    'native_tensor_checks':tensor_checks,'native_isocurve_checks':native,
                    'exact_curve_transform_checks':transform_checks,
                    'original_parameters_of_equal_new_parameter_isocurves':fixed_values})
    print(f'Panel{letter}:{tensor_checks}tensor+{native}native isocurve checks,121exact invariant surface points.',flush=True)
for group,name in [(panels[:2],'fig_6_16.tex'),(panels[2:3],'fig_6_17.tex'),(panels[3:],'fig_6_18.tex')]:
    right='19.6' if len(group)==2 else '6.6'
    lines=['% Same explicit representative3x2 surface as5.9; exact given Mobius mappings.',
           '% Equal NEW parameter values inverted exactly before drawing polynomial isocurves.',
           '% All transformed rational tensor controls/weights independently checked; no hatching trace.',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-5.3,-5.8) rectangle ('+right+',8.3);']
    for j,panel in enumerate(group):
        lines.append(r'\begin{scope}[xshift='+str(13*j)+'cm]');lines.extend(panel);lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}');(root/'image_tex/ch06'/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-reparameterization-check.json').write_text(json.dumps({
    'figure':'6.14','source_control_net':[[list(map(str,pt)) for pt in row] for row in P],
    'source_degrees':[3,2],'source_knots':[list(map(str,U)),list(map(str,V))],
    'mapping':'(2u+1)/(3u+2)','panels':reports},indent=2)+'\n')
print('PASS:four invariant surface geometries; correctly redistributed equal-new-parameter grids.')
