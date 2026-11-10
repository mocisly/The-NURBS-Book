#!/usr/bin/env python3
"""Native reconstructions of the next six scans in chapter 1.

Equations and geometry are exact for the representative data selected here.
The scans do not supply numeric coordinates or a camera; these are inferred
illustrative choices, not recovered source data. Existing drawings are kept.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def coord(point):
    return "(" + ",".join(f"{value:.6f}" for value in point) + ")"


def sphere():
    def project(p):
        x, y, z = p
        return ((-x+y)/math.sqrt(2), (-x-y+2*z)/math.sqrt(6))

    lines = [r"% Fig. 1.3: unit sphere, equation (1.3); orthographic view chosen for clarity.",
             r"\begin{tikzpicture}[x=2.8cm,y=2.8cm,book line]",
             r"\draw (0,0) circle (1);"]
    for plane in range(3):
        # Continuous paths avoid seams and preserve the hidden-line dash phase.
        for visible in (True, False):
            segment = []
            prefix = "\\draw" + ("" if visible else "[dashed]") + " plot coordinates {"
            for index in range(361):
                a = math.radians(index)
                p = ([0, math.cos(a), math.sin(a)] if plane == 0 else
                     [math.cos(a), 0, math.sin(a)] if plane == 1 else
                     [math.cos(a), math.sin(a), 0])
                if (sum(p) >= 0) == visible:
                    segment.append(project(p))
                elif segment:
                    segment.append(project(p))
                    lines.append(prefix + " ".join(coord(p) for p in segment) + "};")
                    segment = []
            if segment:
                lines.append(prefix + " ".join(coord(p) for p in segment) + "};")
    for axis, label in enumerate("xyz"):
        unit = [0,0,0]
        unit[axis] = 1
        end = [1.65*x for x in unit]
        lines.append("\\draw[dashed] (0,0) -- " + coord(project(unit)) + ";")
        lines.append("\\draw[book axis] " + coord(project(unit)) + " -- " + coord(project(end)) + f" node[{'above' if axis==2 else 'below'}] {{${label}$}};")
    radius = project((-.2,.4,math.sqrt(.8)))
    lines += ["\\draw[book axis,dashed] (0,0) -- " + coord(radius) + ";",
              r"\node[right] at (.85,.7) {$R=1$};", r"\end{tikzpicture}"]
    return "\n".join(lines) + "\n"


def surface_frame():
    # Representative curved patch S(u,v)=(-v,u,1-.6u^2).
    # Su=(0,1,-1.2u), Sv=(-1,0,0), Su x Sv=(0,1.2u,1).
    def project(p):
        x, y, z = p
        return (-.9*x+.8*y, -.2*x-.65*y+z)

    def surface(u,v):
        return (-v,u,1-.6*u*u)

    def curve(points):
        return "\\draw plot coordinates {" + " ".join(coord(project(p)) for p in points) + "};"

    lines = [r"% Fig. 1.4: differential frame, equation (1.4).",
             r"% Representative patch S(u,v)=(-v,u,1-.6u^2); chosen coordinates/view.",
             r"\begin{tikzpicture}[x=3.2cm,y=3.2cm,book line]"]
    for end,label,anchor in (((1.35,0,0),"x","below left"),((0,1.6,0),"y","below right"),((0,0,1.85),"z","above")):
        lines.append("\\draw[book axis] (0,0) -- " + coord(project(end)) + f" node[{anchor}] {{${label}$}};")
    for v in (-.75,.05,.8):
        lines.append(curve([surface(-.8+1.8*j/100,v) for j in range(101)]))
    for u in (-.8,.45,1):
        lines.append(curve([surface(u,v) for v in (-.75,.8)]))
    point = surface(.45,.05)
    p = project(point)
    su = project((0,1,-.54))
    sv = project((-1,0,0))
    length = math.sqrt(1+.54**2)
    normal = project((0,.54/length,1/length))
    lines.append("\\fill " + coord(p) + " circle (.6pt);")
    for delta,label,anchor,scale in ((su,r"\mathbf S_u","below right",1.0),(sv,r"\mathbf S_v","right",1.1),(normal,r"\mathbf N","above right",1.25)):
        end = tuple(p[k]+scale*delta[k] for k in range(2))
        lines.append("\\draw[book axis,thick] " + coord(p) + " -- " + coord(end) + f" node[{anchor}] {{${label}$}};")
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines) + "\n"


LINE = r"""% Fig. 1.5: C(u)=a0+u*a1, 0<=u<=1; representative coordinates.
\begin{tikzpicture}[book line]
  \coordinate (A) at (0,0);
  \coordinate (B) at (5.2,3.4);
  \draw[book axis] (A) -- (B) node[pos=.5,above left] {$\mathbf a_1$};
  \node[book point,label=below:{$\mathbf a_0$}] at (A) {};
  \node[book point,label=above right:{$\mathbf a_0+\mathbf a_1$}] at (B) {};
\end{tikzpicture}
"""

PARABOLA = r"""% Fig. 1.6: C(u)=(0,0)+(4,3)u+(0,-3)u^2.
% Exact quadratic, with exact endpoint tangent directions; representative data.
\begin{tikzpicture}[book line]
  \draw plot[domain=0:1,samples=81] ({4*\x},{3*\x-3*\x*\x});
  \draw[book axis] (0,0) -- (4.8,3.6)
    node[pos=.58,above left] {$\mathbf a_1$};
  \draw[book axis] (4,0) -- (6.4,-1.8)
    node[pos=.65,right=4pt] {$\mathbf a_1+2\mathbf a_2$};
  \node[book point,label=below left:{$\mathbf a_0$}] at (0,0) {};
  \node[book point,label=above right:{$\mathbf a_0+\mathbf a_1+\mathbf a_2$}] at (4,0) {};
\end{tikzpicture}
"""

PARALLEL_A = r"""% Fig. 1.7(a): a1 and a2 have the same direction.
% In local coordinates a1=(3,0), a2=(2,0); C(u)=3u+2u^2.
\begin{tikzpicture}[book line]
  \begin{scope}[rotate=35]
    \draw (0,0) -- (5,0);
    \draw[book axis] (0,.7) -- (3,.7) node[midway,above] {$\mathbf a_1$};
    \draw[book axis] (0,-.7) -- (2,-.7) node[midway,below] {$\mathbf a_2$};
    \node[book point,label=left:{$\mathbf a_0$}] at (0,0) {};
    \node[book point,label=right:{$\mathbf a_0+\mathbf a_1+\mathbf a_2$}] at (5,0) {};
  \end{scope}
  \node at (2,-1.6) {(a)};
\end{tikzpicture}
"""

PARALLEL_B = r"""% Fig. 1.7(b): a1=(6,0), a2=(-4,0); C(u)=6u-4u^2.
% C'(u0)=0 at u0=3/4. C(u0)=2.25, C(1)=2; final part retraced.
\begin{tikzpicture}[book line]
  \begin{scope}[rotate=48]
    \draw (0,0) -- (2.25,0);
    \draw[book axis] (.7,.7) -- (6.7,.7)
      node[midway,above left=6pt] {$\mathbf a_1$};
    \draw[book axis] (2,-.7) -- (-2,-.7)
      node[midway,below right=6pt] {$\mathbf a_2$};
    \node[book point,label=left:{$\mathbf a_0$}] at (0,0) {};
    \node[book point,label=right:{$\mathbf a_0+\mathbf a_1+\mathbf a_2$}] at (2,0) {};
    \fill (2.25,0) circle (.8pt);
    \draw[book axis,thin,dashed] (3.5,-.6) node[right] {$\mathbf C(u_0)$} -- (2.25,0);
  \end{scope}
  \node at (1,-2.4) {(b)};
\end{tikzpicture}
"""


def main():
    drawings = {"03": sphere(), "04": surface_frame(), "05": LINE,
                "06": PARABOLA, "07": PARALLEL_A, "08": PARALLEL_B}
    for suffix, source in drawings.items():
        target = ROOT / "image_tex/ch01" / f"fig_1_{suffix}.tex"
        if target.exists():
            continue
        target.write_text(source, encoding="utf-8")
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
