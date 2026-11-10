"""9.19:exact chord vectors,Akima blend and parameter-dependent derivative blend."""
from fractions import Fraction as F
from pathlib import Path
import json
from native_bspline import point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_23.tex')['applied']
Q=tuple(tuple(map(F,p)) for p in [('0','0'),('.4','3'),('2.8','4.2'),('6.8','3'),('7.2','.8')])
params=tuple(map(F,['0','1/5','3/5','13/10','17/10']))
chords=tuple(tuple(b-a for a,b in zip(A,B)) for A,B in zip(Q,Q[1:]))
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
a,b=abs(cross(chords[0],chords[1])),abs(cross(chords[2],chords[3]));alpha=a/(a+b);assert alpha==F(21,47)
du=(params[2]-params[1],params[3]-params[2]);assert du==(F(2,5),F(7,10))
V=tuple((1-alpha)*x+alpha*y for x,y in zip(chords[1],chords[2]))
D=tuple((1-alpha)*x/du[0]+alpha*y/du[1] for x,y in zip(chords[1],chords[2]))
assert V==(F(732,235),F(6,47)) and D==(F(276,47),F(42,47)) and cross(V,D)!=0
lines=['% Representative five-point geometry;all q,V,D are computed vectors,not placed arrows.',r'\begin{tikzpicture}[book line,x=2.5cm,y=2.5cm]',r'\path[use as bounding box] (-.8,-.7) rectangle (9.4,5.9);']
for i,(A,B,name,anchor) in enumerate(zip(Q,Q[1:],['k-1','k','k+1','k+2'],['right','below','below','left'])):
    lines.append(r'\draw[book axis,shorten >=3pt] '+point(A)+'--'+point(B)+';')
    mid=tuple((x+y)/2 for x,y in zip(A,B));lines.append(r'\node['+anchor+r'=8pt] at '+point(mid)+r' {$\mathbf q_{'+name+'}$};')
for vec,name in [(V,'V'),(D,'D')]:
    tip=tuple(a+b for a,b in zip(Q[2],vec));lines.append(r'\draw[book axis] '+point(Q[2])+'--'+point(tip)+';')
    where=tip if name=='V' else tuple(a+b/2 for a,b in zip(Q[2],vec))
    lines.append(r'\node['+('right' if name=='V' else 'above')+r'=8pt] at '+point(where)+r' {$\mathbf '+name+'_{k}$};')
for q,name,anchor in zip(Q,['k-2','k-1','k','k+1','k+2'],['below right','above left','above left','below left','below left']):
    lines.append(r'\draw '+point(q)+r' circle[radius=2.4pt];')
    lines.append(r'\node['+anchor+r'=8pt] at '+point(q)+r' {$\mathbf Q_{'+name+'}$};')
lines.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_23.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/local-tangent-derivative-vectors-check.json').write_text(json.dumps(dict(figure='9.19',representative_data=[[str(x) for x in q] for q in Q],representative_parameters=list(map(str,params)),actual_chord_vectors=[[str(x) for x in q] for q in chords],cross_product_magnitudes=[str(a),str(b)],alpha_from_equation9_31=str(alpha),adjacent_parameter_increments=list(map(str,du)),V_from_equation9_29=list(map(str,V)),D_from_equation9_28=list(map(str,D)),V_cross_D_nonzero=str(cross(V,D)),all_vector_arrows_actual_coordinate_scale='1',q_arrow_tips_shortened_only_to_clear_open_endpoint_markers=True),indent=2)+'\n')
print('PASS:four exact chord differences,Akima alpha21/47,V=(732/235,6/47),D=(276/47,42/47);actual arrows share scale1 and have distinct directions.')
