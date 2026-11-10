"""Editable semantic record/array cells for the implementation chapter."""
from fractions import Fraction as F
from native_bspline import point,number
def grid(x,y,widths,rows,h=F(4,5)):
    x,y=F(x),F(y);widths=tuple(map(F,widths));out=[];W=sum(widths);H=h*len(rows)
    out.append(r'\draw '+point((x,y))+' rectangle '+point((x+W,y-H))+';')
    for r,row in enumerate(rows):
        assert len(row)==len(widths);left=x
        if r:out.append(r'\draw[book grid] '+point((x,y-r*h))+'--'+point((x+W,y-r*h))+';')
        for w,label in zip(widths,row):
            out.append(r'\node at '+point((left+w/2,y-(r+F(1,2))*h))+' {'+label+'};');left+=w
    left=x
    for w in widths[:-1]:
        left+=w;out.append(r'\draw[book grid] '+point((left,y))+'--'+point((left,y-H))+';')
    return out
