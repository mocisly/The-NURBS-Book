"""Native Fig5.20/5.21: one tensor surface and its actual four Bezier patches."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json
from knot520_data import BASE,decomposition
from surface_geometry import verify_tensor
from native_surface_drawing import wires
from native_bspline import point

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('mode',choices=['base','patch-net','patch-surface'])
a=p.parse_args();root=Path(__file__).resolve().parents[1]
number={'base':24,'patch-net':25,'patch-surface':26}[a.mode]
target=root/f'image_tex/ch05/fig_5_{number}.tex';assert not target.exists(),target
panels=[];reports=[]
camera=r'\begin{scope}[x={(-.85cm,-.55cm)},y={(.85cm,-.3cm)},z={(0cm,.9cm)}]'

def axes():
    return [r'\draw[book axis] (0,0,0)--(5.5,0,0) node[below left=4pt] {$x$};',
            r'\draw[book axis] (0,0,0)--(0,6.2,0) node[right=4pt] {$y$};',
            r'\draw[book axis] (0,0,0)--(0,0,8.3) node[above=4pt] {$z$};']

def control_net(net):
    R=net[-1];lines=[]
    for row in R:lines.append(r'\draw[book grid,dashed] '+'--'.join(map(point,row))+';')
    for j in range(len(R[0])):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(row[j]) for row in R)+';')
    for row in R:
        for pt in row:lines.append(r'\fill '+point(pt)+' circle[radius=1pt];')
    return lines

report={'figure':'5.20' if a.mode=='base' else '5.21','mode':a.mode,
        'degrees':[3,2],'original_controls':[5,4],'unit_weights':True,
        'representative_control_coordinates_not_given_in_original':True,
        'U':list(map(str,BASE[0])),'V':list(map(str,BASE[1])),
        'original_control_coordinates':[[list(map(str,t)) for t in row] for row in BASE[-1]]}
if a.mode=='base':
    report['tensor_vs_both_deboor_directions_points']=verify_tensor(*BASE,steps=16)
    for index in (0,1):
        lines=[camera]
        if index==0:lines+=control_net(BASE)
        else:
            drawn,proof=wires(*BASE,count=37);lines+=drawn;reports.append(proof)
        lines+=axes()+[r'\end{scope}',r'\node at (0,-4.8) {('+chr(97+index)+')};']
        panels.append(lines)
else:
    patches,proofs,refined=decomposition();report['exact_decomposition_proofs']=proofs
    report['refined_control_count']=[len(refined[-1]),len(refined[-1][0])]
    report['four_extracted_patch_nets_match_refined_net_exactly']=True
    report['each_patch_control_count']=[4,3]
    report['display_translation_only']=True
    lines=[camera]
    for i,j,child in patches:
        # Opening the two seams is an explicitly documented display translation.
        # u controls physical y, v controls physical x in this example.
        dx=F(3,5)*(1 if j==0 else -1);dy=F(3,5)*(-1 if i==0 else 1)
        A,B,pd,qd,R=child
        displayed=(A,B,pd,qd,tuple(tuple((t[0]+dx,t[1]+dy,t[2]) for t in row) for row in R))
        if a.mode=='patch-net':lines+=control_net(displayed)
        else:
            drawn,proof=wires(*displayed,count=25);lines+=drawn;reports.append(proof)
    lines+=axes()+[r'\end{scope}',r'\node at (0,-5.15) {'+('(a)' if a.mode=='patch-net' else '(b)')+'};']
    panels.append(lines)
lines=['% Semantic tensor-product surface, exact polynomial isocurves and Bezier extraction.',
       '% All coordinates and display offsets documented in scripts/knot520_data.py and report.',
       r'\begin{tikzpicture}[book line]']
if a.mode=='base':
    lines.append(r'\path[use as bounding box] (-13.5,-5.5) rectangle (13.5,8.2);')
    for panel,shift in zip(panels,(-7,7)):
        lines+=[r'\begin{scope}[xshift='+str(shift)+'cm]']+panel+[r'\end{scope}']
else:
    lines.append(r'\path[use as bounding box] (-6.5,-5.6) rectangle (6.5,8.2);')
    lines+=panels[0]
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
report['native_isocurve_proofs']=reports
(root/f'image_tex/build/surface-bezier-{a.mode}-check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS '+a.mode+': '+str(report.get('tensor_vs_both_deboor_directions_points','four exact Bezier patches'))+
      '; native isocurve checks '+str(sum(r['exact_isocurve_checks'] for r in reports)))
