"""9.49: exact removal of one simple cubic knot, old basis support[2,6]."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json
from knot51_data import insert
from inverse_knot_projection import remove_to
from native_bspline import segments,check,cubic_path,point,de_boor
from bspline_math import piece,compose_affine,basis
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_57.tex')['applied']
K=tuple(map(F,[0,0,0,0,1,2,3,5,6,7,8,8,8,8]))
R=tuple(tuple(map(F,p)) for p in [('0','0'),('-1','1'),('-1','2.5'),('0','4'),('3','4.9'),('5','2.5'),('3.4','1.1'),('5','0'),('7','0'),('8','1.6')])
U,P,alpha=insert(K,R,3,F(4));assert len(P)==11 and U[7]==4 and U.count(F(4))==1
V,C,proof=remove_to(U,P,3,(F(4),));assert V==K and C==R and proof['curve_exactly_unchanged']
left=tuple((P[4][d]-(1-alpha[4])*P[3][d])/alpha[4] for d in range(2))
right=tuple((P[6][d]-alpha[6]*P[7][d])/(1-alpha[6]) for d in range(2))
assert left==R[4] and right==R[5]
assert P[5]==tuple((a+b)/2 for a,b in zip(left,right))
assert tuple(t for t in sorted(set(U[4:11])) if t!=4)==tuple(map(F,[1,2,3,5,6,7]))
assert (U[5],U[9])==(2,6)
ss=segments(U,P,3);native=check(U,P,3,ss,steps=10)
assert all(de_boor(U,P,3,F(k,20))==de_boor(V,C,3,F(k,20)) for k in range(161))
def view(p):return (F(9,5)*p[0]+2,F(9,5)*p[1]+8)
out=['% Actual single cubic knot removal4:r7,s1;explicit representative controls and exact curve invariance.',r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-1,-1) rectangle (19,18);']
out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern']))) for s in ss)
out.append(r'\draw[book grid] '+'--'.join(point(view(p)) for p in P)+';')
out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(p)) for p in (P[4],left,right,P[6]))+';')
out.extend(r'\draw '+point(view(p))+r' circle[radius=2.2pt];' for p in P)
out.extend(r'\draw '+point(view(p))+r' circle[radius=2.2pt];' for p in (left,right))
for idx,anchor in [(0,'below right'),(4,'above left'),(5,'right'),(6,'below right'),(10,'above')]:
    out.append(r'\node['+anchor+r'=6pt] at '+point(view(P[idx]))+r' {$\mathbf P_{'+str(idx)+r'}$};')
out.extend([r'\node[above=6pt] at '+point(view(left))+r" {$\mathbf P^{\prime}_4$};",r'\node[right=6pt] at '+point(view(right))+r" {$\mathbf P^{\prime}_6$};"])
checks=0
for i in range(11):
    for span in range(3,11):
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
        out.append(cubic_path(dict(bern=bern),style='book grid,dashed' if i==5 else 'book grid'))
for k in range(160):
    w=[basis(U,i,3,F(k,20)) for i in range(11)];assert min(w)>=0 and sum(w)==1
out.extend([r'\draw[book grid,book axis] (-.3,0)--(18.3,0) node[right=4pt] {$u$};',r'\draw[book grid,book axis] (0,-.15)--(0,5.1);',r'\node[left=5pt] at (0,4) {$1$};',r'\node[above=5pt] at (8,3.05) {$N_{5,3}$};'])
for k in range(9):
    out.extend([r'\draw[book grid] '+point((2*k,-F(1,10)))+'--'+point((2*k,F(1,10)))+';',r'\node[below=6pt] at '+point((2*k,0))+' {$'+str(k)+'$};'])
for x in [-F(18,100),-F(6,100),F(6,100),F(18,100),F(16)-F(18,100),F(16)-F(6,100),F(16)+F(6,100),F(16)+F(18,100)]:
    out.append(r'\draw[book grid] '+point((x,-F(1,8)))+'--'+point((x,F(1,8)))+';')
out.extend([r'\draw[book grid] (4,0)--(4,4.65);',r'\draw[book grid] (12,0)--(12,4.65);',r'\draw[book grid,{Stealth[length=4pt]}-{Stealth[length=4pt]}] (4,4.45)--(12,4.45);',r'\node[above=5pt] at (8,4.45) {$\operatorname{supp}N_{5,3}=[2,6]$};',r'\end{tikzpicture}'])
(root/'image_tex/ch09/fig_9_57.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report=dict(figure='9.49',degree=3,old_knots=list(map(str,U)),new_knots=list(map(str,V)),original_controls=[list(map(str,p)) for p in P],new_controls=[list(map(str,p)) for p in C],representative_controls=True,old_r=7,old_s=1,middle_control_exactly_midpoint_of_inverse_candidates=True,exact_curve_removal=proof,old_basis_error_support=[2,6],new_Br_knots=[1,2,3,5,6,7],new_basis_parameter_index_ranges=[3,4,5,6],native_curve_checks=native,exact_basis_checks=checks,partition_samples=160,curve_invariance_samples=161,same_geometry_font_as='9.48')
(root/'image_tex/build/single-knot-removal-domain-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.49:exact simple4removal;middlecontrolcandidate midpoint;support2..6;updatedBr1/2/3/5/6/7,newN3..6;',checks,'basis checks.')
