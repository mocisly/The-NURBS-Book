"""Printed Fig2.12: exact nonuniform cubic family specified in the caption."""
from pathlib import Path
from fractions import Fraction as F
import json
import argparse
from bspline_math import piece,evaluate,derivative,expression,basis,compose_affine

root=Path(__file__).resolve().parents[1];target=root/'image_tex/ch02/fig_2_14.tex'
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--refresh-unapplied',action='store_true')
args=parser.parse_args()
if target.exists():
    entry=next(e for e in json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))['images'] if e['tex']=='image_tex/ch02/fig_2_14.tex')
    assert args.refresh_unapplied and not entry.get('applied'), 'Only unintegrated source14 may be refreshed'
knots=(0,0,0,0,1,5,6,8,8,8,8);spans=(3,4,5,6)
checks=0
for span in spans:
    a,b=knots[span:span+2]
    for k in range(41):
        x=F(a)+F(k,41)*(b-a);values=[]
        for i in range(7):
            c=piece(knots,i,3,span)
            y=evaluate(c,x)
            assert evaluate(compose_affine(c,a,b-a),F(k,41))==y
            assert y==basis(knots,i,3,x);values.append(y);checks+=1
        assert min(values)>=0 and sum(values)==1
for span in (3,4,5):
    for i in range(7):
        a,b=piece(knots,i,3,span),piece(knots,i,3,span+1)
        for order in range(3):
            assert evaluate(a,F(knots[span+1]))==evaluate(b,F(knots[span+1]))
            a,b=derivative(a),derivative(b)
# P2.8/FindSpan extend the final basis to N_n,p(b)=1 at the right endpoint.
end=[evaluate(piece(knots,i,3,6),F(8)) for i in range(7)]
assert end==[0,0,0,0,0,0,1]
def value(i,x):
    x=F(str(x));span=next(s for s in spans if knots[s]<=x<knots[s+1])
    return float(evaluate(piece(knots,i,3,span),x))

lines=['% Printed Fig2.12. U=(0,0,0,0,1,5,6,8,8,8,8), from caption.',
       '% Right endpoint follows P2.8/FindSpan: N6,3(8)=1.',
       '% Exact rational polynomial pieces from Cox-de Boor; no tracing.',
       '% Each piece uses a local parameter t in [0,1] to avoid cancellation.',
       r'\begin{tikzpicture}',
       r'\begin{axis}[scale only axis,width=14cm,height=5.2cm,axis lines=left,',
       r'xmin=-.3,xmax=9.2,ymin=0,ymax=1.45,xtick={0,1,5,6,8},ytick={1},',
       r'xlabel={$u$},tick align=outside,axis line style={-{Stealth}},clip=false]']
for i in range(7):
    for span in spans:
        a,b=knots[span:span+2];c=piece(knots,i,3,span)
        if any(c): lines.append(r'\addplot[book line,no marks,samples=41,domain=0:1] ({'+f'{a}+{b-a}*x'+'},{'+expression(compose_affine(c,a,b-a))+'});')
    if i in (0,6): continue
    y,x=max((value(i,F(k,100)),k/100) for k in range(800))
    lines.append(r'\node[above=5pt] at (axis cs:'+f'{x:.5f},{y:.8f}'+') {$N_{'+f'{i},3'+'}$};')
lines += [r'\node (n0) at (axis cs:.25,1.28) {$N_{0,3}$};',
          r'\draw[book grid,-{Stealth[length=4pt]}] (n0)--(axis cs:.08,.778688);',
          r'\fill (axis cs:8,1) circle[radius=1.5pt];',
          r'\node[above=5pt] at (axis cs:8,1) {$N_{6,3}$};',
          r'\pgfplotsinvokeforeach{-.09,-.03,.03,7.91,7.97,8.03}{',
          r'\draw[book grid] (axis cs:#1,-.025)--(axis cs:#1,.025);}',
          r'\end{axis}',r'\end{tikzpicture}']
target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(root/'image_tex/build/nonuniform-basis-check.json').write_text(json.dumps({
    'knots':knots,'exact_recurrence_comparisons':checks,
    'nonnegative_partition':True,'C2_at_internal_knots':True,
    'right_endpoint_P28':[int(x) for x in end]},indent=2)+'\n')
print(f'Created Fig2.12; {checks} exact comparisons and endpoint checks passed.')
