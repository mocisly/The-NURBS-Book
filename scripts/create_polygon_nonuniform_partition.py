"""Fig5.4: same Fig5.3 polygon, genuinely different nonuniform knot partitions."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point,number
from polygon_leg_data import P,NONUNIFORM as K

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_05.tex';assert not target.exists()
previous=json.loads((root/'image_tex/build/polygon-leg-subdivision-check.json').read_text())
assert previous['representative_controls']==[[str(c) for c in p] for p in P]
lines=['% Fig5.4: exact SAME representative polygon as5.3; specified nonuniform knot vector.',
       '% Each cut is the normalized cumulative knot length; no interpolation from raster positions.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',r'\path[use as bounding box] (-1,-2.2) rectangle (12,6.4);',
       r'\draw[book line] '+'--'.join(map(point,P))+';']
partitions=[]
for i in range(1,len(P)):
    lam=tuple((K[i+j+1]-K[i+j])/(K[i+3]-K[i]) for j in range(3));assert min(lam)>=0 and sum(lam)==1
    points=[tuple((1-sum(lam[:j]))*a+sum(lam[:j])*b for a,b in zip(P[i-1],P[i])) for j in range(4)]
    for j in range(3):
        d=sum((a-b)**2 for a,b in zip(P[i-1],P[i]));dj=sum((a-b)**2 for a,b in zip(points[j],points[j+1]));assert dj==lam[j]**2*d
    for pt in sorted(set(points[1:3])-{P[i-1],P[i]}):lines.append(r'\draw '+point(pt)+' circle[radius=1.15pt];')
    partitions.append({'leg':i,'knots':list(map(str,K[i:i+4])),'normalized_lengths':list(map(str,lam)),'partition_points':[[str(c) for c in p] for p in points]})
for i,(p,anchor) in enumerate(zip(P,['below right','left','above left','above','right','left','below','below right','right','above right','above'])):
    lines += [r'\draw '+point(p)+' circle[radius=2pt];',r'\node['+anchor+'=5pt] at '+point(p)+r' {$\mathbf P_{'+str(i)+'}$};']
lines.append(r'\draw[book grid] (0,-1.5)--(11,-1.5);')
for t in sorted(set(K)):
    m=K.count(t)
    for j in range(m):
        x=F(11,7)*t+F(3,50)*(F(j)-F(m-1,2))
        lines.append(r'\draw[book grid] '+point((x,F(-8,5)))+'--'+point((x,F(-7,5)))+';')
    lines.append(r'\node[below=5pt] at '+point((F(11,7)*t,F(-3,2)))+' {$'+number(t)+'$};')
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/polygon-nonuniform-partition-check.json').write_text(json.dumps({'figure':'5.4','degree':3,'knots':list(map(str,K)),'same_controls_as5.3':True,'representative_controls':[[str(c) for c in p] for p in P],'exact_partition_and_squared_length_checks':30,'legs':partitions},indent=2)+'\n')
print('PASS:same11 controls as5.3;10 exact nonuniform partitions,30 squared-length identities.')
