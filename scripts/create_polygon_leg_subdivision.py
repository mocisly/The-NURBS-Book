"""Fig5.3: native indexed polygon legs partitioned by the specified knot spans."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point
from polygon_leg_data import K,P

root=Path(__file__).resolve().parents[1]
targets=[root/f'image_tex/ch05/fig_5_0{i}.tex' for i in (3,4)];assert not any(p.exists() for p in targets)
def mix(a,b,t):return tuple((1-t)*x+t*y for x,y in zip(a,b))
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,t):return tuple(x*t for x in a)
partition=[]
lines=['% Fig5.3(a): representative 11-point polygon; specified cubic knot vector.',
       '% Every leg is partitioned by exact normalized knot differences, including zero subintervals.',
       '% Native lines, circles and editable labels; no image contours.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\path[use as bounding box] (-1,-2.6) rectangle (12,6.4);',
       r'\draw[book line] '+'--'.join(map(point,P))+';']
for i in range(1,len(P)):
    lam=tuple((K[i+j+1]-K[i+j])/(K[i+3]-K[i]) for j in range(3));assert sum(lam)==1 and min(lam)>=0
    t=F(0);marks=[]
    for fraction in lam[:-1]:
        t+=fraction
        if 0<t<1 and t not in marks:
            lines.append(r'\draw '+point(mix(P[i-1],P[i],t))+' circle[radius=1.15pt];');marks.append(t)
    cuts=[mix(P[i-1],P[i],sum(lam[:j])) for j in range(4)]
    for j in range(3):
        d=sum((P[i][k]-P[i-1][k])**2 for k in range(2));dj=sum((cuts[j+1][k]-cuts[j][k])**2 for k in range(2));assert dj==lam[j]**2*d
    partition.append({'leg':i,'knots':list(map(str,K[i:i+4])),'normalized_lengths':list(map(str,lam)),'distinct_interior_cuts':list(map(str,marks))})
for i,(p,anchor) in enumerate(zip(P,['below right','left','above left','above','right','left','below','below right','right','above right','above'])):
    lines += [r'\draw '+point(p)+' circle[radius=2pt];',r'\node['+anchor+'=5pt] at '+point(p)+r' {$\mathbf P_{'+str(i)+'}$};']
lines.append(r'\draw[book grid] (0,-1.5)--(11,-1.5);')
for t in sorted(set(K)):
    multiplicity=K.count(t)
    for j in range(multiplicity):
        x=F(11,7)*t+F(3,50)*(F(j)-F(multiplicity-1,2))
        lines.append(r'\draw[book grid] '+point((x,F(-8,5)))+'--'+point((x,F(-7,5)))+';')
    lines.append(r'\node[below=5pt] at '+point((F(11,7)*t,F(-3,2)))+' {$'+str(t)+'$};')
lines += [r'\node at (5.5,-2.35) {(a)};',r'\end{tikzpicture}'];targets[0].write_text('\n'.join(lines)+'\n',encoding='utf-8')

# A true uniform enlargement of the same P2-P3 edge, not a pixel-derived outline.
A=(F(0),F(13,5));B=plus(A,scale(tuple(P[3][d]-P[2][d] for d in range(2)),3));normal=(F(-1,6),F(29,30))
lines=['% Fig5.3(b): enlarged L3=P2P3, three equal knot subspans [u3,u4],[u4,u5],[u5,u6].',
       '% Same edge direction as panel(a), enlarged exactly3 times. lambda=1/3, lengths d3/3.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',r'\path[use as bounding box] (-1,-2.25) rectangle (10,6.1);',
       r'\draw '+point(A)+'--'+point(B)+';']
for j in range(4):
    pt=mix(A,B,F(j,3));lines.append(r'\draw '+point(pt)+' circle[radius='+('1.8pt' if j in (0,3) else '1.2pt')+'];')
lines += [r'\node[left=5pt] at '+point(A)+r' {$\mathbf P_2$};',r'\node[right=5pt] at '+point(B)+r' {$\mathbf P_3$};']
def dimension(a,b,label):
    c,d=mix(a,b,F(2,5)),mix(a,b,F(3,5))
    lines.extend([r'\draw[book grid,{Stealth[length=4pt]}-] '+point(a)+'--'+point(c)+';',
                  r'\draw[book grid,-{Stealth[length=4pt]}] '+point(d)+'--'+point(b)+';',
                  r'\node at '+point(mix(a,b,F(1,2)))+' {$'+label+'$};'])
    for pt in (a,b):lines.append(r'\draw[book grid] '+point(plus(pt,scale(normal,F(-1,10))))+'--'+point(plus(pt,scale(normal,F(1,10))))+';')
for j in range(3):
    a,b=plus(mix(A,B,F(j,3)),scale(normal,F(4,5))),plus(mix(A,B,F(j+1,3)),scale(normal,F(4,5)))
    dimension(a,b,r'd_3^{'+str(j)+'}')
    lines.append(r'\node[above=4pt] at '+point(plus(mix(a,b,F(1,2)),scale(normal,F(3,10))))+r' {$L_3^{'+str(j)+'}$};')
dimension(plus(A,scale(normal,F(-4,5))),plus(B,scale(normal,F(-4,5))),r'd_3')
lines.append(r'\draw[book grid] (0,.1)--(8.7,.1);')
for j in range(4):
    x=F(29,10)*j
    lines += [r'\draw[book grid] '+point((x,F(0)))+'--'+point((x,F(1,5)))+';',r'\node[above=5pt] at '+point((x,F(1,10)))+' {$u_'+str(3+j)+'$};']
for j in range(3):lines.append(r'\node at '+point((F(29,10)*(F(j)+F(1,2)),F(-1,2)))+r' {$\lambda_3^{'+str(j)+r'}=\frac13$};')
dimension((F(0),F(-6,5)),(F(87,10),F(-6,5)),r'u_6-u_3')
lines += [r'\node at (4.35,-1.95) {(b)};',r'\end{tikzpicture}'];targets[1].write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/polygon-leg-subdivision-check.json').write_text(json.dumps({'figure':'5.3','degree':3,'knots':list(map(str,K)),'representative_controls':[[str(v) for v in p] for p in P],'exact_partition_and_squared_length_checks':30,'legs':partition,'detail_leg':3,'detail_uniform_enlargement':3,'detail_normalized_lengths':['1/3']*3},indent=2)+'\n')
print('PASS:10 exact leg partitions and30 squared-length identities, including repeated-knot zero intervals; detail enlarged3 times.')
