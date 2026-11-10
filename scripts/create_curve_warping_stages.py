from pathlib import Path
from fractions import Fraction as F
import json
from curve_warping_data import *
from native_bspline import check,cubic_path,point
root=Path(__file__).resolve().parents[1];R=warp();L,S,removal=simplify(R);states=[(U,P),(K,Q),(K,R),(L,S)];nc=0;panels=[]
for index,(V,C)in enumerate(states):
    ss=segments(V,C,3);nc+=check(V,C,3,ss,steps=7);out=[r'\begin{scope}[x=4cm,y=4cm]',r'\path[use as bounding box] (-.18,-.35) rectangle (4.18,1.45);']
    out.append(r'\draw[book grid,dashed] '+'--'.join(point(p)for p in C)+';');out.extend(cubic_path(s)for s in ss)
    if index>=2:out.extend(cubic_path(s,'book grid,dotted')for s in segments(U,P,3))
    for p in C:out.append(r'\draw '+point(p)+r' circle[radius=1.3pt];')
    for t,label,anchor in[(US,r'C(u_s)','below right'),(UE,r'C(u_e)','below left')]:
        p=de_boor(U,P,3,t);out.append(r'\draw '+point(p)+r' rectangle ++(.025,.025) node['+anchor+r'=6pt] {$'+label+'$};')
    if index==0:out.extend([r'\draw[book axis] (2,1)--(2,.4) node[midway,right=5pt] {$d$};',r'\node[below=5pt] at (2,.4) {$W$};'])
    out.extend([r'\node at (2,-.28) {('+chr(97+index)+')};',r'\end{scope}']);panels.append(out)
for num,pair in[(21,(0,1)),(22,(2,3))]:
    lines=['% Four actual stages, redistributed as AB/CD to preserve one coherent printed figure.',r'\begin{tikzpicture}[book line,font=\fontsize{10}{12}\selectfont]']
    for j,i in enumerate(pair):lines+=[r'\begin{scope}[xshift='+str(18*j)+'cm]']+panels[i]+[r'\end{scope}']
    lines.append(r'\end{tikzpicture}');(root/f'image_tex/ch11/fig_11_{num:02}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/curve-warping-stages-check.json').write_text(json.dumps(dict(original_knots=U,original_controls=P,refined_knots=K,refined_controls=Q,modified_controls=R,parameter_interval=(US,UE),eligible_control_indices=ELIGIBLE,chord_parameters=PARAMS,refinement_whole_power_identities=identities,warp_weight=1,maximum_control_displacement=F(3,5),direction=(0,-1),final_knots=L,final_controls=S,removal=removal,native_checks=nc,no_contour_tracing=True),default=str,indent=2)+'\n',encoding='utf-8');print('PASS11.19',nc,'nativechecks,',identities,'whole refinement coefficients; controls',len(P),len(Q),len(R),len(S),'bound',removal['certified_whole_domain_L1_error_bound_cm'])
