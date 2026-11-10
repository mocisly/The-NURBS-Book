from pathlib import Path
from fractions import Fraction as F
import json
from unclamp_algorithm import left_stages
from unclamped_geometry import verified_segments
from native_bspline import point,segments
from native_polynomial_drawing import paths
root=Path(__file__).resolve().parents[1]
K=(F(0),)*5+(F(1,4),F(1,2),F(3,4))+(F(1),)*5
P=tuple(tuple(F(str(x))for x in p)for p in[(0,1),(-.05,1.25),(.1,1.6),(.9,1.6),(2,-.4),(3,-.6),(3.7,-.2),(3.7,.6)])
FINAL,Q,STAGES=left_stages(K,P,4);reference,n=verified_segments(K,P,4);checks=n
# Intermediate states are the work arrays of A12.1, not complete knot/control representations.
# The fixed reference curve shows which geometry the eventual construction preserves.
ss,c=verified_segments(FINAL,Q,4);checks+=c;assert all(a['power']==b['power']for a,b in zip(ss,reference));identities=4*5
SCALE=F(14,5)
def view(p):return tuple(SCALE*x for x in p)
reports=[]
for source,panels in[(5,[0]),(6,[1,2]),(7,[3])]:
    xmax=F(43,10)*SCALE+F(31,2)*(len(panels)-1)
    out=[r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]',r'\path[use as bounding box] '+point((-F(3,5)*SCALE,-F(17,10)*SCALE))+' rectangle '+point((xmax,2*SCALE))+';']
    for local,j in enumerate(panels):
        controls=P if j==0 else STAGES[j-1]['controls'];out.append(r'\begin{scope}[xshift='+str(float(F(31,2)*local))+'cm]')
        out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(q))for q in controls)+';')
        draw,report=paths([dict(bern=tuple(view(q)for q in s['bern']))for s in reference],tolerance=F(1,100000));reports.append(report);out.extend(draw)
        for i,q in enumerate(controls):
            anchor={0:'below right=7pt',1:'left=7pt',2:'above left=7pt',3:'above right=7pt',4:'below left=7pt',5:'below=7pt',6:'right=7pt',7:'above=7pt'}[i]
            if j==3 and i==0:anchor='right=9pt'
            label='P_'+str(i)+(('^{'+str(j-1)+'}')if j and i<j else'')
            out.append(r'\draw[book grid] '+point(view(q))+r' circle[radius=1.6pt] node['+anchor+r'] {$'+label+'$};')
        out.append(r'\node at '+point(view((F(37,20),-F(3,2))))+' {('+chr(97+j)+')};');out.append(r'\end{scope}')
    out.append(r'\end{tikzpicture}');(root/f'image_tex/ch12/fig_12_{source:02d}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/quartic-unclamping-stages-check.json').write_text(json.dumps(dict(original_knots=K,original_controls=P,states=STAGES,final_left_unclamped_knots=FINAL,whole_vector_coefficient_identities=identities,exact_back_substitution_vector_identities=6,exact_curve_checks=checks,native_render_bounds=reports,intermediate_knots_are_algorithm_work_arrays=True,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS exactA12.1left i0/1/2,6backsubstitutionidentities,20WHOLE finalquarticvectorcoefficients; certifiedphysical cubic rendering1e-5cm')
