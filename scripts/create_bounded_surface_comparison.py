"""9.52: five coherent native panels from actual bounded tensor calculations."""
from pathlib import Path
from fractions import Fraction as F
import json
from bounded_surface_example_data import Q
from bounded_surface_approximation import VP
from surface_geometry import isocurve,surface
from native_bspline import segments,check,cubic_path,point,de_boor
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (60,61,62):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n}.tex')['applied']
report=json.loads((root/'image_tex/build/bounded-surface-comparison-data.json').read_text());assert [p['letter'] for p in report['panels']]==list('bcde')
nets={r['letter']:(tuple(map(F,r['U'])),tuple(map(F,r['V'])),*r['degrees'],tuple(tuple(tuple(map(F,p)) for p in row) for row in r['controls'])) for r in report['panels']}
def view(p):
    x,y,z=p;return(2*(-F(4,5)*x+F(9,10)*y),2*(-F(2,5)*x-F(7,20)*y+z))
proof=[]
def panel(letter,shift):
    out=[r'\begin{scope}[xshift='+str(float(shift))+r'cm]',r'\path[use as bounding box] (-7.6,-4) rectangle (7.6,11);'];native=iso=0
    if letter!='a':
        net=nets[letter];fixed=tuple(sorted(set(tuple(F(i,32) for i in range(33))+VP)))
        for v in fixed:
            K,p,C=isocurve(*net,'u',v);ss=segments(K,C,p);native+=check(K,C,p,ss,steps=4)
            for u in (F(0),F(1,3),F(2,3),F(1)):
                assert de_boor(K,C,p,u)==surface(*net,u,v);iso+=1
            out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern']))) for s in ss)
        if letter in 'cde':
            for boundary in (Q[0],Q[-1],tuple(row[0] for row in Q),tuple(row[-1] for row in Q)):
                out.append(r'\draw[book grid,dashed] '+'--'.join(point(view(p)) for p in boundary)+';')
        labels={'b':r'$(2,2),\ E=0$','c':r'$(2,2),\ E=1/2$','d':r'$(2,2),\ E=1$','e':r'$(3,3),\ E=1$'}
        out.append(r'\node at (0,10.55) {'+labels[letter]+'};')
    out.extend(r'\fill '+point(view(p))+r' circle[radius=.8pt];' for row in Q for p in row)
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(9,2)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(view(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out.extend([r'\node at (0,-3.55) {('+letter+')};',r'\end{scope}'])
    proof.append(dict(panel=letter,native_curve_checks=native,isocurve_tensor_crosschecks=iso,actual_data_count=169,common_camera_scale=2,font_rescaling=False))
    return out
for n,letters in [(60,'ab'),(61,'cd'),(62,'e')]:
    out=['% Same169explicit data/commonmeshparameters/camera/font for ALL panels;real degree/tolerance constructions.',r'\begin{tikzpicture}[book line]']
    for i,letter in enumerate(letters):out+=panel(letter,F(33,2)*i)
    out.append(r'\end{tikzpicture}');(root/f'image_tex/ch09/fig_9_{n}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report.update(native_panels=proof,no_contour_tracing=True,layout='ABhorizontal,CDhorizontal,Ecenterbelow;all nativecamera2font10ptunscaled')
(root/'image_tex/build/bounded-surface-comparison-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.52:all5panels semantic native geometry,',sum(p['native_curve_checks'] for p in proof),'nativechecks;169shareddata,commoncamera/font.')
