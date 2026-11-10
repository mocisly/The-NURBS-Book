"""Fig5.1: exact insertion, unchanged curve, and original/refined bases."""
from pathlib import Path
from fractions import Fraction as F
import json,argparse
from native_bspline import segments,check,cubic_path,point,number,de_boor
from surface_geometry import extraction,weights
from knot51_data import K,P,insert

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--existing',action='store_true');args=parser.parse_args()
figure='5.2' if args.existing else '5.1';u=F(2) if args.existing else F(5,2)
root=Path(__file__).resolve().parents[1];target=root/('image_tex/ch05/fig_5_02.tex' if args.existing else 'image_tex/ch05/fig_5_01.tex');assert not target.exists()
V,Q,alphas=insert(K,P,3,u)
assert alphas==({3:F(2,3),4:F(1,3),5:F(0)} if args.existing else {3:F(5,6),4:F(1,2),5:F(1,6)})
utex='2' if args.existing else r'\frac52'
def fraction_tex(a):return str(a.numerator) if a.denominator==1 else r'\frac{'+str(a.numerator)+'}{'+str(a.denominator)+'}'
old=segments(K,P,3);new=segments(V,Q,3);checks=check(K,P,3,old)+check(V,Q,3,new)
for s in new:
    original=next(t for t in old if t['a']<=s['a'] and s['b']<=t['b'])
    assert s['power']==original['power']
for n in range(201):
    t=F(n,40);assert de_boor(K,P,3,t)==de_boor(V,Q,3,t)
    a,b=weights(K,3,t),weights(V,3,t)
    assert a[0]==b[0] and a[1]==b[1] and a[6]==b[7] and a[7]==b[8]
    if args.existing:assert a[5]==b[6]
lines=['% Fig'+figure+': exact knot insertion ubar='+str(u)+' into cubic K; representative control coordinates.',
       '% Refined and original polynomial span coefficients are identical on every refined span.',
       '% Exact interpolation ratios recorded in geometry report. Native cubic paths and editable math labels; no contours.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\path[use as bounding box] (-.7,-2.6) rectangle (12.5,15.4);',
       r'\begin{scope}[yshift=5.5cm]',r'\begin{scope}[yshift=3.6cm]']
lines.append(r'\draw[book grid] '+'--'.join(map(point,P))+';')
lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,Q))+';')
for seg in old:lines.append(cubic_path(seg))
for i,(p,anchor) in enumerate(zip(P,['below right','above left','below left','below right','right','above right','above left','above left'])):
    j=i if i<=2 else i+1
    label=r'\mathbf P_'+str(i)+(r'=\mathbf Q_'+str(j) if i not in (3,4) or (args.existing and i==4) else '')
    lines += [r'\draw '+point(p)+' circle[radius=1.6pt];',r'\node['+anchor+'=5pt] at '+point(p)+' {$'+label+'$};']
for i,anchor in [(3,'below'),(4,'below right'),(5,'above right')]:
    if args.existing and i==5:continue
    lines += [r'\fill '+point(Q[i])+' circle[radius=1.6pt];',r'\node['+anchor+'=5pt] at '+point(Q[i])+r' {$\mathbf Q_'+str(i)+'$};']
lines += [r'\end{scope}',r'\draw[book grid] (1.5,1.8)--(10.5,1.8);']
def barx(t):return F(3,2)+F(9,5)*t
# Offset repeated endpoints only for symbolic multiplicity ticks.
for t in range(6):
    for offset in ([F(-9,100),F(-3,100),F(3,100),F(9,100)] if t in (0,5) else [F(0)]):
        x=barx(t)+offset;lines.append(r'\draw[book grid] '+point((x,F(17,10)))+'--'+point((x,F(19,10)))+';')
lines.append(r'\draw[book axis] '+point((barx(u),F(5,2)))+'--'+point((barx(u),F(19,10)))+r' node[pos=0,above=4pt] {$\bar u='+utex+'$};')
for i,y in [(3,F(6,5)),(4,F(7,10)),(5,F(1,5))]:
    a,b=K[i],K[i+3]
    lines.append(r'\draw[book grid] '+point((barx(a),y+F(1,10)))+'--'+point((barx(a),y))+'--'+point((barx(b),y))+'--'+point((barx(b),y+F(1,10)))+';')
    lines.append(r'\draw '+point((barx(u),y))+' circle[radius=1.3pt];')
    lines.append(r'\node[right=5pt] at '+point((barx(b),y))+r' {$\alpha_'+str(i)+'='+fraction_tex(alphas[i])+'$};')
lines += [r'\node at (5,-.55) {(a)};',r'\end{scope}',r'\draw[book axis] (0,0)--(11.9,0) node[right=4pt] {$u$};',r'\draw[book axis] (0,0)--(0,4.2);',r'\draw[book grid] (-.08,3)--(.08,3) node[left=5pt] {$1$};']
basispaths=0
for knots,count,style,indices in [(K,8,'book line',range(8)),(V,9,'book line,dashed',range(2,6 if args.existing else 7))]:
    for s in range(3,count):
        a,b=knots[s:s+2]
        if a==b:continue
        B=extraction(knots,3,s)
        for i in indices:
            if not any(row[i] for row in B):continue
            controls=tuple((F(11,5)*(a+(b-a)*F(r,3)),3*B[r][i]) for r in range(4))
            lines.append(cubic_path({'bern':controls},style));basispaths+=1
for t in range(6):
    x=F(11,5)*t
    anchor='below left' if args.existing and t==2 else 'below'
    lines += [r'\draw[book grid] '+point((x,F(-2,25)))+'--'+point((x,F(2,25)))+';',r'\node['+anchor+'=5pt] at '+point((x,0))+' {$'+str(t)+'$};']
labels=[(F(1,10),r'N_0=\bar N_0','right',F(18,5)),(F(9,10),r'N_1=\bar N_1','right',F(13,5)),(F(109,10),r'N_7=\bar N_8','left',F(18,5))]
labels+=([(F(43,5),r'N_5=\bar N_6','left',F(13,5)),(F(11,3),r'\bar N_3','above',F(12,5)),(F(77,15),r'\bar N_4','above',F(12,5))] if args.existing else [(F(97,10),r'N_6=\bar N_7','left',F(13,5)),(F(11,2),r'\bar N_4','above',F(12,5))])
for x,label,anchor,y in labels:
    lines.append(r'\node['+anchor+'=4pt] at '+point((x,y))+' {$'+label+'$};')
xx=F(11,5)*u
lines += [r'\draw[book axis] '+point((xx,F(-19,20)))+'--'+point((xx,F(-1,10)))+r' node[pos=0,below=4pt] {$\bar u='+utex+'$};',r'\node at (5.5,-2.15) {(b)};',r'\end{tikzpicture}']
target.parent.mkdir(exist_ok=True);target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/('image_tex/build/knot-insertion-existing-check.json' if args.existing else 'image_tex/build/knot-insertion-comparison-check.json')).write_text(json.dumps({'figure':figure,'degree':3,'knots_before':list(map(str,K)),'knots_after':list(map(str,V)),'representative_controls':list(map(lambda p:list(map(str,p)),P)),'refined_controls':list(map(lambda p:list(map(str,p)),Q)),'alphas':{str(i):str(a) for i,a in alphas.items()},'exact_unchanged_polynomial_spans':len(new),'deboor_and_partition_comparison_points':201,'native_span_checks':checks,'native_basis_paths':basispaths,'unchanged_basis_identities':['N0=barN0','N1=barN1','N6=barN7','N7=barN8']+(['N5=barN6'] if args.existing else [])},indent=2)+'\n')
print(f'PASS: {len(new)} identical polynomial spans,201 point/basis comparisons,{checks} exact curve checks,{basispaths} native basis paths.')
