"""Author Fig.1.25 by evaluating the documented Fig.1.24 control net."""
from pathlib import Path
from fractions import Fraction as F
import json

ROOT=Path(__file__).resolve().parents[1]


def mix(a,b,t):
    return tuple((1-t)*x+t*y for x,y in zip(a,b))


def point(p):
    return '('+','.join(f'{float(x):.9f}' for x in p)+')'


def main():
    target=ROOT/'image_tex/ch01/fig_1_36.tex'
    if target.exists(): raise FileExistsError(target)
    u,v=F(21,50),F(9,20)
    z=[[F(str(x)) for x in row] for row in [[0,2.2,.8,3],[.2,2.8,1.3,3.5],[-.9,.9,.4,2]]]
    p=[[(2-F(4*j,3),2*i-2,z[i][j]) for j in range(4)] for i in range(3)]
    q=[mix(mix(p[0][j],p[1][j],u),mix(p[1][j],p[2][j],u),u) for j in range(4)]
    levels=[q]
    while len(levels[-1])>1:
        levels.append([mix(a,b,v) for a,b in zip(levels[-1],levels[-1][1:])])
    s=levels[-1][0]
    base=(ROOT/'image_tex/ch01/fig_1_35.tex').read_text(encoding='utf-8')
    start=base.index(r'\begin{tikzpicture}')
    body=base[start:].replace(r'\node at (canvas cs:x=.5cm,y=-4cm) {(b)};', '')
    body=body.removesuffix('\\end{tikzpicture}\n')
    body=body.replace('x=6.4cm,y=5.1cm','x=18.9cm,y=5.1cm',1)
    # Keep the same surface and camera; labels belong to the isolated right panel.
    for line in body.splitlines():
        if r'\node[' in line and r'\mathbf P_' in line:
            body=body.replace(line+'\n','')
    body=body.replace(r'\begin{tikzpicture}',r'\begin{tikzpicture}',1)
    lines=['% Fig.1.25: same degree-(2,3) surface/control net as Fig.1.24(b).',
           '% u0=21/50, v0=9/20. Qj and all de Casteljau levels computed with rational arithmetic.',
           '% Right panel magnifies the same projection by 1.35; all text retains book font size.',body]
    for j,a in enumerate(q): lines.append(rf'\coordinate (Q{j}) at {point(a)};')
    lines.extend([rf'\coordinate (S) at {point(s)};',
                  r'\draw[line width=1pt] (Q0) .. controls (Q1) and (Q2) .. (Q3);',
                  r'\fill (S) circle (1.7pt);',
                  r'\node at (canvas cs:x=-4.1cm,y=1.2cm) {$\mathbf S(u_0,v_0)$};',
                  r'\draw[-{Stealth[length=4pt]},line width=.35pt] (canvas cs:x=-3.2cm,y=1.2cm)--([xshift=-3pt]S);',
                  r'\node at (canvas cs:x=.5cm,y=-4cm) {(a)};',
                  r'\begin{scope}[xshift=12.5cm,yshift=-.8cm,x={(-1.215cm,-.6075cm)},y={(1.485cm,-.3375cm)},z={(0cm,1.35cm)}]',
                  r'\path[use as bounding box] (canvas cs:x=-5.5cm,y=-3.4cm) rectangle (canvas cs:x=6.4cm,y=5.9cm);'])
    for k,level in enumerate(levels):
        for j,a in enumerate(level): lines.append(rf'\coordinate (L{k}{j}) at {point(a)};')
        if len(level)>1:
            chain='--'.join(f'(L{k}{j})' for j in range(len(level)))
            lines.append(r'\draw[line width='+('.45pt' if k==0 else '.35pt')+(','+'dashed' if k>0 else '')+'] '+chain+';')
    lines.append(r'\draw[line width=1pt] (L00) .. controls (L01) and (L02) .. (L03);')
    for j,pos in enumerate(['below left','above left','right','above right']):
        lines.append(rf'\node[book point,label={pos}:{{$\mathbf Q_{j}(u_0)$}}] at (L0{j}) {{}};')
    for k in [1,2]:
        for j in range(len(levels[k])):
            lines.append(rf'\draw (L{k}{j}) circle (1.1pt);')
    lines.extend([r'\fill (L30) circle (1.7pt);',
                  r'\node at (canvas cs:x=-3.5cm,y=2cm) {$\mathbf S(u_0,v_0)$};',
                  r'\draw[-{Stealth[length=4pt]},line width=.35pt] (canvas cs:x=-2.6cm,y=1.9cm)--([xshift=-3pt]L30);',
                  r'\node at (canvas cs:x=.5cm,y=-3.2cm) {(b)};',
                  r'\end{scope}',r'\end{tikzpicture}'])
    target.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    report={'u0':str(u),'v0':str(v),'Q':[[str(x) for x in a] for a in q],
            'S':[str(x) for x in s],'levels':[[[str(x) for x in a] for a in l] for l in levels]}
    (ROOT/'image_tex/build/surface-evaluation-data.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__': main()
