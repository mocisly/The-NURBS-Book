"""9.50: computed bounded cubic fit,data and true parameter/control views."""
from pathlib import Path
from fractions import Fraction as F
import json
from bounded_curve_example_data import Q
from native_bspline import segments,check,cubic_path,point,de_boor,number
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_58.tex')['applied']
report=json.loads((root/'image_tex/build/bounded-wavy-curve-data.json').read_text(encoding='utf-8'))
U=tuple(map(F,report['knots']));P=tuple(tuple(map(F,p)) for p in report['controls']);params=tuple(map(F,report['parameters']))
ss=segments(U,P,3);native=check(U,P,3,ss,steps=9)
squares=tuple(sum((x-y)**2 for x,y in zip(q,de_boor(U,P,3,t))) for q,t in zip(Q,params))
assert max(squares)<=F(7,100)**2
assert any(U.count(t)==2 for t in set(U[4:-4])) and any(U.count(t)==1 for t in set(U[4:-4]))
out=['% A9.10stage structure with documented conservative exact L1datum error budgets;explicit81representative data.',r'\begin{tikzpicture}[book line,x=2.4cm,y=2.4cm]']
for letter,shift in [('a',21),('b',0)]:
    out.extend([r'\begin{scope}[yshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-.6,-1.6) rectangle (8.6,7);'])
    if letter=='b':out.append(r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';')
    out.extend(cubic_path(s) for s in ss)
    if letter=='a':
        out.extend(r'\draw '+point(q)+r' circle[radius=2pt];' for q in Q)
    else:
        for j in range(41):
            q=de_boor(U,P,3,F(j,40));out.extend([r'\draw[book grid] '+point(q)+r' ++(-2pt,0)--++(4pt,0);',r'\draw[book grid] '+point(q)+r' ++(0,-2pt)--++(0,4pt);'])
        out.append(r'\draw[book grid] (0,-1)--(8,-1);')
        for t in sorted(set(U)):
            m=U.count(t)
            for j in range(m):
                x=8*t+F(1,35)*(F(j)-F(m-1,2));out.append(r'\draw[book grid] '+point((x,-F(27,25)))+'--'+point((x,-F(23,25)))+';')
        out.extend([r'\node[below=4pt] at (0,-1.05) {$0$};',r'\node[below=4pt] at (8,-1.05) {$1$};',r'\node[above=4pt] at (4,-1) {$U$};'])
    out.extend([r'\node at (4,'+('-.65' if letter=='a' else '-1.5')+') {('+letter+')};',r'\end{scope}'])
out.append(r'\end{tikzpicture}')
(root/'image_tex/ch09/fig_9_58.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report.update(native_cubic_checks=native,actual_maximum_Euclidean_same_parameter_error=float(max(squares))**.5,parameter_crosses=[str(F(i,40)) for i in range(41)],all81datum_errors_certified_below_007=True,native_font_rescaling=False)
(root/'image_tex/build/bounded-wavy-curve-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.50native:',native,'exactBezierchecks;maximumEuclideanerror',report['actual_maximum_Euclidean_same_parameter_error'],'<=.07;actualmixedsimple/doubleknots.')
