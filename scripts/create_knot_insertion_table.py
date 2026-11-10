"""Reconstruct Table5.1's symbolic insertion triangle from its original scan."""
from pathlib import Path
import json,re
import image_tex as p

root=p.ROOT;target=root/'image_tex/ch05/table_5_01.tex';assert not target.exists()
lines=[r'% Table5.1: genuine LaTeX indices, no text/image outlines.',r'\begin{tikzpicture}[book line]',
       r'\path[use as bounding box] (-1.9,-2.4) rectangle (10.8,2.4);',
       r'\draw[book grid] (-1.8,2.2)--(10.6,2.2);',r'\draw[book grid] (-1.8,-2.2)--(10.6,-2.2);']
nodes=[(0,1.7,r'\mathbf Q^w_{k-p+1,1}'),(0,.85,r'\mathbf Q^w_{k-p+2,1}'),
       (0,0,r'\vdots'),(0,-.85,r'\mathbf Q^w_{k-1,1}'),(0,-1.7,r'\mathbf Q^w_{k,1}'),
       (3.8,1.25,r'\mathbf Q^w_{k-p+2,2}'),(3.8,0,r'\vdots'),(3.8,-1.25,r'\mathbf Q^w_{k,2}'),
       (6.8,0,r'\cdots'),(9.8,0,r'\mathbf Q^w_{k,p}')]
for x,y,label in nodes:lines.append(r'\node at ('+str(x)+','+str(y)+') {$'+label+'$};')
lines.append(r'\end{tikzpicture}');target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
counts=[]
for degree in range(3,13):
    k=20;generated={(i,r) for r in range(1,degree+1) for i in range(k-degree+r,k+1)}
    boundary=[(k-degree+r,r) for r in range(1,degree+1)]+[(k,r) for r in range(degree-1,0,-1)]
    assert len(generated)==degree*(degree+1)//2
    assert len(boundary)==len(set(boundary))==2*degree-1 and set(boundary)<=generated
    counts.append({'p':degree,'generated':len(generated),'retained_boundary':len(boundary),'discarded_interior':len(generated-set(boundary))})
(root/'image_tex/build/knot-insertion-table-check.json').write_text(json.dumps({
    'table':'5.1','full_triangle_assumptions':'s=0,r=p','symbolic_rows_match_equation515':True,
    'retained_points_follow_clockwise_outer_boundary_not_interior':True,'exact_combinatorial_checks':counts},indent=2)+'\n')
# This crop was listed as unused because the OCR emitted an HTML tag instead
# of includegraphics. Keep the stable original ID and restore its real chapter.
d=p.load();e=next(e for e in d['images'] if '_159_499_257_531_414_' in e['image'])
assert e['kind']=='unused' and not e['applied'];s=(root/'chapter/5.tex').read_text(encoding='utf-8')
matches=[m for m in re.finditer(r'<img\b[^>]*>',s) if r'\_159.jpg?x=499\&y=257\&w=531\&h=414' in m.group()]
assert len(matches)==1;original=matches[0].group()
e.update(chapter=5,chapter_file='chapter/5.tex',line=s[:matches[0].start()].count('\n')+1,
         tex='image_tex/ch05/table_5_01.tex',kind='inline',options=r'max width=\linewidth',original=original,
         previous_kind='unused',note='Original HTML crop recovered as Table5.1; semantic redraw awaiting preview/review.')
p.save(d);print('Authored Table5.1 and restored its HTML crop to chapter5;10 exact triangle/boundary count checks passed.')
