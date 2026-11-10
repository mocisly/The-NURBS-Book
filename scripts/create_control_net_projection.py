"""Fig6.3: actual control-edge samples projected onto one nonlinear surface."""
from pathlib import Path
from fractions import Fraction as F
import json
from projection_surface_data import BASE,P,ZETA,MU,L,FY_SECOND_BOUND,CAMERA,graph,project,partials
from surface_geometry import verify_tensor,surface,isocurve
from native_bspline import segments,check,cubic_path,point

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch06/fig_6_03.tex'
manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch06/fig_6_03.tex')['applied']
tensor=verify_tensor(*BASE,steps=10);checks=0;graph_error=0.
for i in range(11):
    for j in range(11):
        S=surface(*BASE,F(i,10),F(j,10));z,*_=graph(float(S[0]),float(S[1]));graph_error=max(graph_error,abs(z-float(S[2])))
assert graph_error<3e-14
samples=set(pt for row in P for pt in row)
edges=[]
for row in P:edges+=list(zip(row,row[1:]))
for j in range(4):edges+=list(zip([row[j] for row in P],[row[j] for row in P[1:]]))
assert len(edges)==24
for A,B in edges:
    for i in range(1,8):samples.add(tuple((1-F(i,8))*x+F(i,8)*y for x,y in zip(A,B)))
assert len(samples)==184
projections=[];maximum_residual=0.;maximum_surface_error=0.;maximum_tangent_dot=0.
for source in sorted(samples):
    target_point,uv,proof=project(source);maximum_residual=max(maximum_residual,proof['gradient_norm'])
    actual=surface(*BASE,F(str(uv[0])),F(str(uv[1])))
    mismatch=max(abs(float(x)-y) for x,y in zip(actual,target_point));assert mismatch<3e-13
    maximum_surface_error=max(maximum_surface_error,mismatch)
    tangents=partials(F(str(uv[0])),F(str(uv[1])))
    dots=[sum(float(t)*(float(a)-float(b)) for t,a,b in zip(tangent,actual,source)) for tangent in tangents]
    assert max(map(abs,dots))<3e-12;maximum_tangent_dot=max(maximum_tangent_dot,*map(abs,dots))
    proof['surface_tangent_dot_residuals']=dots
    projections.append({'source':list(map(str,source)),'foot':list(target_point),'parameters':list(uv),'proof':proof})
lines=['% Actual nearest projections of184 control-net edge/vertex samples.',
       '% Independent explicit representative p3q2 surface with2/5 height scaling.',
       '% Global uniqueness follows from half-distance Hessian bounds41/125 <=lambda<2.',
       '% All calculations use the displayed surface; no vertical drops or raster hatching.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-7.2,-6.12) rectangle (8.4,9.6);',r'\begin{scope}['+CAMERA+']']
for row in P:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
for j in range(4):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(row[j]) for row in P)+';')
for record in projections:
    A=tuple(map(F,record['source']));B=tuple(F(str(x)) for x in record['foot'])
    if sum((float(a)-float(b))**2 for a,b in zip(A,B))>1e-20:
        lines.append(r'\draw[book grid] '+point(A)+'--'+point(B)+';')
for variable,values in [('u',(F(0),F(1,4),F(3,4),F(1))),('v',(F(0),F(1,3),F(2,3),F(1)))]:
    for fixed in values:
        K,p,Q=isocurve(*BASE,variable,fixed);ss=segments(K,Q,p);checks+=check(K,Q,p,ss)
        for s in ss:lines.append(cubic_path(s,'book line' if fixed in (0,1) else 'book grid'))
lines += [r'\draw[book axis] (0,0,0)--(5.8,0,0) node[below left=4pt] {$x$};',
          r'\draw[book axis] (0,0,0)--(0,6.8,0) node[right=4pt] {$y$};',
          r'\draw[book axis] (0,0,0)--(0,0,2.88) node[above=4pt] {$z$};',r'\end{scope}',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/control-net-projection-check.json').write_text(json.dumps({
    'figure':'6.3','representative_control_net':[[list(map(str,pt)) for pt in row] for row in P],
    'height_scale':str(ZETA),'exact_tensor_checks':tensor,'native_isocurve_checks':checks,
    'whole_graph_strong_convexity_mu':str(MU),'gradient_Lipschitz_upper_bound':str(L),
    'exact_f_second_derivative_upper_bound':str(FY_SECOND_BOUND),
    'global_unique_projection_proof':'half squared-distance Hessian=I+grad(h)grad(h)^T+(h-Z)diag(hxx,hyy); ||hessian(h)||<=2/5,|h-Z|<=42/25 =>lower41/125; upper<2',
    'projection_count':len(projections),'maximum_numerical_stationarity_residual':maximum_residual,
    'maximum_surface_tangent_dot_residual':maximum_tangent_dot,
    'maximum_graph_vs_tensor_error':graph_error,'maximum_projected_foot_vs_tensor_error':maximum_surface_error,
    'projections':projections},indent=2)+'\n')
print(f'PASS:{tensor} exact tensor+{checks} native curve checks;184 globally unique projections,max gradient residual={maximum_residual:.3g}.')
