"""Restore the11.14 raster equation as native editable math and check four-control formula."""
from pathlib import Path
from fractions import Fraction as F
import json
from point_relocation_example_data import U
from surface_geometry import weights,surface
root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'));assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch11/fig_11_08.tex')['applied']
g=tuple(sum(U[i+1:i+4])/3 for i in range(9));P=tuple(tuple((8*a,7*b,3*a*b) for b in g) for a in g);W=tuple(tuple(1+F(i,10)+F(j,20) for j in range(9)) for i in range(9));H=tuple(tuple(tuple(w*x for x in p)+(w,) for p,w in zip(row,ww)) for row,ww in zip(P,W))
u,v=F(43,100),F(3,5);a,b=weights(U,3,u),weights(U,3,v);den=sum(a[i]*b[j]*W[i][j] for i in range(9) for j in range(9));R=tuple(tuple(a[i]*b[j]*W[i][j]/den for j in range(9)) for i in range(9));assert sum(map(sum,R))==1
direction=(F(2,3),-F(1,3),F(2,3));assert sum(x*x for x in direction)==1;distance=F(7,5)
base=surface(U,U,3,3,H,u,v);old=tuple(x/base[-1] for x in base[:-1]);proof=[]
for delta,gamma in [(F(0),F(0)),(F(1),F(0)),(F(0),F(1)),(F(1),F(1)),(F(1,3),F(4,5)),(F(8,17),F(3,5))]:
    beta=((1-delta)*(1-gamma),delta*(1-gamma),(1-delta)*gamma,delta*gamma);assert sum(beta)==1 and min(beta)>=0
    indices=((3,4),(4,4),(3,5),(4,5));B=sum(c*R[i][j] for c,(i,j) in zip(beta,indices));assert B>0;alpha=distance/B
    Q=[[tuple(p) for p in row] for row in P]
    for c,(i,j) in zip(beta,indices):Q[i][j]=tuple(x+c*alpha*d for x,d in zip(Q[i][j],direction))
    G=tuple(tuple(tuple(w*x for x in p)+(w,) for p,w in zip(row,ww)) for row,ww in zip(Q,W));newh=surface(U,U,3,3,G,u,v);new=tuple(x/newh[-1] for x in newh[:-1]);assert newh[-1]==base[-1]
    assert tuple(y-x for x,y in zip(old,new))==tuple(distance*d for d in direction);assert sum((y-x)**2 for x,y in zip(old,new))==distance*distance
    proof.append(dict(delta=str(delta),gamma=str(gamma),basis_blend=str(B),alpha=str(alpha),squared_distance=str(distance*distance)))
formula=r'\alpha=\frac{d}{\lvert\mathbf V\rvert\bigl[(1-\delta)(1-\gamma)R_{k,\ell}(\bar u,\bar v)+\cdots+\delta\gamma R_{k+1,\ell+1}(\bar u,\bar v)\bigr]}'
out=['% Restored equation(11.14), matching the original scan and four movements(11.13).','% The omitted terms are delta*(1-gamma)*R_(k+1,l)+(1-delta)*gamma*R_(k,l+1).','% This node contains actual editable math;11pt matches the body and source has no tracing.',r'\begin{tikzpicture}[baseline=(formula.base)]',r'\node[inner sep=0pt,outer sep=0pt,font=\fontsize{11}{13.2}\selectfont] (formula) {$\displaystyle '+formula+'$};',r'\end{tikzpicture}']
(root/'image_tex/ch11/fig_11_08.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/restored-equation-11-14-check.json').write_text(json.dumps(dict(original_equation='11.14',native_editable_math=True,font_pt=11,ellipsis_middle_terms=['delta*(1-gamma)*R_(k+1,l)','(1-delta)*gamma*R_(k,l+1)'],general_nonuniform_positive_NURBS_weight_check=True,unit_3D_direction=list(map(str,direction)),exact_3D_surface_target_checks=proof,no_contour_tracing=True),indent=2)+'\n',encoding='utf-8');print('PASS equation11.14:6exactrationalNURBSfour-controltargetchecks/includescornercases;native11ptmath.')
