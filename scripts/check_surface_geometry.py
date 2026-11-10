"""Validate tensor-product, de Casteljau and rational-weight diagram identities."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,re

ROOT=Path(__file__).resolve().parents[1]


def basis(n,i,t): return comb(n,i)*t**i*(1-t)**(n-i)


def main():
    source=(ROOT/'image_tex/ch01/fig_1_35.tex').read_text(encoding='utf-8')
    raw=re.search(r'\\foreach \\i/\\j/\\z in \{([^}]+)\}',source).group(1)
    controls={}
    for item in raw.split(','):
        i,j,z=item.split('/'); i,j=int(i),int(j)
        controls[i,j]=(2-F(4*j,3),2*i-2,F(z))
    report=json.loads((ROOT/'image_tex/build/surface-evaluation-data.json').read_text(encoding='utf-8'))
    u,v=F(report['u0']),F(report['v0'])
    q=[tuple(sum(basis(2,i,u)*controls[i,j][k] for i in range(3)) for k in range(3)) for j in range(4)]
    assert q==[tuple(F(x) for x in row) for row in report['Q']]
    direct=tuple(sum(basis(2,i,u)*basis(3,j,v)*controls[i,j][k]
                     for i in range(3) for j in range(4)) for k in range(3))
    assert direct==tuple(F(x) for x in report['S'])
    rational=(ROOT/'image_tex/ch01/fig_1_38.tex').read_text(encoding='utf-8')
    def expression(name):
        value=re.search(r'\\pgfmathdeclarefunction\{'+name+r'\}\{2\}\{\\pgfmathparse\{(.*?)\}\}',rational,re.S).group(1)
        return value.replace('#1','u').replace('#2','v').replace('^','**')
    def z(u,v): return sum(float(basis(2,i,u)*basis(3,j,v))*float(controls[i,j][2]) for i in range(3) for j in range(4))
    env={'__builtins__':{},'rprod':lambda u,v:(1-u)**2*3*v*(1-v)**2,'bezsurfz':z}
    formulas=[expression(n) for n in ['ratX','ratY','ratZ']]
    error=0.0
    for ui in range(21):
        for vi in range(21):
            u,v=F(ui,20),F(vi,20)
            weights={(i,j):basis(2,i,u)*basis(3,j,v)*(5 if (i,j)==(0,1) else 1)
                     for i in range(3) for j in range(4)}
            den=sum(weights.values()); assert den>0 and min(weights.values())>=0
            normalized=[x/den for x in weights.values()]; assert sum(normalized)==1
            weighted=tuple(sum(weights[i,j]*controls[i,j][k] for i,j in weights)/den for k in range(3))
            f=basis(2,0,u)*basis(3,1,v)
            assert weights[0,1]/den==5*f/(1+4*f)
            actual=[eval(expr,env,{'u':float(u),'v':float(v)}) for expr in formulas]
            error=max(error,max(abs(float(x)-y) for x,y in zip(weighted,actual)))
    assert error<1e-12,error
    # Independent homogeneous tensor-product evaluation of Ex1.15's cylinder.
    cylinder={(0,0):(1,1,0,1),(1,0):(1,1,1,1),(2,0):(2,0,2,2),
              (0,1):(-1,1,0,1),(1,1):(-1,1,1,1),(2,1):(-2,0,2,2)}
    for ui in range(21):
        for vi in range(21):
            u,v=F(ui,20),F(vi,20)
            h=tuple(sum(basis(2,i,u)*basis(1,j,v)*cylinder[i,j][k]
                        for i in range(3) for j in range(2)) for k in range(4))
            x,y,z=(h[k]/h[3] for k in range(3))
            assert (x,y,z)==(1-2*v,(1-u*u)/(1+u*u),2*u/(1+u*u))
            assert y*y+z*z==1
    out={'de_casteljau_matches_tensor_product_exactly':True,'rational_grid_samples':441,
         'rational_partition_positive':True,'rational_formula_max_error':error,
         'cylinder_exact_grid_samples':441,'cylinder_unit_radius_verified_exactly':True,
         'weights':'w01=5, all others=1'}
    (ROOT/'image_tex/build/surface-geometry-check.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2))


if __name__=='__main__': main()
