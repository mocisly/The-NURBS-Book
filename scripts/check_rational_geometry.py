"""Check the mathematical identities used by the authored rational diagrams."""
from math import comb
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]


def coordinates(source):
    return {name:tuple(map(float,values.split(',')))
            for name,values in re.findall(r'\\coordinate\s*\(([^)]+)\)\s*at\s*\(([-.\d,]+)\)',source)}


def blend(points,u):
    degree=len(points)-1
    return tuple(sum(comb(degree,i)*u**i*(1-u)**(degree-i)*p[k]
                     for i,p in enumerate(points)) for k in range(len(points[0])))


def main():
    cubic=(ROOT/'image_tex/ch01/fig_1_31.tex').read_text(encoding='utf-8')
    values=coordinates(cubic)
    controls=[values[f'P{i}'] for i in range(4)]
    lift=[values[f'Q{i}'] for i in range(4)]
    expressions={name:value.replace(r'\u','u').replace('^','**')
                 for name,value in re.findall(r'\\def\\(XX|YY|Den)\{([^}]+)\}',cubic)}
    for p,q in zip(controls,lift):
        assert max(abs(p[k]*q[2]-q[k]) for k in range(2))<1e-12
    weights=(1,3,7,1)
    basis_source=(ROOT/'image_tex/ch01/fig_1_28.tex').read_text(encoding='utf-8')
    denominator=re.search(r'\\def\\RDen\{([^}]+)\}',basis_source).group(1).replace(r'\u','u').replace('^','**')
    circle_source=(ROOT/'image_tex/ch01/fig_1_32.tex').read_text(encoding='utf-8')
    circle=coordinates(circle_source)
    circle_lift=[circle['P0'],circle['P1'],circle['Q2']]
    max_error=0.0
    for j in range(1001):
        u=j/1000
        basis=[comb(3,i)*u**i*(1-u)**(3-i)*w for i,w in enumerate(weights)]
        den=eval(denominator,{'__builtins__':{}},{'u':u})
        assert den>0 and min(basis)>=0
        max_error=max(max_error,abs(sum(basis)/den-1))
        q=blend(lift,u)
        written=tuple(eval(expressions[name],{'__builtins__':{}},{'u':u}) for name in ('XX','YY','Den'))
        max_error=max(max_error,max(abs(a-b) for a,b in zip(q,written)))
        direct=tuple(sum(comb(3,i)*u**i*(1-u)**(3-i)*lift[i][2]*controls[i][k]
                         for i in range(4))/q[2] for k in range(2))
        max_error=max(max_error,max(abs(direct[k]-q[k]/q[2]) for k in range(2)))
        arc=blend(circle_lift,u)
        explicit=(1-u*u,2*u,1+u*u)
        max_error=max(max_error,max(abs(a-b) for a,b in zip(arc,explicit)))
        x,y=arc[0]/arc[2],arc[1]/arc[2]
        max_error=max(max_error,abs(x*x+y*y-1))
    assert blend(circle_lift,.5)==circle['Rw']==(.75,1,1.25)
    assert circle['R']==(.6,.8,1)
    assert max_error<1e-12,max_error
    report={'samples':1001,'max_error':max_error,
            'checks':['positive rational denominator','partition of unity',
                      'homogeneous lift coefficients','central projection identity',
                      'unit circle identity','midpoint homogeneous de Casteljau data']}
    out=ROOT/'image_tex/build/rational-geometry-check.json'
    out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'PASS: {len(report["checks"])} geometry identities, 1001 samples, max error {max_error:.3g}')


if __name__=='__main__':
    main()
