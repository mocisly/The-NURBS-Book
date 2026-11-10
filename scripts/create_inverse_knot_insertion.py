"""Fig5.8: editable symbolic leg and independently checked inverse insertion."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import point,de_boor,segments,check
from rational_geometry import project
from knot51_data import insert

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch05/fig_5_09.tex';assert not target.exists()
# Concrete verification of Eq5.19--5.21; the drawing retains symbolic knot labels.
U=tuple(map(F,[0,0,0,0,1,2,3,4,5,5,5,5]));i=4
P=tuple(tuple(F(c) for c in p) for p in [(0,0),(1,1),(2,3),(3,4),(6,4),(8,2),(9,0),(10,0)])
tests=[];native=0
for wa,wb in [(F(1),F(1)),(F(2),F(3)),(F(5),F(1,2))]:
    w=[F(1)]*8;w[i-1],w[i]=wa,wb
    H=tuple(tuple(c*w[j] for c in p)+(w[j],) for j,p in enumerate(P))
    for lam in (F(1,10),F(1,3),F(11,20),F(9,10)):
        # Distances on the same leg have a common factor, so lambda is exact.
        Q=tuple((1-lam)*a+lam*b for a,b in zip(P[i-1],P[i]))
        s=wa*lam/(wa*lam+wb*(1-lam));ubar=U[i]+s*(U[i+3]-U[i])
        assert project(tuple((1-s)*a+s*b for a,b in zip(H[i-1],H[i])))==Q
        V,R,alpha=insert(U,H,3,ubar);assert alpha[i]==s and project(R[i])==Q
        for j in range(41):assert de_boor(U,H,3,F(j,8))==de_boor(V,R,3,F(j,8))
        native+=check(V,R,3,segments(V,R,3),steps=7)
        tests.append({'endpoint_weights':list(map(str,(wa,wb))),'euclidean_leg_fraction':str(lam),'homogeneous_fraction':str(s),'inserted_parameter':str(ubar),'new_control_projects_to_selected_point':True})
lines=['% Fig5.8: symbolic cubic inverse-knot-insertion leg; editable line/point/math nodes.',
       '% Knot ticks are schematic, not a numerical ruler for arbitrary unequal weights.',
       '% Equations5.19--5.21 independently verified with12 positive-weight insertion cases.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]',
       r'\path[use as bounding box] (-2.6,-1.1) rectangle (10.9,3.7);',
       r'\draw (-2,-.65)--(0,2.5)--(8,2.5)--(10.2,-.65);',
       r'\draw (0,2.5) circle[radius=2.2pt];',r'\draw (8,2.5) circle[radius=2.2pt];',
       r'\draw (4.4,2.5) circle[radius=1.7pt];',
       r'\node[above=7pt] at (0,2.5) {$\mathbf P_{i-1}$};',
       r'\node[above=7pt] at (8,2.5) {$\mathbf P_i$};',
       r'\node[above=7pt] at (4.4,2.5) {$\mathbf Q$};',
       r'\node[below right=6pt] at (0,2.5) {$u_i$};',
       r'\node[below left=6pt] at (8,2.5) {$u_{i+3}$};',
       r'\draw[book grid] (2,2.32)--(2,2.68);',
       r'\draw[book grid] (6,2.32)--(6,2.68);',
       r'\node[below=6pt] at (2,2.32) {$u_{i+1}$};',
       r'\node[below=6pt] at (6,2.32) {$u_{i+2}$};',
       r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/inverse-knot-insertion-check.json').write_text(json.dumps({'figure':'5.8','symbolic_schematic':True,'degree':3,'inverse_insertion_cases':tests,'exact_deboor_curve_invariance_points':492,'exact_native_homogeneous_curve_checks':native,'note':'For unequal weights use homogeneous fraction s, not the Euclidean leg fraction; symbolic knot ticks are not a metric ruler.'},indent=2)+'\n')
print(f'PASS:12 exact weighted inverse insertions,492 curve-invariance points,{native} homogeneous span checks.')
