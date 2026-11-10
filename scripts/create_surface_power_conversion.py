"""6.19: three exact polynomial patches and selected global tensor coefficient vectors."""
from pathlib import Path
from fractions import Fraction as F
import json
from tensor_power_conversion import convert,evaluate
from surface_geometry import verify_tensor,surface,isocurve
from native_surface_drawing import wires
from native_bspline import segments,check,cubic_path,point,number

root=Path(__file__).resolve().parents[1];data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for name in ('fig_6_24.tex','fig_6_25.tex'):
    assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/'+name)['applied']
U=(F(0),)*4+(F(3,10),F(7,10))+(F(1),)*4
V=(F(0),)*3+(F(3,10),F(3,5))+(F(1),)*3
xs=(F(3),F(3,2),F(0),-F(3,2),-F(3))
ys=(-F(3),-F(2),-F(3,5),F(4,5),F(11,5),F(7,2))
zu=(F(0),F(0),F(3,5),F(2),F(2),F(2));zv=(F(3,10),F(0),F(0),F(3,10),F(3,5))
# Small explicitly declared XY terms give a genuinely coupled polynomial sheet.
P=tuple(tuple((x+F(1,50)*x*y,y-F(1,100)*x*y,zu[i]+zv[j]+F(1,20)*x*y) for j,x in enumerate(xs)) for i,y in enumerate(ys))
BASE=(U,V,3,2,P);tensor=verify_tensor(*BASE,steps=10);patches={};proofs=[]
uspans=[i for i in range(3,len(P)) if U[i]<U[i+1]]
vspans=[j for j in range(2,len(P[0])) if V[j]<V[j+1]]
assert len(uspans)==len(vspans)==3
for iu,us in enumerate(uspans):
    for iv,vs in enumerate(vspans):
        Q,A,B=convert(*BASE,us,vs);a,b=U[us:us+2];c,d=V[vs:vs+2]
        for i in range(6):
            for j in range(6):
                u=a+(b-a)*F(i,5);v=c+(d-c)*F(j,5)
                assert evaluate(B,u,v)==surface(*BASE,u,v)
        patches[iu,iv]=((a,)*4+(b,)*4,(c,)*3+(d,)*3,3,2,Q)
        proofs.append({'patch':[iu,iv],'domain':list(map(str,(a,b,c,d))),
                       'all12_global_tensor_coefficients_equal_independent_Cox_products':True,
                       'exact_surface_evaluation_checks':36,
                       'global_power_coefficients':[[list(map(str,pt)) for pt in row] for row in B]})
selected=((0,2),(1,1),(2,0));camera=r'x={(-.81cm,-.54cm)},y={(.9cm,-.315cm)},z={(0cm,1.2cm)}'
lines=['% Explicit representative6x5 p3q2 sheet with the stated U/V; all weightsone.',
       '% Three selected patches are exact tensor restrictions; cross-isocurves computed natively.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-6.6,-5.6) rectangle (7,8.2);',r'\begin{scope}['+camera+']']
paths,wireproof=wires(*BASE,count=31);lines.extend(paths);crosschecks=0
for key in selected:
    base=patches[key];K,L,p,q,Q=base;a,b=K[0],K[-1];c,d=L[0],L[-1]
    for i in range(9):
        fixed=a+(b-a)*F(i,8);knots,deg,C=isocurve(*base,'v',fixed);ss=segments(knots,C,deg);crosschecks+=check(knots,C,deg,ss)
        lines.extend(cubic_path(s,'book line' if i in (0,8) else 'book grid') for s in ss)
    for fixed in (c,d):
        knots,deg,C=isocurve(*base,'u',fixed);ss=segments(knots,C,deg);crosschecks+=check(knots,C,deg,ss)
        lines.extend(cubic_path(s) for s in ss)
lines += [r'\draw[book axis] (0,0,0)--(5.5,0,0) node[below left=4pt] {$x$};',
          r'\draw[book axis] (0,0,0)--(0,6.3,0) node[right=4pt] {$y$};',
          r'\draw[book axis] (0,0,0)--(0,0,5.8) node[above=4pt] {$z$};',r'\end{scope}',r'\node at (0,-5.1) {(a)};',r'\end{tikzpicture}']
(root/'image_tex/ch06/fig_6_24.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
center=next(proof for proof in proofs if proof['patch']==[1,1]);B=tuple(tuple(tuple(map(F,pt)) for pt in row) for row in center['global_power_coefficients'])
indices=((0,0),(1,0),(0,1),(0,2),(1,2),(2,0),(3,0))
tips=[tuple(x/2 for x in B[i][j]) for i,j in indices]
def screen(pt):
    x,y,z=pt;return (-F(81,100)*x+F(9,10)*y,-F(27,50)*x-F(63,200)*y+F(6,5)*z)
maximum=max(abs(t) for pt in tips for t in screen(pt));viewscale=min(F(1),F(23,5)/maximum)
# Independent coefficient-view coordinate scale, preserving all vector directions
# and the stipulated b/2 display convention. Fonts/strokes are never scaled.
cam=('x={('+number(-F(81,100)*viewscale)+'cm,'+number(-F(27,50)*viewscale)+'cm)},'
     'y={('+number(F(9,10)*viewscale)+'cm,'+number(-F(63,200)*viewscale)+'cm)},'
     'z={(0cm,'+number(F(6,5)*viewscale)+'cm)}')
lines=['% Selected GLOBAL power coefficients of patch(1,1), computed as R3*M3*Q*M2^T*R2^T.',
       '% Arrows are b_ij/2. This panel has its own uniform coordinate-view scale, not a font scaling.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-6.6,-5.6) rectangle (7,8.2);',r'\begin{scope}['+cam+']']
positions=[]
short_indices={(0,2),(1,2)}
for (i,j),tip in zip(indices,tips):
    x,y=screen(tip);x*=viewscale;y*=viewscale
    anchor=('right' if x>=0 else 'left') if abs(y)<abs(x)/3 else ('above right' if x>=0 else 'above left') if y>=0 else ('below right' if x>=0 else 'below left')
    label='' if (i,j) in short_indices else r' node['+anchor+r'=6pt] {$\mathbf b_{'+str(i)+','+str(j)+'}$}'
    style='book line,-{Stealth[length=3pt]}' if (i,j) in short_indices else 'book axis'
    lines.append(r'\draw['+style+'] (0,0,0)--'+point(tip)+label+';')
    positions.append({'index':[i,j],'coefficient':list(map(str,B[i][j])),'screen_tip_cm':list(map(str,(x,y)))})
axis=6/viewscale
for axisindex,label in [(0,'x'),(1,'y'),(2,'z')]:
    pt=tuple(axis if d==axisindex else F(0) for d in range(3))
    lines.append(r'\draw[book axis,book grid] (0,0,0)--'+point(pt)+r' node['+('below left' if axisindex==0 else 'right' if axisindex==1 else 'above')+r'=4pt] {$'+label+'$};')
lines += [r'\end{scope}',r'\draw[book grid] (-.5,-.1) rectangle (.15,.55);',
          r'\draw[book grid,densely dotted] (.15,.55)--(2.3,3.8);',
          r'\draw[book grid] (2.3,3.8) rectangle (6.5,7.8);',
          r'\node at (5.7,7.2) {$\times4$};',r'\draw (5,4.6) circle[radius=1.2pt];']
for record in positions:
    if tuple(record['index']) not in short_indices:continue
    x,y=map(F,record['screen_tip_cm']);tip=(F(5)+4*x,F(23,5)+4*y);i,j=record['index']
    anchor='above left' if (i,j)==(0,2) else 'right'
    lines.append(r'\draw[book axis] (5,4.6)--'+point(tip)+r' node['+anchor+r'=6pt] {$\mathbf b_{'+str(i)+','+str(j)+'}$};')
lines += [r'\node at (0,-5.1) {(b)};',r'\end{tikzpicture}']
(root/'image_tex/ch06/fig_6_25.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-power-conversion-check.json').write_text(json.dumps({
    'figure':'6.19','representative_controls':[[list(map(str,pt)) for pt in row] for row in P],
    'knots':[list(map(str,U)),list(map(str,V))],'native_tensor_checks':tensor,
    'all_patch_power_proofs':proofs,'selected_patches':[list(t) for t in selected],
    'whole_surface_wire_proof':wireproof,'selected_patch_cross_isocurve_checks':crosschecks,
    'coefficient_display_factor':'1/2','independent_coefficient_view_coordinate_scale':str(viewscale),
    'selected_coefficient_arrows':positions,'small_coefficient_projection_inset':{'indices':[[0,2],[1,2]],'magnification':4}},indent=2)+'\n')
print(f'PASS:all9patches12globalcoefficients identical to independent Cox products;324 exact surface evaluations;{crosschecks}selected grid checks.')
print('Coefficient screen endpoints:'+str([(r['index'],tuple(map(float,map(F,r['screen_tip_cm'])))) for r in positions]))
