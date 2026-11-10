"""6.17: exact reflected tensor control nets, tangent signs and normal orientation."""
from pathlib import Path
from fractions import Fraction as F
import json
from knot59_data import U,V,P
from surface_geometry import surface,isocurve,verify_tensor
from native_bspline import segments,check,cubic_path,point
from bspline_math import derivative,evaluate

root=Path(__file__).resolve().parents[1];data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for name in ('fig_6_21.tex','fig_6_22.tex'):
    assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/'+name)['applied']
BASE=(U,V,3,2,P)
def partials(base,u,v):
    result=[]
    for variable,fixed,t in [('u',v,u),('v',u,v)]:
        K,p,C=isocurve(*base,variable,fixed);ss=segments(K,C,p)
        seg=next(s for s in ss if s['a']<=t<=s['b'])
        result.append(tuple(evaluate(derivative(c),t) for c in seg['power']))
    return tuple(result)
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def scale(a,c):return tuple(x*c for x in a)
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
u0,v0=F(2,5),F(7,20);C=surface(*BASE,u0,v0);Su,Sv=partials(BASE,u0,v0);N=cross(Su,Sv);assert N!=(0,0,0)
panels=[];reports=[]
for letter,ur,vr in [('a',False,False),('b',True,False),('c',False,True),('not_drawn_both',True,True)]:
    K=tuple(1-u for u in reversed(U)) if ur else U
    L=tuple(1-v for v in reversed(V)) if vr else V
    Q=tuple(reversed(P)) if ur else P
    Q=tuple(tuple(reversed(row)) for row in Q) if vr else Q
    base=(K,L,3,2,Q);tensor=verify_tensor(*base,steps=10)
    for i in range(11):
        for j in range(11):
            u,v=F(i,10),F(j,10);s,t=1-u if ur else u,1-v if vr else v
            assert surface(*base,s,t)==surface(*BASE,u,v)
            a,b=partials(BASE,u,v);aa,bb=partials(base,s,t)
            assert aa==scale(a,-1 if ur else 1) and bb==scale(b,-1 if vr else 1)
            assert cross(aa,bb)==scale(cross(a,b),(-1 if ur else 1)*(-1 if vr else 1))
    aa,bb=partials(base,1-u0 if ur else u0,1-v0 if vr else v0);nn=cross(aa,bb)
    proof={'panel':letter,'u_reversed':ur,'v_reversed':vr,'tensor_checks':tensor,
           'exact_geometry_and_derivative_sign_checks':121,'exact_normal_cross_product_sign_checks':121,
           'reflected_u_knots':list(map(str,K)),'reflected_v_knots':list(map(str,L)),
           'new_partial_u':list(map(str,aa)),'new_partial_v':list(map(str,bb)),'new_normal':list(map(str,nn))}
    reports.append(proof)
    if letter=='not_drawn_both':continue
    lines=[r'\begin{scope}[x={(-.81cm,-.54cm)},y={(.9cm,-.315cm)},z={(0cm,1.5cm)}]'];native=0
    for variable,values in [('u',(F(0),F(1))),('v',(F(0),F(1)))]:
        for fixed in values:
            knots,p,controls=isocurve(*BASE,variable,fixed);ss=segments(knots,controls,p);native+=check(knots,controls,p,ss)
            lines.extend(cubic_path(s) for s in ss)
    for variable,fixed in [('u',v0),('v',u0)]:
        knots,p,controls=isocurve(*BASE,variable,fixed);ss=segments(knots,controls,p);native+=check(knots,controls,p,ss)
        lines.extend(cubic_path(s,'book grid,dashed') for s in ss)
    vecs=[(aa,F(1,2),r'\mathbf S_s' if ur else r'\mathbf S_u','above left' if ur else 'below right',False),
          (bb,F(1,2),r'\mathbf S_t' if vr else r'\mathbf S_v','below left' if vr else 'right',False),
          (nn,F(1,8),r'-\mathbf N' if ur or vr else r'\mathbf N','right' if ur or vr else 'above left',ur or vr)]
    for vec,factor,label,anchor,dashed in vecs:
        tip=plus(C,scale(vec,factor))
        gap='8pt' if anchor=='right' else '6pt'
        lines.append(r'\draw[book axis'+(',dashed' if dashed else '')+'] '+point(C)+'--'+point(tip)+r' node['+anchor+'='+gap+r'] {$'+label+'$};')
    lines += [r'\draw '+point(C)+r' circle[radius=2pt];',
              r'\draw[book axis] (0,0,0)--(5.5,0,0) node[below left=4pt] {$x$};',
              r'\draw[book axis] (0,0,0)--(0,6.3,0) node[right=4pt] {$y$};',
              r'\draw[book axis] (0,0,0)--(0,0,4.8) node[above=4pt] {$z$};',
              r'\end{scope}',r'\node at (0,-5.1) {('+letter+')};']
    panels.append(lines);proof['native_isocurve_checks']=native
    print(f'Panel{letter}:121 exact geometry/partial/normal sign checks,{native} native curve checks.',flush=True)
for group,name in [(panels[:2],'fig_6_21.tex'),(panels[2:],'fig_6_22.tex')]:
    right='20.1' if len(group)==2 else '6.6'
    lines=['% Same explicit3x2 representative surface as5.9/6.14, exact reflection of parameter/control net.',
           '% Arrows display1/2 of first partials and1/8 of normal, consistently in all panels.',
           '% One reversed parameter negates the normal; both reversed restore it (also verified).',
           r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-6,-5.6) rectangle ('+right+',8.3);']
    for j,panel in enumerate(group):
        lines.append(r'\begin{scope}[xshift='+str(13.5*j)+'cm]');lines.extend(panel);lines.append(r'\end{scope}')
    lines.append(r'\end{tikzpicture}');(root/'image_tex/ch06'/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-reversal-check.json').write_text(json.dumps({
    'figure':'6.17','original_parameter_point':list(map(str,(u0,v0))),
    'physical_point':list(map(str,C)),'source_partial_u':list(map(str,Su)),
    'source_partial_v':list(map(str,Sv)),'source_normal':list(map(str,N)),
    'display_partial_factor':'1/2','display_normal_factor':'1/8','panels':reports},indent=2)+'\n')
print('PASS:all four reflection cases verified,three orientation diagrams authored.')
