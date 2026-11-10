"""Unscaled-font common geometry for staircase surface comparisons9.45..47."""
from fractions import Fraction as F
from surface_approximation_example_data import Q,X,Y
from surface_least_squares_data import sqrt_bounds,VP
from surface_geometry import isocurve,surface
from native_bspline import segments,check,cubic_path,point,de_boor
def view(p):
    x,y,z=p;return (2*(-F(4,5)*x+F(9,10)*y),2*(-F(2,5)*x-F(7,20)*y+z))
def draw(base,letter=None,squares=None):
    out=[r'\begin{tikzpicture}[book line]',r'\path[use as bounding box] (-7.6,-4) rectangle (7.6,9);'];native=iso=0
    if squares is None:
        fixed=tuple(sorted(set(tuple(F(i,32) for i in range(33))+VP)))
        for v in fixed:
            K,p,C=isocurve(*base,'u',v);ss=segments(K,C,p);native+=check(K,C,p,ss,steps=4)
            for u in (F(0),F(1,3),F(2,3),F(1)):
                assert de_boor(K,C,p,u)==surface(*base,u,v);iso+=1
            out.extend(cubic_path(dict(bern=tuple(view(p) for p in s['bern']))) for s in ss)
        out.extend(r'\fill '+point(view(p))+r' circle[radius=.95pt];' for row in Q for p in row)
    else:
        E=tuple(tuple((X[i],Y[j],2*sum(sqrt_bounds(squares[i][j]))) for j in range(9)) for i in range(9))
        for lines in (E,tuple(zip(*E))):
            for row in lines:out.append(r'\draw[book grid] '+'--'.join(point(view(p)) for p in row)+';')
    for end,name,anchor in [((F(3),0,0),'x','below left'),((0,F(3),0),'y','below right'),((0,0,F(7,2)),'z' if squares is None else '4e','above')]:
        out.append(r'\draw[book grid,book axis] (0,0)--'+point(view(end))+r' node['+anchor+r'=5pt] {$'+name+'$};')
    if letter:out.append(r'\node at (0,-3.55) {('+letter+')};')
    out.append(r'\end{tikzpicture}')
    return '\n'.join(out)+'\n',dict(native_curve_checks=native,isocurve_tensor_crosschecks=iso,displayed_isocurves=len(fixed) if squares is None else 0,camera_scale=2,error_vertical_magnification=4,font_rescaling=False)
