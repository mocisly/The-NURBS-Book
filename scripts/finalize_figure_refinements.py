"""Record and apply individually reviewed label and panel spacing corrections."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'tmp/figure-layout'
notes=json.loads((WORK/'layout-offsets.json').read_text(encoding='utf-8'))
changed=set()
def replace(path,before,after):
    p=ROOT/'image_tex'/path;s=p.read_text(encoding='utf-8')
    note=dict(path='image_tex/'+path,before=before,after=after)
    if note not in notes:
        assert before in s,(path,before)
        p.write_text(s.replace(before,after),encoding='utf-8');notes.append(note)
    changed.add(path)
def tag(path,letter,dy):
    p=ROOT/'image_tex'/path
    for line in p.read_text(encoding='utf-8').splitlines():
        if '[book panel tag]'in line and '{('+letter+')}'in line:
            replace(path,line,line.replace('[book panel tag]',f'[book panel tag,yshift={dy}pt]'))
replace('ch07/fig_7_03.tex','node[below right=6pt] {$(-a,0)$}','node[below left=6pt] {$(-a,0)$}')
replace('ch07/fig_7_03.tex','node[below left=6pt] {$(a,0)$}','node[below right=6pt] {$(a,0)$}')
# Separate labels on nearly aligned low control points.
replace('ch06/fig_6_27.tex','node[below right=6pt] {$\\mathbf P_1$}','node[below left=6pt] {$\\mathbf P_1$}')
replace('ch06/fig_6_27.tex','node[below left=6pt] {$\\mathbf P_8$}','node[below right=6pt] {$\\mathbf P_8$}')
replace('ch06/fig_6_27.tex','node[below right=6pt] {$\\mathbf Q_1$}','node[below left=6pt] {$\\mathbf Q_1$}')
replace('ch06/fig_6_27.tex','node[below left=6pt] {$\\mathbf Q_5$}','node[below right=6pt] {$\\mathbf Q_5$}')
for path,letter,dy in [('ch08/fig_8_07.tex','d',-20),('ch07/fig_7_21.tex','b',-18),*[(f'ch07/fig_7_{i}.tex','b',-10)for i in [22,23,24]],*[(f'ch12/fig_12_{i}.tex',letter,-16)for i,letter in [('03','a'),('03c','c'),('04','b')]]]:tag(path,letter,dy)
for path,before,after in [('ch08/fig_8_13.tex','yshift=32cm','yshift=36cm'),('ch08/fig_8_21.tex','yshift=26cm','yshift=30cm'),('ch09/fig_9_69.tex','yshift=36cm','yshift=44cm'),('ch09/fig_9_69.tex','yshift=18cm','yshift=22cm'),('ch10/fig_10_24.tex','yshift=14cm','yshift=17cm'),('ch11/fig_11_06.tex','yshift=10.5cm','yshift=14cm')]:replace(path,before,after)
replace('ch09/fig_9_23.tex',r'\node[left=8pt] at (7,1.9)',r'\node[right=8pt] at (7,1.9)')
replace('ch09/fig_9_23.tex',r'\node[below left=8pt] at (6.8,3)',r'\node[above right=8pt] at (6.8,3)')
replace('ch09/fig_9_14.tex',r'\node[above right=5pt] at (0.9,4.45)',r'\node[left=8pt] at (0.9,4.45)')
replace('ch09/fig_9_14.tex',r'\node[below left=5pt] at (-3.9,-2.55)',r'\node[below right=8pt] at (-3.9,-2.55)')
replace('ch10/fig_10_25.tex',r'\node[above right=6pt] at (5.262,1.0634311111)',r'\node[below right=6pt] at (5.262,1.0634311111)')
for path,needle in [('ch10/fig_10_04.tex',r'\node at (0,4.55)'),('ch10/fig_10_05.tex',r'\node at (0,4.55)'),('ch11/fig_11_06.tex',r'\node at (4,3.8)'),('ch11/fig_11_15.tex',r'\node[anchor=west] at (.04,.64)'),('ch11/fig_11_17.tex',r'\node[anchor=west] at (.04,.55)'),('ch11/fig_11_18.tex',r'\node[anchor=west] at (.04,.55)')]:
    replace(path,needle,needle.replace('\\node at','\\node[yshift=22pt] at').replace('anchor=west]','anchor=west,yshift=22pt]'))
replace('ch11/fig_11_12.tex','node[above left=6pt] {$P_{8}$}','node[below right=8pt] {$P_{8}$}')
replace('ch11/fig_11_12.tex',r'\node[align=left,anchor=north west] at (.1,6.6)',r'\node[align=left,anchor=north east] at (-.6,6.6)')
replace('ch11/fig_11_15.tex',r'\node[below=7pt] at (0.0266666667,-0.1)',r'\node[below left=7pt] at (0.0266666667,-0.1)')
replace('ch11/fig_11_15.tex',r'\node[below=7pt] at (0.1035469277,-0.1)',r'\node[below right=7pt] at (0.1035469277,-0.1)')
replace('ch11/fig_11_36.tex',r'\node[below right=7pt] at (4,-1)',r'\node[above right=7pt] at (4,-1)')
replace('ch12/fig_12_01.tex',r'\node at (3,-4.1)',r'\node[yshift=-20pt] at (3,-4.1)')
replace('ch12/fig_12_04.tex','node[left=7pt] {$P_1$}','node[below left=10pt] {$P_1$}')
replace('ch12/fig_12_04.tex','node[left=7pt] {$P_6$}','node[above left=10pt] {$P_6$}')
replace('ch12/fig_12_07.tex','node[right=9pt] {$P_0^{2}$}','node[below right=16pt] {$P_0^{2}$}')
(WORK/'layout-offsets.json').write_text(json.dumps(notes,indent=2),encoding='utf-8')
profiles=json.loads((WORK/'profiles.json').read_text(encoding='utf-8'))
for p in profiles:
    if p['path']in ['ch13/fig_13_04.tex','ch13/fig_13_05.tex']:p['min_scale']=1;changed.add(p['path'])
    if p['path']=='ch10/fig_10_08.tex':p['target_width_cm']=9;p['target_height_cm']=8;changed.add(p['path'])
(WORK/'profiles.json').write_text(json.dumps(profiles,indent=2),encoding='utf-8')
(WORK/'final-refinement-paths.json').write_text(json.dumps(sorted(changed),indent=2),encoding='utf-8')
print(' '.join(sorted(changed)))
