"""9.48: exact removable cubic double knot and its actual old basis domain."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,re
import image_tex as pipeline
from knot51_data import insert
from inverse_knot_projection import remove_to
from native_bspline import segments,check,cubic_path,point,de_boor
from bspline_math import piece,compose_affine,evaluate,basis
root=Path(__file__).resolve().parents[1];data=pipeline.load()
entry=next(e for e in data['images'] if '437_294_1248' in e['image']);assert not entry['applied']
chapter=root/'chapter/9.tex';text=chapter.read_text(encoding='utf-8')
html=re.search(r'<img[^\n]*437\.jpg[^\n]*/>',text);assert html
entry.update(chapter=9,chapter_file='chapter/9.tex',line=text[:html.start()].count('\n')+1,tex='image_tex/ch09/fig_9_48_html.tex',kind='html',original=html.group(),options=r'max width=\linewidth')
pipeline.save(data)
K=tuple(map(F,[0,0,0,0,1,2,3,4,5,6,7,8,8,8,8]))
R=tuple(tuple(map(F,p)) for p in [('0','0'),('-1','1'),('-1','2.5'),('0','4'),('2','4.7'),('3.6','4.3'),('4.8','2.4'),('3.4','1.1'),('5','0'),('7','0'),('8','1.6')])
U,P,alpha=insert(K,R,3,F(4));assert len(P)==12 and U[8]==4 and U.count(F(4))==2
V,C,proof=remove_to(U,P,3,(F(4),));assert V==K and C==R and proof['curve_exactly_unchanged']
left=tuple((P[5][d]-(1-alpha[5])*P[4][d])/alpha[5] for d in range(2))
right=tuple((P[6][d]-alpha[6]*P[7][d])/(1-alpha[6]) for d in range(2))
assert left==right==R[5]
assert tuple(sorted(set(U[5:11])))==tuple(map(F,[2,3,4,5,6]))
assert (U[6],U[10])==(3,6)
ss=segments(U,P,3);native=check(U,P,3,ss,steps=10)
assert all(de_boor(U,P,3,F(k,20))==de_boor(V,C,3,F(k,20)) for k in range(161))
def view(p):return (F(9,5)*p[0]+2,F(9,5)*p[1]+8)
out=['% Actual cubic one-time removal u8=4,s2;explicit representative controls,exact unchanged curve.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-1,-1) rectangle (19,18);']
out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern']))) for s in ss)
out.append(r'\draw[book grid] '+'--'.join(point(view(p)) for p in P)+';')
out.append(r'\draw[book grid,dashed] '+point(view(P[5]))+'--'+point(view(R[5]))+'--'+point(view(P[6]))+';')
out.extend(r'\draw '+point(view(p))+r' circle[radius=2.2pt];' for p in P)
out.append(r'\draw '+point(view(R[5]))+r' circle[radius=2.2pt];')
for idx,anchor in [(0,'below right'),(5,'above left'),(6,'right'),(11,'above')]:
    out.append(r'\node['+anchor+r'=6pt] at '+point(view(P[idx]))+r' {$\mathbf P_{'+str(idx)+r'}$};')
out.extend([r'\node (newpoint) at (12.4,16.9) {$\mathbf P^{\prime}_5=\mathbf P^{\prime}_6$};',r'\draw[book grid] (newpoint)--'+point(view(R[5]))+';'])
# Original-knot basis, including the exact dashed N6,3 with support[3,6].
checks=0
for i in range(12):
    for span in range(3,12):
        a,b=U[span:span+2]
        if a==b:continue
        coeff=piece(U,i,3,span)
        if not any(coeff):continue
        local=compose_affine(coeff,a,b-a)
        bern=tuple((2*(a+(b-a)*F(j,3)),4*sum((local[k] if k<len(local) else 0)*F(comb(j,k),comb(3,k)) for k in range(j+1))) for j in range(4))
        for k in range(11):
            t=F(k,11);u=a+(b-a)*t;q=list(bern)
            for _ in range(3):q=[tuple((1-t)*x+t*y for x,y in zip(c,d)) for c,d in zip(q,q[1:])]
            assert q[0]==(2*u,4*basis(U,i,3,u));checks+=1
        out.append(cubic_path(dict(bern=bern),style='book grid,dashed' if i==6 else 'book grid'))
for k in range(160):
    u=F(k,20);w=[basis(U,i,3,u) for i in range(12)];assert min(w)>=0 and sum(w)==1
out.extend([r'\draw[book grid,book axis] (-.3,0)--(18.3,0) node[right=4pt] {$u$};',r'\draw[book grid,book axis] (0,-.15)--(0,5.1);',r'\node[left=5pt] at (0,4) {$1$};',r'\node[above=5pt] at (8.7,3.05) {$N_{6,3}$};'])
for k in range(9):
    out.extend([r'\draw[book grid] '+point((2*k,-F(1,10)))+'--'+point((2*k,F(1,10)))+';',r'\node[below=6pt] at '+point((2*k,0))+' {$'+str(k)+'$};'])
for x in [-F(18,100),-F(6,100),F(6,100),F(18,100),F(16)-F(18,100),F(16)-F(6,100),F(16)+F(6,100),F(16)+F(18,100),F(8)-F(5,100),F(8)+F(5,100)]:
    out.append(r'\draw[book grid] '+point((x,-F(1,8)))+'--'+point((x,F(1,8)))+';')
out.extend([r'\draw[book grid] (6,0)--(6,4.65);',r'\draw[book grid] (12,0)--(12,4.65);',r'\draw[book grid,{Stealth[length=4pt]}-{Stealth[length=4pt]}] (6,4.45)--(12,4.45);',r'\node[above=5pt] at (9,4.45) {$\operatorname{supp}N_{6,3}=[3,6]$};',r'\end{tikzpicture}'])
(root/entry['tex']).write_text('\n'.join(out)+'\n',encoding='utf-8')
report=dict(figure='9.48',degree=3,original_knots=list(map(str,U)),coarse_knots=list(map(str,V)),original_controls=[list(map(str,p)) for p in P],coarse_controls=[list(map(str,p)) for p in C],representative_controls=True,one_time_removed_knot=4,old_r=8,old_s=2,two_inverse_candidates_exactly_coincide=True,exact_curve_removal=proof,old_basis_error_support=[3,6],new_Br_knots=[2,3,4,5,6],new_basis_parameter_index_ranges=[4,5,6],native_curve_checks=native,exact_basis_piece_checks=checks,old_basis_partition_samples=160,curve_invariance_samples=161)
(root/'image_tex/build/double-knot-removal-domain-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.48:exact unchanged cubic removal;inverse candidates coincide;old N6,3support3..6;newBr2..6/newN4..6;',checks,'basis checks.')
