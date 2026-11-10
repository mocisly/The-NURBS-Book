"""9.28: rational symmetric example of Eq9.46..50, with truly equal speed arrows."""
from pathlib import Path
from fractions import Fraction as F
import json
from native_bspline import segments,check,cubic_path,point,de_boor
from bspline_math import derivative,evaluate
from local_quadratic_interpolator import add,mul,dot
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_34.tex')['applied']
A=(F(0),F(0));B=(F(26,5),F(0));Ts=(F(3,5),F(4,5));Te=(F(3,5),-F(4,5));alpha=F(6)
P=(A,add(A,Ts,alpha/3),add(B,Te,-alpha/3),B);K=(F(0),)*4+(F(1),)*4
ss=segments(K,P,3);nc=check(K,P,3,ss);power=ss[0]['power']
values=[]
for u in (F(0),F(1,2),F(1)):
    C=de_boor(K,P,3,u);D=tuple(evaluate(derivative(p),u) for p in power)
    assert dot(D,D)==alpha*alpha;values.append((u,C,D))
assert values[0][2]==mul(Ts,alpha) and values[-1][2]==mul(Te,alpha)
delta=add(B,A,-1);Tsum=add(Ts,Te);a=16-dot(Tsum,Tsum);b=12*dot(delta,Tsum);c=-36*dot(delta,delta)
assert a*alpha*alpha+b*alpha+c==0 and a>0 and c<0
levels=[P]
while len(levels[-1])>1:levels.append(tuple(mul(add(x,y),F(1,2)) for x,y in zip(levels[-1],levels[-1][1:])))
assert levels[3][0]==values[1][1]
assert add(levels[2][1],levels[3][0],-1)==mul(add(add(P[3],P[2]),add(P[1],P[0]),-1),F(1,8))
assert values[1][2]==mul(add(levels[2][1],levels[3][0],-1),6)
out=['% Exact symmetric cubic: alpha6,Ts(3/5,4/5),Te(3/5,-4/5),endpoint distance26/5.',r'\begin{tikzpicture}[book line,x=2.8cm,y=2.8cm]',r'\path[use as bounding box] (-.7,-3) rectangle (8,3.2);',r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';']
out.extend(cubic_path(s) for s in ss)
for i,(q,anchor) in enumerate(zip(P,('below left','left','above','above right'))):
    out.extend([r'\draw '+point(q)+r' circle[radius=2.4pt];',r'\node['+anchor+r'=6pt] at '+point(q)+r' {$\mathbf P_'+str(i)+'$};'])
for u,C,D in values:
    end=add(C,D,F(1,2));out.append(r'\draw[book axis] '+point(C)+'--'+point(end)+';')
    if u==0:out.append(r'\node[above right=6pt] at '+point(end)+r" {$\mathbf C'(0)$};")
    elif u==1:out.append(r'\node[below left=6pt] at '+point(end)+r" {$\mathbf C'(1)$};")
    else:
        out.extend([r'\draw '+point(C)+r' circle[radius=2.4pt];',r"\node at (4.8,1.55) {$\mathbf C'(1/2)$};"])
out.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_34.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/'image_tex/build/equal-three-speeds-cubic-check.json').write_text(json.dumps(dict(figure='9.28',controls=[list(map(str,p)) for p in P],unit_end_tangents=[list(map(str,p)) for p in (Ts,Te)],alpha=str(alpha),quadratic_9_50_coefficients=list(map(str,(a,b,c))),positive_root_exact=True,three_samples=[dict(u=str(u),position=list(map(str,C)),derivative=list(map(str,D)),squared_speed=str(dot(D,D))) for u,C,D in values],deCasteljau_equations_9_48_and_9_49_exact=True,all_arrow_scale='1/2',native_checks=nc),indent=2)+'\n')
print('PASS9.28:exact positive alpha6 root,all three speeds6,all arrows common1/2,deCasteljau9.48/49identities and native cubic41checks.')
