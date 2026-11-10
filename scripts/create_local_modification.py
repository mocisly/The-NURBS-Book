"""Fig3.7: moving one control changes exactly its basis-support interval."""
from pathlib import Path
from fractions import Fraction as F
import json
from bspline_math import piece,evaluate
from native_bspline import segments,check,point,cubic_path

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch03/fig_3_07.tex'
assert not target.exists()
knots=(F(0),)*4+(F(1,4),F(1,2),F(3,4))+(F(1),)*4
controls=((0,0),(4,0),(4,4),(9,4),(5,-2),(10,-4),(2,-4))
changed=list(controls);changed[4]=(F(17,2),-1)
original=segments(knots,controls,3);modified=segments(knots,changed,3)
count=check(knots,controls,3,original)+check(knots,changed,3,modified)
assert original[0]['power']==modified[0]['power']
delta=tuple(b-a for a,b in zip(controls[4],changed[4]))
for left,right in zip(original,modified):
    s=left['span'];w=piece(knots,4,3,s)
    for k in range(42):
        u=left['a']+(left['b']-left['a'])*F(k,41)
        for d in range(2): assert evaluate(right['power'][d],u)-evaluate(left['power'][d],u)==evaluate(w,u)*delta[d]
lines=['% Fig3.7: cubic U=(0,0,0,0,1/4,1/2,3/4,1,1,1,1).',
       '% Representative coordinates; only P4 moves, from (5,-2) to (17/2,-1).',
       '% Modified minus original is exactly N4,3(u)*(P4prime-P4); no tracing.',
       r'\begin{tikzpicture}[book line,x=1cm,y=1cm]']
for i,p in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at '+point(p)+';')
lines += [r'\coordinate (Q4) at '+point(changed[4])+';',
          r'\draw[book grid] (P0)--(P1)--(P2)--(P3)--(P4)--(P5)--(P6);',
          r'\draw[book grid,dashed] (P3)--(Q4)--(P5);']
for seg in original: lines.append(cubic_path(seg))
for seg in modified[1:]: lines.append(cubic_path(seg,'dashed'))
for seg in original[:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
for seg in modified[1:-1]: lines.append(r'\fill '+point(seg['bern'][-1])+' circle[radius=1.7pt];')
lines += [r'\foreach \i in {0,...,6} \node[book point] at (P\i) {};',
          r'\node[book point] at (Q4) {};',r"\node[left=5pt] at (Q4) {$\mathbf P'_4$};"]
for i,pos in enumerate(['below left','below left','above left','above right','below left','below right','below left']):
    lines.append(r'\node['+pos+'=4pt] at (P'+str(i)+r') {$\mathbf P_{'+str(i)+'}$};')
lines.append(r'\end{tikzpicture}')
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/local-modification-check.json').write_text(json.dumps({'figure':'3.7',
    'knots':list(map(str,knots)),'representative_controls':[[str(v) for v in p] for p in controls],
    'moved_control':[str(v) for v in changed[4]],'exact_curve_comparisons':count,
    'difference_equals_basis_times_control_displacement':True,'first_span_identical':True,
    'affected_support':['1/4','1'],'endpoint_unchanged':True},indent=2)+'\n')
print(f'PASS: {count} exact curve checks; local displacement identity and unchanged first span verified.')
