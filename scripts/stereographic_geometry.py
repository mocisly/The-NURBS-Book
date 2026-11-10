"""Exact homogeneous stereographic map of equation8.13 and its display sphere."""
from fractions import Fraction as F
from revolved_surface_data import U,CIRCLE,w
from rational_geometry import project
def lift_h(h,R=F(1)):
    u,v,a=h;g=u*u+v*v
    return (4*R*R*u*a,4*R*R*v*a,2*R*g,g+4*R*R*a*a)
def lift(u,v,R=F(1)):return project(lift_h((F(u),F(v),F(1)),R))
def sphere_net(R=F(1)):
    pts=[(0,0,0),(R,0,0),(R,0,R),(R,0,2*R),(0,0,2*R)]
    profile=tuple(tuple(F(x)*b for x in p)+(b,) for i,p in enumerate(pts) for b in [w if i%2 else F(1)])
    V=(F(0),)*3+(F(1,2),)*2+(F(1),)*3
    net=tuple(tuple((x*r,y*r,a*z,a*b) for r,_,z,b in profile) for x,y,a in CIRCLE)
    return U,V,net
