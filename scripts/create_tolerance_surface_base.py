"""Fig5.30: common9x8 net and sparse actual surface isoparametric lines."""
from pathlib import Path
from fractions import Fraction as F
import json
from knot530_data import U,V,R,S,P,BASE,CAMERA,PROJECTION,U_OPERATIONS,V_OPERATIONS
from surface_geometry import verify_tensor,isocurve,surface
from native_bspline import segments,check,cubic_path,point,de_boor

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_42.tex';assert not target.exists()
tensor=verify_tensor(*BASE,steps=20);curvechecks=points=0
uvalues=tuple(F(t) for t in ('0','.3','.7','1'));vvalues=tuple(F(t) for t in ('0','.42','.81','1'))
panels=[]
for index in (0,1):
    lines=[r'\begin{scope}['+CAMERA+']']
    if index==0:
        for row in P:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
        for j in range(8):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(row[j]) for row in P)+';')
        for row in P:
            for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius=1pt];')
    else:
        for variable,values in [('u',vvalues),('v',uvalues)]:
            for fixed in values:
                K,p,Q=isocurve(*BASE,variable,fixed);ss=segments(K,Q,p);curvechecks+=check(K,Q,p,ss)
                for i in range(21):
                    t=F(i,20);assert de_boor(K,Q,p,t)==(surface(*BASE,t,fixed) if variable=='u' else surface(*BASE,fixed,t));points+=1
                for s in ss:lines.append(cubic_path(s,'book line,dashed'))
    lines += [r'\draw[book axis] (0,0,0)--(5.5,0,0) node[below left=4pt] {$x$};',
              r'\draw[book axis] (0,0,0)--(0,6.2,0) node[right=4pt] {$y$};',
              r'\draw[book axis] (0,0,0)--(0,0,9.5) node[above=4pt] {$z$};',
              r'\end{scope}',r'\node at (.3,-4.65) {('+chr(97+index)+')};'];panels.append(lines)
lines=['% Fig5.30: one explicit representative9x8 p3q2 surface with the exact printed knots.',
       '% (a)control net,(b)sparse actual u/v isoparametric curves, all mathematical and editable.',
       '% SAME base data must be used for every tolerance comparison5.31-5.34.',
       '% Exact tangent slope separation certifies projection has no folds.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-5.6,-5.2) rectangle (19.4,7.3);']
for panel,shift in zip(panels,(0,13)):
    lines+=[r'\begin{scope}[xshift='+str(shift)+'cm]']+panel+[r'\end{scope}']
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/tolerance-surface-base-check.json').write_text(json.dumps({
    'figure':'5.30','degrees':[3,2],'control_count':[9,8],'all_unit_weights':True,
    'U':list(map(str,U)),'V':list(map(str,V)),
    'representative_u_curve':[[str(t) for t in pt] for pt in R],
    'representative_v_curve':[[str(t) for t in pt] for pt in S],
    'controls':[[list(map(str,t)) for t in row] for row in P],
    'representative_multiscale_u_operations':U_OPERATIONS,'representative_multiscale_v_operations':V_OPERATIONS,
    'projection_orientation':PROJECTION,'exact_tensor_vs_nested_deboor_points':tensor,
    'exact_native_isocurve_checks':curvechecks,'isocurve_vs_surface_points':points,
    'sparse_u_parameters':list(map(str,uvalues)),'sparse_v_parameters':list(map(str,vvalues)),
    'same_data_required_for531_through534':True},indent=2)+'\n')
print('PASS:441 exact tensor points,'+str(curvechecks)+' native isocurve checks,'+str(points)+' surface/isocurve points;9x8 net and sparse sheet share one verified projection.')
