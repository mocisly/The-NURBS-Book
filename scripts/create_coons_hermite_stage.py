"""One individually inspected printed Coons construction figure,27--30."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json
from coons_hermite_data import make,add,mul
from coons_patch_data import U,V,C0U,C1U,C0V,C1V,view
from gordon_native import panel
from native_bspline import segments,check,cubic_path
root=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('number',type=int,choices=(27,28,29,30));args=parser.parse_args();data=make()
source=args.number+10;name={27:'S2',28:'S1',29:'T',30:'S'}[args.number];title={'S2':'S_2','S1':'S_1','T':'T','S':'S'}[name];net=data['nets'][name]
manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'));assert not next(e for e in manifest['images'] if e['tex']==f'image_tex/ch10/fig_10_{source:02}.tex')['applied']
if name=='S2':
    P=net[4];assert P[0]==C0V and P[-1]==C1V
    assert tuple(mul(add(b,a,-1),3) for a,b in zip(P[0],P[1]))==data['DL'][0]
    assert tuple(mul(add(b,a,-1),3) for a,b in zip(P[-2],P[-1]))==data['DL'][1]
if name=='S1':
    P=net[4];assert tuple(row[0] for row in P)==C0U and tuple(row[-1] for row in P)==C1U
    assert tuple(mul(add(row[1],row[0],-1),3) for row in P)==data['DK'][0]
    assert tuple(mul(add(row[-1],row[-2],-1),3) for row in P)==data['DK'][1]
out=['% Exact Coons Hermite stage from shared compatible boundary derivative data.',r'\begin{tikzpicture}[book line]'];proof=[]
for letter,control,shift in [('a',True,0),('b',False,19)]:
    lines,r=panel(net,letter,title,shift,control)
    if not control:
        extra=[]
        for K,C,p,interpolated in [(U,C0U,3,name in ('S1','S')),(U,C1U,3,name in ('S1','S')),(V,C0V,2,name in ('S2','S')),(V,C1V,2,name in ('S2','S'))]:
            ss=segments(K,C,p);r['native_curve_checks']+=check(K,C,p,ss,steps=3)
            extra.extend(cubic_path(dict(bern=tuple(view(a) for a in s['bern'])),'line width=.9pt' if interpolated else 'dashed') for s in ss)
        lines[-1:-1]=extra
    r.update(stage=name,letter=letter);out+=lines;proof.append(r)
out.append(r'\end{tikzpicture}');(root/f'image_tex/ch10/fig_10_{source:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
report={k:v for k,v in data.items() if k!='nets'};report.update(native_panels=proof,math_source='scripts/coons_hermite_data.py',no_contour_tracing=True,native_curve_error=0)
(root/f'image_tex/build/coons-hermite-stage-{args.number}-check.json').write_text(json.dumps(report,default=str,indent=2)+'\n',encoding='utf-8');print('PASS10.'+str(args.number),name,':',sum(r['native_curve_checks'] for r in proof),'nativechecks/',sum(r['tensor_isocurve_checks'] for r in proof),'tensorcrosschecks;',r['control_shape'],'actualnet.')
