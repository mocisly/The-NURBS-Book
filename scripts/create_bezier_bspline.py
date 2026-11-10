"""Fig3.1: exact clamped cubic B-spline/Bézier equivalence, native controls."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import argparse,json
from bspline_math import piece,evaluate,derivative

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--check-only',action='store_true')
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
target=root/'image_tex/ch03/fig_3_01.tex'
knots=(0,0,0,0,1,1,1,1)
controls=((0,0),(2,5),(7,6),(10,0)) # Representative: scan/text provide no coordinates.
pieces=[piece(knots,i,3,3) for i in range(4)]
for i,c in enumerate(pieces):
    bern=[F(0)]*4
    for j in range(i,4): bern[j]=F(comb(3,i)*comb(3-i,j-i)*(-1)**(j-i))
    assert [evaluate(c,F(k,10)) for k in range(11)]==[evaluate(bern,F(k,10)) for k in range(11)]
for k in range(1001):
    u=F(k,1000);weights=[evaluate(c,u) for c in pieces]
    assert min(weights)>=0 and sum(weights)==1
    curve=tuple(sum(weights[i]*controls[i][axis] for i in range(4)) for axis in range(2))
    cast=[tuple(map(F,p)) for p in controls]
    for r in range(1,4):
        cast=[tuple((1-u)*a+u*b for a,b in zip(cast[i],cast[i+1])) for i in range(4-r)]
    assert curve==cast[0]
for axis in range(2):
    left=sum(evaluate(derivative(c),F(0))*controls[i][axis] for i,c in enumerate(pieces))
    right=sum(evaluate(derivative(c),F(1))*controls[i][axis] for i,c in enumerate(pieces))
    assert left==3*(controls[1][axis]-controls[0][axis])
    assert right==3*(controls[3][axis]-controls[2][axis])
(root/'image_tex/build/bezier-bspline-check.json').write_text(json.dumps({
    'knots':knots,'representative_controls':controls,
    'exact_bspline_decasteljau_grid_points':1001,
    'partition_nonnegative':True,'endpoint_tangents_verified':True},indent=2)+'\n')
if not args.check_only:
    assert not target.exists()
    lines=['% Fig3.1: clamped cubic U=(0,0,0,0,1,1,1,1), property P3.1.',
           '% Representative controls (0,0),(2,5),(7,6),(10,0); no coordinates in text.',
           '% Exact native cubic Bezier, equal to the clamped B-spline; no tracing.',
           r'\begin{tikzpicture}[x=1cm,y=1cm,book line]']
    for i,(x,y) in enumerate(controls): lines.append(r'\coordinate (P'+str(i)+') at ('+f'{x},{y}'+');')
    lines += [r'\draw[book grid] (P0)--(P1)--(P2)--(P3);',
              r'\draw (P0) .. controls (P1) and (P2) .. (P3);',
              r'\foreach \i in {0,...,3} \node[book point] at (P\i) {};',
              r'\node[below left=4pt] at (P0) {$\mathbf P_0$};',
              r'\node[above left=4pt] at (P1) {$\mathbf P_1$};',
              r'\node[above=4pt] at (P2) {$\mathbf P_2$};',
              r'\node[below right=4pt] at (P3) {$\mathbf P_3$};',
              r'\end{tikzpicture}']
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print('PASS: 1001 exact B-spline/de Casteljau comparisons, endpoint tangents and convex weights.'+(' No TeX input changed.' if args.check_only else ' Created Fig3.1 source.'))
