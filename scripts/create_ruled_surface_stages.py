"""8.5a-e: real elevation/refinement states and equal-parameter rulings."""
from pathlib import Path
from fractions import Fraction as F
import json
from ruled_surface_data import U1,U2,P1,P2,E1,Q1,Q2,U,V,R1,R2,NET,elevation,camera
from native_bspline import segments,check,de_boor,cubic_path,point
from surface_geometry import surface,verify_tensor
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (5,6,7,8):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch08/fig_8_{n:02d}.tex')['applied']
states=[(U1,P1,2),(U2,P2,3),(E1,Q1,3),(U,R1,3),(U,R2,3)];checks=0;identities=[]
for K,P,p in states:checks+=check(K,P,p,segments(K,P,p))
for K,P,p,oldK,oldP,oldp in [(E1,Q1,3,U1,P1,2),(U,R1,3,U1,P1,2),(U,R2,3,U2,P2,3)]:
    old=segments(oldK,oldP,oldp)
    for new in segments(K,P,p):
        before=next(s for s in old if s['a']<=new['a'] and new['b']<=s['b'])
        assert all(tuple(a)+(F(0),)*(p-oldp)==tuple(b) for a,b in zip(before['power'],new['power']))
    for i in range(201):assert de_boor(K,P,p,F(i,200))==de_boor(oldK,oldP,oldp,F(i,200))
    identities.append({'degree':p,'control_count':len(P),'all_original_global_power_coefficients_unchanged':True,'exact_same_u_checks':201})
tensorchecks=verify_tensor(U,V,3,1,NET)
for i in range(21):
    u=F(i,20);a=de_boor(U1,P1,2,u);b=de_boor(U2,P2,3,u)
    for j in range(21):
        v=F(j,20);assert surface(U,V,3,1,NET,u,v)==tuple((1-v)*x+v*y for x,y in zip(a,b))
def axes():
    lines=[]
    for end,label,anchor in [((F(3),0,0),'x','below left'),((0,F(27,10),0),'y','right'),((0,0,F(9,2)),'z','above')]:lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+label+'$};')
    return lines
def base(label):return [r'\begin{scope}',r'\path[use as bounding box] (-6.2,-6.4) rectangle (6.9,11.9);']
def finish(lines,label):return lines+axes()+[r'\node at (.35,-6) {('+label+')};',r'\end{scope}']
def polygon(P,style='book grid'):return r'\draw['+style+'] '+'--'.join(point(camera(p)) for p in P)+';'
def curves():
    return [cubic_path(s) for K,P,p in [(U1,P1,2),(U2,P2,3)] for s in segments(K,tuple(map(camera,P)),p)]
anchors1=['left','below','below right','above left','above right','right']
anchors2=['below left','above left','above','below','below right','above right']
def mark(P,letter,family,indices,anchors=None):
    lines=[]
    for i,p in enumerate(P):
        lines.append(r'\fill '+point(camera(p))+r' circle[radius=1.5pt];')
        if i in indices:
            if anchors:anchor=anchors[i]
            else:
                y=camera(p)[1];anchor='above left' if family==1 and i>=len(P)//2 else 'below' if family==1 else 'above' if i<len(P)//2 else 'below right'
                if i==0:anchor='left' if family==1 else 'below left'
                if i==len(P)-1:anchor='right' if family==1 else 'above right'
                if letter=='Q' and family==1 and i==4:anchor='right'
                if letter=='R' and family==2 and i==2:anchor='left'
            lines.append(r'\node['+anchor+r'=7pt] at '+point(camera(p))+' {$\\mathbf '+letter+'_{'+str(i)+'}^{'+str(family)+'}$};')
    return lines
panels=[]
lines=base('a')+[polygon(P1),polygon(P2)]+curves()+mark(P1,'P',1,range(6),anchors1)+mark(P2,'P',2,range(6),anchors2);panels.append(finish(lines,'a'))
lines=base('b')+[polygon(P1,'book grid,dashed'),polygon(Q1),polygon(Q2)]+curves()+mark(Q1,'Q',1,[0,2,4,6,9])+mark(Q2,'Q',2,range(6),anchors2);panels.append(finish(lines,'b'))
lines=base('c')+[polygon(Q1,'book grid,dashed'),polygon(Q2,'book grid,dashed'),polygon(R1),polygon(R2)]+curves()+mark(R1,'R',1,[0,2,5,7,9,11])+mark(R2,'R',2,[0,2,5,7,9,11]);panels.append(finish(lines,'c'))
lines=base('d')+[polygon(R1,'book grid,dashed'),polygon(R2,'book grid,dashed')]
for a,b in NET:lines.append(r'\draw[book grid,dashed] '+point(camera(a))+'--'+point(camera(b))+';')
for j,P in enumerate((R1,R2)):
    for i,p in enumerate(P):
        lines.append(r'\fill '+point(camera(p))+r' circle[radius=1.5pt];')
        if i in (0,3,8,11):
            anchor='above left' if j==0 else 'below right'
            if j==0 and i==11:anchor='above right'
            lines.append(r'\node['+anchor+r'=7pt] at '+point(camera(p))+' {$\\mathbf S_{'+str(i)+','+str(j)+'}$};')
panels.append(finish(lines,'d'))
lines=base('e')
for i in range(31):
    u=F(i,30);a=de_boor(U,R1,3,u);b=de_boor(U,R2,3,u)
    lines.append(r'\draw['+('book line' if i in (0,30) else 'book grid')+'] '+point(camera(a))+'--'+point(camera(b))+';')
lines+=curves();panels.append(finish(lines,'e'))
for n,ll in [(5,panels[0]),(6,panels[1]+[r'\begin{scope}[xshift=15.7cm]']+panels[2]+[r'\end{scope}']),(7,panels[3]),(8,panels[4])]:
    (root/f'image_tex/ch08/fig_8_{n:02d}.tex').write_text('% Exact8.5stages,explicit representative3Dcontrols,unitweights. No outline or bitmap tracing.\n'+r'\begin{tikzpicture}[book line]'+'\n'+'\n'.join(ll)+'\n'+r'\end{tikzpicture}'+'\n',encoding='utf-8')
(root/'image_tex/build/ruled-surface-stages-check.json').write_text(json.dumps({'figure':'8.5','representative_controls_1':[[str(x) for x in p] for p in P1],'representative_controls_2':[[str(x) for x in p] for p in P2],'unit_weights':True,'input_degrees':[2,3],'input_knots_1':list(map(str,U1)),'corrected_clamped_cubic_input_knots_2':list(map(str,U2)),'elevated_knots_1':list(map(str,E1)),'common_knots':list(map(str,U)),'stage_control_counts':{'a':[6,6],'b':[10,6],'c':[12,12],'d':[12,2]},'degree_elevation_proof':elevation,'curve_invariance':identities,'native_curve_checks':checks,'exact_tensor_checks':tensorchecks,'exact_equal_u_linear_ruling_checks':441,'plotted_generator_parameter_grid':'u=i/30,not equal arc length','camera_common_all_five_panels':True,'cubic_endpoint_multiplicity_OCR_corrected_to4_each':True},indent=2)+'\n')
print('PASS:exact degree elevation/merged-knot coefficient identities,603same-u checks,441tensor/ruling checks;actual6/10/12control stages and corrected4/4cubic endpoint knots.')
