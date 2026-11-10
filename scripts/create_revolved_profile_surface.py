"""8.9: exactly the same six-point profile as8.8,with full net and actual isocurves."""
from pathlib import Path
from fractions import Fraction as F
import json
from revolved_surface_data import P,V,PROFILE,U,CIRCLE,NET,camera,w
from native_bspline import segments,check,de_boor,cubic_path,point
from rational_geometry import project,approximate
from surface_geometry import surface,verify_tensor,isocurve
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
assert not next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_13.tex')['applied']
tc=verify_tensor(U,V,2,2,NET);lines=['% Same tensor-product surface and camera as8.8:9circumferential x6profile controls.',r'\begin{tikzpicture}[book line]'];cert=[];nc=iso=0
for label,shift in [('a',32),('b',0)]:
    lines.extend([r'\begin{scope}[yshift='+str(shift)+'cm]',r'\path[use as bounding box] (-16,-7) rectangle (16,23);'])
    if label=='a':
        for j in range(6):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(NET[i][j]))) for i in range(9))+';')
        for row in NET[:-1]:
            lines.append(r'\draw[book grid,dashed] '+'--'.join(point(camera(project(h))) for h in row)+';')
            lines.extend(r'\fill '+point(camera(project(h)))+r' circle[radius=1.3pt];' for h in row)
    else:
        for variable,values in [('u',[F(i,4) for i in range(5)]),('v',[F(i,8) for i in range(8)])]:
            for fixed in values:
                K,p,Q=isocurve(U,V,2,2,NET,variable,fixed)
                for i in range(21):
                    t=F(i,20);assert de_boor(K,Q,p,t)==(surface(U,V,2,2,NET,t,fixed) if variable=='u' else surface(U,V,2,2,NET,fixed,t));iso+=1
                if variable=='v':
                    assert len(set(h[-1] for h in Q))==1
                    pp=tuple(camera(project(h)) for h in Q);ss=segments(K,pp,p);nc+=check(K,pp,p,ss)
                    lines.extend(cubic_path(s) for s in ss)
                else:
                    hh=tuple(camera(h[:3])+(h[-1],) for h in Q)
                    parts=[part for s in segments(K,hh,p) for part in approximate(s['bern'],F(1,100000))]
                    lines.extend(cubic_path(part) for part in parts);cert.append(str(max(part['certified_l1_error'] for part in parts)))
    for end,name,anchor in [((F(14,5),0,0),'x','below left'),((0,F(14,5),0),'y','right'),((0,0,F(53,10)),'z','above')]:
        lines.append(r'\draw[book axis,book grid] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    lines.extend([r'\node at (0,-6.3) {('+label+')};',r'\end{scope}'])
lines.append(r'\end{tikzpicture}');(root/'image_tex/ch08/fig_8_13.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/revolved-profile-surface-check.json').write_text(json.dumps({'figure':'8.9','same_data_as8_8':True,'degrees':[2,2],'control_dimensions':[9,6],'distinct_control_points':48,'product_weights':True,'closed_control_rows0_equals8':all(NET[0][j]==NET[-1][j] for j in range(6)),'exact_tensor_checks':tc,'exact_isocurve_vs_surface_checks':iso,'native_meridian_checks':nc,'parallel_parameters':['0','1/4','1/2','3/4','1'],'meridian_parameters':[str(F(i,8)) for i in range(8)],'native_parallel_screen_L1_error_bounds_cm':cert,'common_camera_scale_and_panel_dimensions':True,'display':'transparent wireframe'},indent=2)+'\n')
print('PASS:shared8.8data,441tensor and273isocurve identities;48distinct controls,exact polynomial meridians and certified circular parallels.')
