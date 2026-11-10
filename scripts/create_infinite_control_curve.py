"""7.14: actual cubic NURBS with one zero-weight homogeneous control/vector."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import approximate,project

root=Path(__file__).resolve().parents[1];manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in manifest['images'] if e['tex']=='image_tex/ch07/fig_7_14.tex')['applied']
U=(F(0),)*4+(F(3,10),F(7,10))+(F(1),)*4
P=tuple(tuple(map(F,p)) for p in [(10,0),(8,5),(0,0),(2,F(26,5)),(F(7,2),0),(0,0)])
vector=(F(4),F(2));H=tuple(pt+(F(1),) if i!=2 else vector+(F(0),) for i,pt in enumerate(P))
HB=tuple(h if i!=2 else (F(0),F(0),F(0)) for i,h in enumerate(H))
ss=segments(U,H,3);bs=segments(U,HB,3);nativechecks=check(U,H,3,ss)+check(U,HB,3,bs)
lower=min(pt[-1] for s in ss for pt in s['bern']);assert lower>0
Ns=tuple((F(i==2),) for i in range(6));checks=0
for i in range(101):
    u=F(i,100);h=de_boor(U,H,3,u);hb=de_boor(U,HB,3,u);N2=de_boor(U,Ns,3,u)[0]
    assert h[-1]==hb[-1]==1-N2 and h[-1]>=lower
    C,CB=project(h),project(hb);f=N2/h[-1];assert f>=0
    assert C==tuple(a+f*v for a,v in zip(CB,vector))
    lambdas=[]
    for j in (0,1,3,4,5):
        basis=de_boor(U,tuple((F(k==j),) for k in range(6)),3,u)[0]/h[-1];lambdas.append((j,basis))
    assert all(w>=0 for _,w in lambdas) and sum(w for _,w in lambdas)==1
    assert CB==tuple(sum(w*P[j][d] for j,w in lambdas) for d in range(2));checks+=1
touch=[]
for t,(i,j) in [(F(3,10),(1,3)),(F(7,10),(3,4))]:
    B=project(de_boor(U,HB,3,t));a,b=P[i],P[j]
    assert (B[0]-a[0])*(b[1]-a[1])==(B[1]-a[1])*(b[0]-a[0])
    assert all(min(x,y)<=z<=max(x,y) for x,y,z in zip(a,b,B));touch.append({'u':str(t),'finite_edge':[i,j],'point':list(map(str,B))})
u=F(3,10);CB=project(de_boor(U,HB,3,u));C=project(de_boor(U,H,3,u));f=de_boor(U,Ns,3,u)[0]/de_boor(U,H,3,u)[-1]
lines=['% Representative cubic U0quad,.3,.7,1quad with H2=(4,2,0), all other weights1.',
       '% Cbar excludes the infinite-control numerator; exact C=Cbar+(N2/W)*vectorP2.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-1,-1.1) rectangle (14.4,9.2);',
       r'\draw[book grid] '+point(P[0])+'--'+point(P[1])+';',
       r'\draw[book grid,densely dotted] '+point(P[1])+'--'+point(P[3])+';',
       r'\draw[book grid] '+point(P[3])+'--'+point(P[4])+'--'+point(P[5])+';']
proofs=[]
for which,pieces,style in [('finite',bs,'densely dashed'),('full',ss,'')]:
    paths=[p for s in pieces for p in approximate(s['bern'],F(1,100000))]
    lines.extend(cubic_path(p,style) for p in paths)
    proofs.append({'curve':which,'native_paths':len(paths),'certified_L1_error':str(max(p['certified_l1_error'] for p in paths))})
for j in (1,3):
    tip=tuple(a+b for a,b in zip(P[j],vector))
    lines.append(r'\draw[book axis,book grid] '+point(P[j])+'--'+point(tip)+(r' node[right=7pt] {$\overrightarrow{\mathbf P}_2$}' if j==1 else '')+';')
lines.append(r'\draw[book axis] '+point(CB)+'--'+point(C)+';')
for j,anchor in [(0,'below right'),(1,'below right'),(3,'above left'),(4,'below right'),(5,'below left')]:
    lines.append(r'\draw '+point(P[j])+r' circle[radius=2pt] node['+anchor+r'=6pt] {$\mathbf P_'+str(j)+'$};')
lines += [r'\draw '+point(CB)+r' circle[radius=2pt] node[below=8pt] {$\overline{\mathbf C}(u)$};',
          r'\draw '+point(C)+r' circle[radius=2pt] node[above=8pt] {$\mathbf C(u)$};',r'\end{tikzpicture}']
(root/'image_tex/ch07/fig_7_14.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/infinite-control-curve-check.json').write_text(json.dumps({'figure':'7.14','knots':list(map(str,U)),'homogeneous_controls':[[str(x) for x in h] for h in H],'infinite_vector':list(map(str,vector)),'whole_domain_denominator_Bernstein_lower_bound':str(lower),'native_checks':nativechecks,'exact_decomposition_and_finite_convex_combination_checks':checks,'finite_curve_exact_edge_touches':touch,'chosen_u':str(u),'chosen_f':str(f),'chosen_Cbar':list(map(str,CB)),'chosen_C':list(map(str,C)),'native_path_certificates':proofs},indent=2)+'\n')
print(f'PASS:{nativechecks}native checks,101exact decompositions/finite convex combinations;W>={lower}; both finite polygon touches exact.')
print('Chosen Cbar,C,f:'+str((tuple(map(float,CB)),tuple(map(float,C)),float(f))))
