"""Standalone semantic asset for the old5.10c crop, already covered in the book."""
from fractions import Fraction as F
import json
import image_tex as pipeline
from knot59_data import U,V,P,insert_surface
from surface_geometry import verify_tensor,surface
from native_bspline import point

root=pipeline.ROOT;target=root/'image_tex/ch05/fig_5_10c_reference.tex';assert not target.exists()
base=(U,V,3,2,P)
A=insert_surface(*base,'u',F('.4'));A=insert_surface(*A,'v',F('.7'))
B=insert_surface(*base,'v',F('.7'));B=insert_surface(*B,'u',F('.4'));assert A==B
Q=A[-1];assert len(Q)==len(Q[0])==5
checks=verify_tensor(*A,steps=10);comparisons=0
for i in range(11):
    for j in range(11):
        u,v=F(i,10),F(j,10);assert surface(*A,u,v)==surface(*base,u,v);comparisons+=1
lines=['% Semantic5.10c reference for the original crop omitted by OCR includegraphics.',
       '% Same exact5x5 refined control net is already drawn in the book fig_5_11.tex panel(c).',
       '% Standalone archive asset; do not insert a duplicate panel in the chapter.',
       r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-6,-5) rectangle (7,8);',
       r'\begin{scope}[x={(-.9cm,-.6cm)},y={(1cm,-.35cm)},z={(0cm,1cm)}]',
       r'\draw[book axis] (0,0,0)--(5.8,0,0) node[below left=4pt] {$x$};',
       r'\draw[book axis] (0,0,0)--(0,6.8,0) node[right=4pt] {$y$};',
       r'\draw[book axis] (0,0,0)--(0,0,7.2) node[above=4pt] {$z$};']
for row in Q:lines.append(r'\draw[book grid,densely dotted] '+'--'.join(map(point,row))+';')
for j in range(5):lines.append(r'\draw[book grid,dashed] '+'--'.join(point(row[j]) for row in Q)+';')
for row in Q:
    for pt in row:lines.append(r'\fill '+point(pt)+r' circle[radius=1.5pt];')
for i,j,where in [(0,0,'left=7pt'),(1,0,'below left=7pt'),(0,1,'above left=7pt'),(0,4,'above=7pt'),(4,4,'right=7pt'),(4,0,'below=7pt')]:
    lines.append(r'\node['+where+'] at '+point(Q[i][j])+r' {$\mathbf Q_{'+str(i)+','+str(j)+'}$};')
lines += [r'\end{scope}',r'\end{tikzpicture}'];target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/surface-insertion-reference-check.json').write_text(json.dumps({
    'original_crop':'0193ba0d-ab19-7138-9798-cb281ce60de0_166_319_257_893_799_0.jpg',
    'covered_by':'image_tex/ch05/fig_5_11.tex panel(c)','same_knot59_representative_data_as_book':True,
    'refinement_order_commutes_exactly':True,'tensor_checks':checks,'exact_original_surface_comparisons':comparisons,
    'U':list(map(str,A[0])),'V':list(map(str,A[1])),
    'refined_controls':[[list(map(str,pt)) for pt in row] for row in Q]},indent=2)+'\n')
d=pipeline.load();e=next(e for e in d['images'] if '_166_319_257_893_799_' in e['image'])
assert e['kind']=='unused' and not e['applied']
e.update(tex='image_tex/ch05/fig_5_10c_reference.tex',chapter=5,chapter_file='chapter/5.tex',
         covered_by=['image_tex/ch05/fig_5_11.tex'],coverage_of='5.10c',
         note='Native standalone reference authored for OCR-omitted crop; already covered by applied5.10c panel, awaiting independent preview/coverage review.')
pipeline.save(d);print('PASS:exact5x5 net,121 tensor checks+121 invariance comparisons; standalone reference registered, no duplicate book insertion.')
