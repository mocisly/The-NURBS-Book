"""Fig4.10(a,b): exact weighted tensor basis with unchanged polynomial marginals."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,point,cubic_path
from surface_geometry import extraction,weights
from rational_geometry import graph_controls,approximate,evaluate,project

root=Path(__file__).resolve().parents[1]
targets=[root/f'image_tex/ch04/fig_4_{n}.tex' for n in (10,11)]
assert not any(p.exists() for p in targets)
U=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
V=(F(0),)*3+tuple(F(i,5) for i in (1,2,3,3,4))+(F(1),)*3
camera_norm=F(53,10)
def f(u,v):return weights(U,3,u)[4]*weights(V,2,v)[2]
def rat(u,v,w):
    ff=f(u,v);return w*ff/(1+(w-1)*ff)
basis_checks=0
for k,i,p in [(U,4,3),(V,2,2)]:
    c=tuple((F(j==i),) for j in range(len(k)-p-1))
    basis_checks+=check(k,c,p,segments(k,c,p))
# These marginals are deliberately independent of w42, as in the original.
marginals=[]
for k,i,p,var in [(U,4,3,'u'),(V,2,2,'v')]:
    fixed=F(-9,10) if var=='u' else F(-9,20)
    origin=(F(0),fixed,F(0)) if var=='u' else (fixed,F(0),F(0))
    end=(F(23,20),fixed,F(0)) if var=='u' else (fixed,F(23,20),F(0))
    zend=(origin[0],origin[1],F(23,20))
    marginals += [r'\draw[book axis,book grid] '+point(origin)+'--'+point(end)+r' node['+('right' if var=='u' else 'below left')+'] {$'+var+'$};',
                  r'\draw[book axis,book grid] '+point(origin)+'--'+point(zend)+';',
                  r'\node['+('right' if var=='u' else 'left')+'] at '+point((origin[0],origin[1],F(1)))+' {$1$};',
                  r'\node[below=4pt] at '+point(origin)+' {$0$};']
    for t in sorted(set(k)):
        a=(t,fixed-F(1,100),F(0)) if var=='u' else (fixed-F(1,100),t,F(0))
        b=(t,fixed+F(1,100),F(0)) if var=='u' else (fixed+F(1,100),t,F(0))
        marginals.append(r'\draw[book grid] '+point(a)+'--'+point(b)+';')
    endpoint=(F(1),fixed,F(0)) if var=='u' else (fixed,F(1),F(0))
    marginals.append(r'\node[below=4pt] at '+point(endpoint)+' {$1$};')
    for span in range(p,len(k)-p-1):
        a,b=k[span:span+2]
        if a==b:continue
        B=extraction(k,p,span)
        controls=tuple((a+(b-a)*F(r,p),fixed,B[r][i]) if var=='u' else (fixed,a+(b-a)*F(r,p),B[r][i]) for r in range(p+1))
        marginals.append(cubic_path({'bern':controls}))
    for t in (F(0),F(1)):
        a=(t,fixed,F(0)) if var=='u' else (fixed,t,F(0))
        b=(t,F(0),F(0)) if var=='u' else (F(0),t,F(0))
        marginals.append(r'\draw[book grid,dashed] '+point(a)+'--'+point(b)+';')
marginals += [r'\node at (.72,-.9,.9) {$N_{4,3}(u)$};',r'\node at (-.45,.3,1) {$N_{2,2}(v)$};']
reports=[]
for target,tag,w in zip(targets,('a','b'),(F(2,5),F(6))):
    lines=['% Fig4.10('+tag+'): original cubic x quadratic basis, single weight w42='+str(w)+'.',
           '% R=w*f/(1+(w-1)*f), f=N4,3(u)*N2,2(v); other55 weights1.',
           '% Knots exactly as corrected Fig3.19(b); the two polynomial marginals remain UNWEIGHTED.',
           '% Same affine camera as Fig3.19, equal bounds/scales in(a),(b).',
           '% Native cubic approximations of mathematical rational isolines, certified screen error<=0.0001cm.',
           '% No sampled image contours or outline conversion.',
           r'\begin{tikzpicture}[x={(4cm,-1.3cm)},y={(-2.6cm,-1.8cm)},z={(0cm,3cm)},book line,line cap=round,line join=round]',
           r'\path[use as bounding box] (canvas cs:x=-5.5cm,y=-4.6cm) rectangle (canvas cs:x=7.5cm,y=5.5cm);']
    paths=graph_checks=0;maximum=F(0);partition=0
    for a in range(21):
        uu=F(a,20);nu=weights(U,3,uu)
        for b in range(21):
            vv=F(b,20);nv=weights(V,2,vv)
            D=sum(nu[i]*nv[j]*(w if (i,j)==(4,2) else 1) for i in range(7) for j in range(8))
            assert D==1+(w-1)*f(uu,vv) and min(F(1),w)<=D<=max(F(1),w)
            rr=[nu[i]*nv[j]*(w if (i,j)==(4,2) else 1)/D for i in range(7) for j in range(8)]
            assert min(rr)>=0 and sum(rr)==1 and rr[4*8+2]==rat(uu,vv,w)
            assert 0<=rat(uu,vv,F(2,5))<=rat(uu,vv,F(6))<=1
            if uu<=F(1,4) or vv>=F(3,5):assert rat(uu,vv,w)==0
            partition+=1
    for var,k,index,p in [('u',U,4,3),('v',V,2,2)]:
        for h in range(21):
            fixed=F(h,20)
            factor=weights(V,2,fixed)[2] if var=='u' else weights(U,3,fixed)[4]
            for span in range(p,len(k)-p-1):
                a,b=k[span:span+2]
                if a==b:continue
                B=extraction(k,p,span)
                A=tuple(w*factor*row[index] for row in B)
                D=tuple(1+(w-1)*factor*row[index] for row in B)
                assert min(D)>=min(F(1),w)>0
                G=graph_controls(a,b,A,D)
                H=tuple((x,fixed*ww,z,ww) if var=='u' else (fixed*ww,x,z,ww) for x,z,ww in G)
                for t in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
                    u=a+(b-a)*t;pt=project(evaluate(H,t))
                    expected=(u,fixed,rat(u,fixed,w)) if var=='u' else (fixed,u,rat(fixed,u,w))
                    assert pt==expected;graph_checks+=1
                for piece in approximate(H,F(1,10000)/camera_norm):
                    lines.append(cubic_path(piece,'book grid'))
                    paths+=1;maximum=max(maximum,piece['certified_l1_error']*camera_norm)
    lines.extend(marginals)
    wlabel=r'\frac25' if w==F(2,5) else '6'
    lines += [r'\node at (canvas cs:x=.5cm,y=-3.6cm) {$R_{4,2}(u,v),\quad w_{4,2}='+wlabel+'$};',
              r'\node at (canvas cs:x=.5cm,y=-4.15cm) {('+tag+')};',r'\end{tikzpicture}']
    target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    reports.append({'panel':tag,'w42':str(w),'rational_partition_grid_points':partition,
                    'exact_isograph_checks':graph_checks,'native_cubic_isograph_paths':paths,
                    'maximum_certified_projected_l1_error_cm':str(maximum),'denominator_bounds':[str(min(F(1),w)),str(max(F(1),w))]})
(root/'image_tex/build/rational-tensor-basis-check.json').write_text(json.dumps({
    'figure':'4.10','degrees':[3,2],'control_basis_count':[7,8],'U':list(map(str,U)),'V':list(map(str,V)),
    'target_basis':[4,2],'other_weights':1,'polynomial_marginal_checks':basis_checks,
    'same_unweighted_marginal_native_commands_in_both_panels':True,
    'rational_formula':'R42=w42*f/(1+(w42-1)*f), f=N4,3*N2,2',
    'support_rectangle':['1/4','1','0','3/5'],
    'weight_monotonicity':'dR/dw=f*(1-f)/(1+(w-1)*f)^2>=0',
    'marginal_plane_offsets':{'u':'-9/10','v':'-9/20'},'camera_l1_operator_norm':str(camera_norm),'panels':reports},indent=2)+'\n')
print('PASS:369 polynomial marginal checks; each panel441 partitions,945 exact rational graph checks; '+', '.join(f"{r['native_cubic_isograph_paths']} certified paths atw={r['w42']}" for r in reports)+'.')
