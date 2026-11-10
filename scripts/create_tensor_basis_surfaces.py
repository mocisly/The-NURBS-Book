"""Fig3.19: exact tensor basis wireframes and their two marginal functions."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
from bspline_math import piece,evaluate,compose_affine,basis,derivative
from native_bspline import segments,check,cubic_path,point

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_20.tex';assert not target.exists()
U=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
V=(F(0),)*3+tuple(F(i,5) for i in (1,2,3,3,4))+(F(1),)*3
families=[(U,4,3),(V,4,2),(V,2,2)];checks=0
for k,i,p in families:
    controls=tuple((F(j==i),) for j in range(len(k)-p-1))
    checks+=check(k,controls,p,segments(k,controls,p))
assert basis(V,4,2,F(3,5))==1
assert evaluate(derivative(piece(V,4,2,4)),F(3,5))==10
assert evaluate(derivative(piece(V,4,2,6)),F(3,5))==-10
assert basis(V,2,2,F(3,10))==F(3,4)
# Exact tensor-product partition, including all repeated-knot grid crossings.
for a in range(20):
    u=F(a,20);wu=[basis(U,i,3,u) for i in range(7)]
    assert min(wu)>=0 and sum(wu)==1
    for b in range(20):
        v=F(b,20);wv=[basis(V,j,2,v) for j in range(8)]
        assert min(wv)>=0 and sum(wv)==1
        assert sum(x*y for x in wu for y in wv)==1

graph_checks=0
def graph(k,i,p,variable,fixed,scale):
    """Exact polynomial graph in3D, represented in Bernstein controls per span."""
    global graph_checks
    result=[]
    for s in range(p,len(k)-p-1):
        a,b=k[s:s+2]
        if a==b: continue
        z=tuple(scale*c for c in compose_affine(piece(k,i,p,s),a,b-a))
        polynomials=((a,b-a),(fixed,),z) if variable=='u' else ((fixed,),(a,b-a),z)
        bern=tuple(tuple(sum((c[l] if l<len(c) else 0)*F(comb(j,l),comb(p,l)) for l in range(j+1)) for c in polynomials) for j in range(p+1))
        for h in (F(0),F(1,3),F(2,3)):
            u=a+(b-a)*h
            assert evaluate(z,h)==scale*basis(k,i,p,u)
            graph_checks+=1
        result.append({'bern':bern})
    return result

lines=['% Printed Fig3.19: N4,3(u) times N4,2(v) or N2,2(v), exact caption knots.',
       '% Every wire is an exact polynomial graph from Cox-de Boor, converted to native Bezier controls.',
       '% One shared affine camera for surface and marginal functions, matching Fig1.24 style.',
       '% Regular parameter isolines, not raster contours. Repeated v=3/5 ridge included exactly.',
       r'\begin{tikzpicture}[x={(4cm,-1.3cm)},y={(-2.6cm,-1.8cm)},z={(0cm,3cm)},',
       r'book line,line cap=round,line join=round]',
       r'\path[use as bounding box] (canvas cs:x=-5.5cm,y=-4.4cm) rectangle (canvas cs:x=6.2cm,y=14.7cm);']
for panel,index,shift in [('a',4,10),('b',2,0)]:
    lines.append(r'\begin{scope}[yshift='+str(shift)+'cm]')
    for j in range(21):
        t=F(j,20)
        lines.append('% Exact u-isoline at v='+str(t))
        for seg in graph(U,4,3,'u',t,basis(V,index,2,t)):
            lines.append(cubic_path(seg,'line width=.3pt'))
        lines.append('% Exact v-isoline at u='+str(t))
        for seg in graph(V,index,2,'v',t,basis(U,4,3,t)):
            lines.append(cubic_path(seg,'line width=.3pt'))
    for k,i,p,var in [(U,4,3,'u'),(V,index,2,'v')]:
        fixed=F(-9,20)
        origin=(F(0),fixed,F(0)) if var=='u' else (fixed,F(0),F(0))
        end=(F(23,20),fixed,F(0)) if var=='u' else (fixed,F(23,20),F(0))
        zend=(origin[0],origin[1],F(23,20))
        lines += [r'\draw[book axis,book grid] '+point(origin)+'--'+point(end)+r' node['+('right' if var=='u' else 'below left')+'] {$'+var+'$};',
                  r'\draw[book axis,book grid] '+point(origin)+'--'+point(zend)+';',
                  r'\node['+('right' if var=='u' else 'left')+'] at '+point((origin[0],origin[1],F(1)))+' {$1$};',
                  r'\node[below=4pt] at '+point(origin)+' {$0$};']
        for t in sorted(set(k)):
            a=(t,fixed-F(1,100),F(0)) if var=='u' else (fixed-F(1,100),t,F(0))
            b=(t,fixed+F(1,100),F(0)) if var=='u' else (fixed+F(1,100),t,F(0))
            lines.append(r'\draw[book grid] '+point(a)+'--'+point(b)+';')
        endpoint=(F(1),fixed,F(0)) if var=='u' else (fixed,F(1),F(0))
        lines.append(r'\node[below=4pt] at '+point(endpoint)+' {$1$};')
        for seg in graph(k,i,p,var,fixed,F(1)): lines.append(cubic_path(seg))
        for t in (F(0),F(1)):
            a=(t,fixed,F(0)) if var=='u' else (fixed,t,F(0))
            b=(t,F(0),F(0)) if var=='u' else (F(0),t,F(0))
            lines.append(r'\draw[book grid,dashed] '+point(a)+'--'+point(b)+';')
    lines.append(r'\node at (.72,-.45,.9) {$N_{4,3}(u)$};')
    lines.append(r'\node at '+('(-.45,.65,1.18)' if index==4 else '(-.45,.3,1)')+' {$N_{'+str(index)+',2}(v)$};')
    lines.append(r'\node at (canvas cs:x=.5cm,y=-3.6cm) {$N_{4,3}(u)N_{'+str(index)+',2}(v)$};')
    lines.append(r'\node at (canvas cs:x=.5cm,y=-4.15cm) {('+panel+')};')
    lines.append(r'\end{scope}')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/tensor-basis-surfaces-check.json').write_text(json.dumps({'figure':'3.19',
    'U':list(map(str,U)),'V':list(map(str,V)),'exact_basis_curve_checks':checks,
    'tensor_partition_grid_points':400,'exact_3d_graph_checks':graph_checks,
    'mesh_isolines_per_direction':21,'v4_peak_at_three_fifths':'1',
    'v4_one_sided_derivatives_at_three_fifths':['10','-10'],'v2_value_at_three_tenths':'3/4',
    'shared_affine_camera_with_marginals':True,'mesh_constructed_from_basis_polynomials':True},indent=2)+'\n')
print(f'PASS: {checks} exact basis checks,400 tensor partition checks,{graph_checks} native polynomial graph checks.')
