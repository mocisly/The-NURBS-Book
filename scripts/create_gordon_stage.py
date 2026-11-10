"""Draw one already inspected printed figure:19,20,21,22 or23, individually."""
from pathlib import Path
import argparse,json
from fractions import Fraction as F
from gordon_native import panel
root=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser();a.add_argument('number',type=int,choices=(19,20,21,22,23));args=a.parse_args()
d=json.loads((root/'image_tex/build/gordon-network-data.json').read_text(encoding='utf-8'))
def net(n):
    U,V,p,q,P=n
    return tuple(map(F,U)),tuple(map(F,V)),p,q,tuple(tuple(tuple(map(F,a)) for a in row) for row in P)
nets=d['nets'];groups={19:[(26,'L1',True,'a',None),(26,'L1',False,'b','v')],20:[(27,'L2',True,'a',None),(27,'L2',False,'b','u')],21:[(28,'T',True,'a',None),(28,'T',False,'b','points')],22:[(29,'refined0',True,'a',None),(29,'refined1',True,'b',None),(30,'refined2',True,'c',None)],23:[(31,'S',True,'a',None),(31,'S',False,'b','both')]}
reports=[];sources={}
manifest=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for source,name,control,letter,highlight in groups[args.number]:
    target=f'image_tex/ch10/fig_10_{source:02}.tex';assert not next(e for e in manifest['images'] if e['tex']==target)['applied']
    if source not in sources:sources[source]=['% Actual Gordon construction from shared compatible data, no contour tracing.',r'\begin{tikzpicture}[book line]']
    shift=19 if letter=='b' else 0
    if name.startswith('refined'):base=net(nets['refined'][int(name[-1])]);title=('L_1','L_2','T')[int(name[-1])]
    else:base=net(nets[name]);title=dict(L1='L_1',L2='L_2',T='T',S='S')[name]
    lines,r=panel(base,letter,title,shift,control,highlight,reference=(args.number in (19,20) and not control));sources[source]+=lines;r.update(printed_figure='10.'+str(args.number),letter=letter,source=target);reports.append(r)
for source,out in sources.items():out.append(r'\end{tikzpicture}');(root/f'image_tex/ch10/fig_10_{source:02}.tex').write_text('\n'.join(out)+'\n',encoding='utf-8')
(root/f'image_tex/build/gordon-stage-{args.number}-check.json').write_text(json.dumps(dict(no_contour_tracing=True,mathematical_data='gordon-network-data.json',panels=reports),indent=2)+'\n',encoding='utf-8')
print('PASS10.'+str(args.number)+':',sum(r['native_curve_checks'] for r in reports),'nativechecks/',sum(r['tensor_isocurve_checks'] for r in reports),'tensorcrosschecks;exactquadratic/cubicpaths.')
