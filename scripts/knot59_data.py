"""Common representative surface for Fig5.9 and subsequent insertion examples."""
from fractions import Fraction as F
from knot51_data import insert
U=(F(0),)*4+(F(1),)*4
V=(F(0),)*3+(F(1,2),)+(F(1),)*3
xs=(F(3),F(1),F(-1),F(-3));ys=(F(-2),F(-3,5),F(3,5),F(2))
zu=(F(1),F(1),F(-6,5),F(-6,5));zv=(F(0),F(0),F(2),F(2))
P=tuple(tuple((xs[j],ys[i],zu[i]+zv[j]) for j in range(4)) for i in range(4))

def insert_surface(U,V,p,q,P,axis,value):
    if axis=='u':
        columns=[];alphas=None
        for j in range(len(P[0])):
            newU,column,aa=insert(U,tuple(row[j] for row in P),p,value)
            assert alphas is None or alphas==aa;alphas=aa;columns.append(column)
        Q=tuple(tuple(col[i] for col in columns) for i in range(len(P)+1))
        return newU,V,p,q,Q
    rows=[];alphas=None
    for row in P:
        newV,R,aa=insert(V,row,q,value)
        assert alphas is None or alphas==aa;alphas=aa;rows.append(R)
    return U,newV,p,q,tuple(rows)
