"""Native curve, data constraints and true common-scale derivative arrows."""
from fractions import Fraction as F
from native_bspline import point,cubic_path
from weighted_constrained_curve_data import Q
def drawing(P,ss,points,derivatives,weight_labels=()):
    out=[r'\begin{tikzpicture}[book line,x=2.6cm,y=2.6cm]',r'\path[use as bounding box] (-.8,-2) rectangle (8.6,4.8);',r'\draw[book grid,dashed] '+'--'.join(map(point,P))+';']
    out.extend(cubic_path(s) for s in ss)
    for k,D in derivatives.items():
        tip=tuple(x+y/10 for x,y in zip(Q[k],D));out.append(r'\draw[book axis] '+point(Q[k])+'--'+point(tip)+';')
    for i,q in enumerate(Q):
        out.append(r'\draw '+point(q)+(r' ++(-2.8pt,-2.8pt) rectangle ++(5.6pt,5.6pt);' if i in points else r' circle[radius=2.4pt];'))
    for xy,label in weight_labels:out.append(r'\node at '+point(xy)+' {$'+label+'$};')
    out.append(r'\end{tikzpicture}');return out
