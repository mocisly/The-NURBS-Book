"""Fig5.5: six genuine interpolation points and exact repeated-insertion curve."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from knot55_data import K,P,u,p,table,ratios,states

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_06.tex';assert not target.exists()
old=segments(K,P,p);checks=check(K,P,p,old);spans=0
for U,R in states:
    ss=segments(U,R,p);checks+=check(U,R,p,ss)
    for s in ss:
        original=next(t for t in old if t['a']<=s['a'] and s['b']<=t['b']);assert s['power']==original['power'];spans+=1
    for i in range(121):assert de_boor(U,R,p,F(i,40))==de_boor(K,P,p,F(i,40))
assert table[3,3]==de_boor(K,P,p,u)
lines=['% Fig5.5: K=(0,0,0,0,2,3,3,3,3), insert ubar=1 three times.',
       '% Representative5-point cubic; exact Eq5.15 interpolation triangle, invariant polynomial curve.',
       '% Every visible Q is computed, never positioned from a scanned contour.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',r'\path[use as bounding box] (-1.3,-4.85) rectangle (12,7.35);',
       r'\begin{scope}[yshift=1.6cm]',r'\draw[book grid] '+'--'.join(map(point,P))+';']
for r in (1,2):lines.append(r'\draw[book grid] '+'--'.join(point(table[i,r]) for i in range(r,4))+';')
lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,states[-1][1]))+';')
for s in old:lines.append(cubic_path(s))
for i,anchor in enumerate(['below left','left','above','above right','below right']):
    lines += [r'\draw '+point(P[i])+' circle[radius=1.8pt];',r'\node['+anchor+'=5pt] at '+point(P[i])+r' {$\mathbf P_'+str(i)+'$};']
for key,anchor in [((1,1),'left'),((2,1),'above left'),((3,1),'above'),((2,2),'below right'),((3,2),'above right'),((3,3),'below right')]:
    lines += [r'\fill '+point(table[key])+' circle[radius=1.7pt];',r'\node['+anchor+'=5pt] at '+point(table[key])+r' {$\mathbf Q_{'+str(key[0])+','+str(key[1])+'}$};']
lines += [r'\end{scope}',r'\draw[book grid] (0,0)--(10,0);']
def xx(t):return F(16,5)*t
for t in sorted(set(K)):
    for j in range(K.count(t)):
        x=xx(t)+F(3,50)*(F(j)-F(K.count(t)-1,2));lines.append(r'\draw[book grid] '+point((x,F(-1,10)))+'--'+point((x,F(1,10)))+';')
    lines.append(r'\node[above=5pt] at '+point((xx(t),F(1,10)))+' {$'+str(t)+'$};')
lines.append(r'\draw[book axis] (3.2,.85)--(3.2,.1) node[pos=0,above=4pt] {$\bar u=1$};')
rows={(1,1):F(-4,5),(2,1):F(-5,4),(3,1):F(-17,10),(2,2):F(-13,5),(3,2):F(-61,20),(3,3):F(-4)}
for (i,r),y in rows.items():
    a,b=K[i],K[i+p-r+1];assert (u-a)/(b-a)==ratios[i,r]
    lines.append(r'\draw[book grid] '+point((xx(a),y+F(1,10)))+'--'+point((xx(a),y))+'--'+point((xx(b),y))+'--'+point((xx(b),y+F(1,10)))+';')
    lines.append(r'\draw '+point((xx(u),y))+' circle[radius=1.3pt];')
for r,y in [(1,F(-5,4)),(2,F(-113,40)),(3,F(-4))]:lines.append(r'\node[right=5pt] at '+point((F(21,2),y))+' {$r='+str(r)+'$};')
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/repeated-knot-insertion-check.json').write_text(json.dumps({'figure':'5.5','degree':3,'knots':list(map(str,K)),'representative_controls':[[str(c) for c in p] for p in P],'insertion_parameter':'1','repetitions':3,'exact_triangle':{str(k):list(map(str,v)) for k,v in table.items()},'ratios':{str(k):str(v) for k,v in ratios.items()},'native_span_checks':checks,'unchanged_polynomial_span_comparisons':spans,'deboor_curve_invariance_points':363,'final_triangle_point_equals_curve_at1':True},indent=2)+'\n')
print(f'PASS: six exact triangle points, {checks} native checks,{spans} unchanged spans,363 deBoor invariance points; Q33=C(1).')
