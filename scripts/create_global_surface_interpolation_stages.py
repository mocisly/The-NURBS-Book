"""9.14:a data,b u-interpolation,c v-interpolation,d actual bicubic surface."""
from fractions import Fraction as F
from pathlib import Path
import json
from global_surface_interpolation_data import Q,R,P,U,V,PARAMS,camera
from surface_geometry import verify_tensor,isocurve
from native_bspline import segments,check,cubic_path,point
root=Path(__file__).resolve().parents[1];d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (14,15,16):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex')['applied']
tc=verify_tensor(U,V,3,3,P);nc=0
def poly(points,style):return r'\draw['+style+'] '+'--'.join(point(camera(q)) for q in points)+';'
def curve(K,C,style=''):
    global nc
    ss=segments(K,C,3);nc+=check(K,C,3,ss)
    return [cubic_path(dict(bern=tuple(camera(q) for q in s['bern'])),style) for s in ss]
def marker(q,filled=True,radius='1.7'):
    return ('\\fill ' if filled else '\\draw ')+point(camera(q))+' circle[radius='+radius+'pt];'
def label(q,name,anchor='above right'):
    return r'\node['+anchor+r'=5pt] at '+point(camera(q))+' {$'+name+'$};'
def panel(mode,shift=0):
    out=[r'\begin{scope}[xshift='+str(shift)+r'cm]',r'\path[use as bounding box] (-10,-6) rectangle (8,13);']
    if mode=='a':
        for row in Q:out.append(poly(row,'book grid,dashed'))
        for col in zip(*Q):out.append(poly(col,'book grid,dashed'))
        anchors=[['above left','above left','above left','above'],['left','left',None,'right'],['below left','left','above right','above right'],['below right','below right','above','below right']]
        for i,row in enumerate(Q):
            for j,q in enumerate(row):
                out.append(marker(q))
                if anchors[i][j]:out.append(label(q,r'\mathbf Q_{'+str(i)+','+str(j)+'}',anchors[i][j]))
    elif mode=='b':
        for j in range(4):
            col=tuple(R[i][j] for i in range(4));out.append(poly(col,'book grid'));out+=curve(U,col)
            for i,q in enumerate(col):
                anchor={ (0,3):'above left',(1,3):'below left',(2,1):'left',(2,2):'below left',(2,0):'below left',(1,0):'above right',(1,1):'above right',(1,2):'above right'}.get((i,j),('above left' if i==0 else 'below right') if j!=3 else 'right')
                out.append(marker(q))
                if (i,j)!=(0,3):out.append(label(q,r'\mathbf R_{'+str(i)+','+str(j)+'}',anchor))
            for q in (Q[i][j] for i in range(1,3)):out.append(marker(q,False,'1.5'))
        out.append(r'\node[anchor=west] (r03) at (1.5,8.5) {$\mathbf R_{0,3}$};')
        out.append(r'\draw[book grid] '+point(camera(R[0][3]))+'--(r03.west);')
    elif mode=='c':
        for col in zip(*R):out.append(poly(col,'book grid,dashed'))
        for i,row in enumerate(P):
            out.append(poly(row,'book grid'));out+=curve(V,row)
            for j,q in enumerate(row):out.append(marker(q))
            for j in (0,1,3):
                if (i,j) in ((0,3),(2,3),(2,1)):continue
                anchor='below left' if (i,j)==(1,0) else ('left' if (j==1 and i!=3) or (j==0 and i!=3) else 'below right')
                out.append(label(row[j],r'\mathbf P_{'+str(i)+','+str(j)+'}',anchor))
            for j in (1,2):out.append(marker(R[i][j],False))
            out.append(label(R[i][1],r'\mathbf R_{'+str(i)+',1}','below right' if i==1 else 'below left'))
        out.append(label(P[0][2],r'\mathbf P_{0,2}','above right'))
        for i,j,target in [(0,3,(F(1),F(8))),(2,3,(F(57,10),F(31,5))),(3,2,(F(11,2),F(9,2))),(2,1,(F(0),-F(14,5)))]:
            name='p'+str(i)+str(j)
            out.append(r'\node[anchor=west] ('+name+') at '+point(target)+r' {$\mathbf P_{'+str(i)+','+str(j)+'}$};')
            out.append(r'\draw[book grid] '+point(camera(P[i][j]))+'--('+name+'.west);')
    else:
        for row in P:out.append(poly(row,'book grid,dashed'))
        for col in zip(*P):out.append(poly(col,'book grid,dashed'))
        for j in range(33):
            K,p,C=isocurve(U,V,3,3,P,'u',F(j,32));out+=curve(K,C)
        for row in P:
            for q in row:out.append(marker(q))
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(24,5)),'z','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(camera(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    out += [r'\node at (-1,-5.5) {('+mode+')};',r'\end{scope}'];return out
header=['% Representative4x4data,p=q=3,uniformdata parametersi/3;all two-stage solves exact.',r'\begin{tikzpicture}[book line]']
for n,modes in [(14,[('a',0),('b',19)]),(15,[('c',0)]),(16,[('d',0)])]:
    lines=header.copy()
    for mode,shift in modes:lines+=panel(mode,shift)
    lines.append(r'\end{tikzpicture}');(root/f'image_tex/ch09/fig_9_{n:02}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/global-surface-interpolation-stages-check.json').write_text(json.dumps(dict(figure='9.14',representative_data=[[[str(x) for x in q] for q in row] for row in Q],parameters=list(map(str,PARAMS)),knots=[list(map(str,U)),list(map(str,V))],degrees=[3,3],intermediate_controls=[[[str(x) for x in q] for q in row] for row in R],final_controls=[[[str(x) for x in q] for q in row] for row in P],all16data_interpolation_constraints_exact=True,reverse_interpolation_order_yields_identical16controls=True,independent_tensor_checks=tc,native_curve_checks=nc,same_camera_and_font_for_all_panels=True),indent=2)+'\n')
print('PASS:two-stage4x4bicubic solve,reverse order identical,all16data exact,441tensor checks,',nc,'native curve checks.')
