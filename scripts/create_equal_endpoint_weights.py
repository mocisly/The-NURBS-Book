"""6.15: endpoint-weight equalization from6.58, with a certified cube-root enclosure."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point,cubic_path,de_boor
from rational_geometry import project,approximate
from mobius_reparameterization import transform

root=Path(__file__).resolve().parents[1];data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in data['images'] if e['tex']=='image_tex/ch06/fig_6_19.tex')['applied']
U=(F(0),)*4+(F(3,10),F(7,10))+(F(1),)*4
P=((F(1),F(0)),(F(0),F(3)),(F(4),F(6)),(F(5),-F(2)),(F(10),F(0)),(F(8),F(3,2)))
weights=(F(2),F(8),F(3),F(4),F(2),F(5));H=tuple(tuple(w*x for x in pt)+(w,) for w,pt in zip(weights,P))
# r=(5/2)^(1/3). Under the exact algebraic relation r^3=5/2,
# transformed endpoint weights before common scaling are2 and5/r^3=2.
D=10**36;low,high=D,2*D
while high-low>1:
    mid=(low+high)//2
    if 2*mid**3<5*D**3:low=mid
    else:high=mid
lo,hi=F(low,D),F(high,D);assert 2*lo**3<5<2*hi**3
r=(lo+hi)/2;c,d=F(1,10),F(4,5)
coeff=(r*d-c,c,r-1,F(1));K,Q,g,inverse,proof=transform(U,H,3,coeff)
Q=tuple(tuple(x/2 for x in row) for row in Q)
assert tuple(map(project,Q))==P and K[0]==c and K[-1]==d and Q[0][-1]==1
end_bound=max(abs(F(5,2)/lo**3-1),abs(F(5,2)/hi**3-1))
assert abs(Q[-1][-1]-1)<=end_bound<F(1,10**34)
ss=segments(U,H,3);minimum=min(weights);lipschitz=F(0)
for seg in ss:
    B=seg['bern'];h=seg['b']-seg['a']
    A=max(sum(map(abs,pt[:-1])) for pt in B)
    Ap=max(3*sum(abs(y-x) for x,y in zip(a[:-1],b[:-1]))/h for a,b in zip(B,B[1:]))
    Wp=max(3*abs(a[-1]-b[-1])/h for a,b in zip(B,B[1:]))
    lipschitz=max(lipschitz,Ap/minimum+A*Wp/minimum**2)
# For fixed normalized new parameter v, inverse u=v/(r-(r-1)v)
# has |du/dr|<=1/4 since r>=1. This bounds all sampling-point displacement.
sample_error=lipschitz*(hi-lo)/4
assert sample_error<F(1,10**32)
checks=check(U,H,3,ss,steps=11)+check(K,Q,3,segments(K,Q,3),steps=11)
old=[project(de_boor(U,H,3,F(i,20))) for i in range(21)]
new=[project(de_boor(K,Q,3,c+(d-c)*F(i,20))) for i in range(21)]
lines=['% Exact endpoint equalization of6.58 with r^3=5/2; theoretical endpoint weights both1.',
       '% Rendering uses a rational r enclosure of width1e-36; all marker displacement certified<1e-32.',
       '% Original weights(2,8,3,4,2,5), unchanged representative six control points.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-.6,-3.7) rectangle (14.5,8.5);',
       r'\begin{scope}[x=1.2cm,y=1.2cm]',r'\draw[book grid] '+'--'.join(map(point,P))+';']
for a in old:
    lines += [r'\begin{scope}[shift={'+point(a)+'}]',r'\draw[book grid] (-1.8pt,0)--(1.8pt,0) (0,-1.8pt)--(0,1.8pt);',r'\end{scope}']
for a in new:lines.append(r'\node[rectangle,draw,line width=.35pt,inner sep=1.4pt] at '+point(a)+' {};')
for a in P:lines.append(r'\draw '+point(a)+r' circle[radius=1.7pt];')
lines += [r'\end{scope}',r'\begin{scope}[xshift=8.8cm,yshift=4.3cm,x=3.6cm,y=3.3cm]',
          r'\draw[book axis] (0,0)--(1.12,0) node[right=3pt] {$u$};',
          r'\draw[book axis] (0,0)--(0,1.08) node[above=3pt] {$s$};',
          r'\node[below left=3pt] at (0,0) {$0$};',
          r'\draw[book grid] (1,-.025)--(1,.025) node[below=4pt] {$1$};',
          r'\draw[book grid] (-.025,1)--(.025,1) node[left=4pt] {$1$};']
a,b,cc,dd=coeff;graph=((F(0),b,dd),(dd/2,b+a/2,dd+cc/2),(cc+dd,a+b,cc+dd))
maximum=F(0);count=0
for piece in approximate(graph,F(1,100000)):
    lines.append(cubic_path(piece));maximum=max(maximum,piece['certified_l1_error']);count+=1
lines += [r'\node[right=4pt] at (1,.8) {$g(u)$};',r'\end{scope}',
          r'\node at (6,-3.1) {$w_0=2,\quad w_5=5\quad\longrightarrow\quad\bar w_0=\bar w_5=1$};',r'\end{tikzpicture}']
(root/'image_tex/ch06/fig_6_19.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
proof.update({'figure':'6.15','source_control_points':[[str(x) for x in pt] for pt in P],
              'original_knots':list(map(str,U)),'original_weights':list(map(str,weights)),
              'new_knots':list(map(str,K)),'new_weights':[str(pt[-1]) for pt in Q],
              'exact_cube_root_relation':'r^3=5/2','exact_equalized_endpoint_proof':'wbar0=2/2=1;wbar5=5/(2r^3)=1',
              'cube_root_enclosure':list(map(str,(lo,hi))),'endpoint_weight_rendering_error_bound':str(end_bound),
              'original_curve_global_L1_derivative_bound':str(lipschitz),'whole_interval_sampling_error_bound':str(sample_error),
              'native_basis_checks':checks,'mapping_graph_native_paths':count,'mapping_graph_error_bound':str(maximum)})
(root/'image_tex/build/equal-endpoint-weights-check.json').write_text(json.dumps(proof,indent=2)+'\n')
print(f'PASS:6.58 exact algebraic endpoint equalization,101 exact curve identities,{checks}native checks;root/marker errors certified.')
