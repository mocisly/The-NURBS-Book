#!/usr/bin/env python3
"""Reproduce the first reviewed examples; never overwrite existing drawings.

This is a curated set of native drawings, not an image-to-TikZ converter.
Run image_tex.py scan first. Numeric choices inferred from scans are documented.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "image_tex"


def basis(i, degree, u, knots):
    if degree == 0:
        return float(knots[i] <= u < knots[i + 1])
    a = knots[i + degree] - knots[i]
    b = knots[i + degree + 1] - knots[i + 1]
    return ((u - knots[i]) / a * basis(i, degree - 1, u, knots) if a else 0.0) + (
        (knots[i + degree + 1] - u) / b * basis(i + 1, degree - 1, u, knots) if b else 0.0)


def basis_picture():
    # The original is a schematic, with no numeric knot values in the caption.
    # Preserve its unequal knot spacing with inferred values; do not claim exact data.
    knots = [0.0, 3.0, 4.0, 7.0, 9.0]
    lines = [r"% Fig. 2.3: Cox-de Boor recurrence (2.5).",
             r"% Knot spacing [0,3,4,7,9] inferred from scan; illustrative, not original data.",
             r"\begin{tikzpicture}",
             r"\begin{axis}[width=13cm,height=6.8cm,axis lines=left,",
             r"xmin=-.4,xmax=10,ymin=0,ymax=1.35,ytick=\empty,",
             r"xtick={0,3,4,7,9},xticklabels={$u_i$,$u_{i+1}$,$u_{i+2}$,$u_{i+3}$,$u_{i+4}$},",
             r"axis line style={-{Stealth}},tick align=outside,clip=false]"]
    for fn in (lambda u: basis(0, 2, u, knots), lambda u: basis(1, 2, u, knots),
               lambda u: basis(0, 3, u, knots)):
        points = " ".join(f"({u:.5f},{fn(u):.7f})" for u in (9 * j / 360 for j in range(361)))
        lines.append(r"\addplot[book line,no marks] coordinates {" + points + "};")
    lines += [r"\addplot[book line] coordinates {(0,0) (7,1)};",
              r"\addplot[book line] coordinates {(3,1) (9,0)};",
              r"\draw[dashed] (axis cs:3,0) -- (axis cs:3,1);",
              r"\draw[dashed] (axis cs:7,0) -- (axis cs:7,1);",
              r"\node at (axis cs:.85,.99) {$\dfrac{u_{i+4}-u}{u_{i+4}-u_{i+1}}$};",
              r"\node at (axis cs:8.8,.99) {$\dfrac{u-u_i}{u_{i+3}-u_i}$};",
              r"\draw[book axis] (axis cs:1.0,.43) node[left] {$N_{i,2}$} -- (axis cs:2.25,.48);",
              r"\draw[book axis] (axis cs:4.35,.93) node[above] {$N_{i,3}$} -- (axis cs:3.95,.68);",
              r"\draw[book axis] (axis cs:8,.42) node[right] {$N_{i+1,2}$} -- (axis cs:6.85,.34);",
              r"\end{axis}", r"\end{tikzpicture}"]
    return "\n".join(lines) + "\n"


PIECEWISE = r"""% Fig. 2.1: schematic piecewise cubic; shape inferred from the scan.
% Bezier controls are illustrative; no numeric controls supplied in the text.
\begin{tikzpicture}[x=1cm,y=1cm,book line]
  \draw[book axis] (0,0) -- (12,0);
  \draw (0,3.3) .. controls (.7,4.5) and (1.9,5.2) .. (3.2,4.4)
    .. controls (4.4,3.7) and (5,2.5) .. (6.4,2.2)
    .. controls (7.9,1.4) and (9.1,1.8) .. (10.4,3.3);
  \foreach \x/\y in {0/3.3,3.2/4.4,6.4/2.2,10.4/3.3}
    \node[book point] at (\x,\y) {};
  \node[above] at (1.65,4.9) {$\mathbf C_1(u)$};
  \node[above right] at (4.35,3.5) {$\mathbf C_2(u)$};
  \node[above] at (8.6,2.7) {$\mathbf C_3(u)$};
  \draw[book axis] (0,.8) -- (0,2.8);
  \draw[book axis] (3.5,.8) -- (3.2,3.85);
  \draw[book axis] (7,.8) -- (6.4,1.7);
  \draw[book axis] (10.4,.8) -- (10.4,2.8);
  \foreach \x/\label in {0/{u_0=0},3.5/{u_1},7/{u_2},10.4/{u_3=1}} {
    \draw (\x,-.08) -- (\x,.08);
    \node[below=5pt] at (\x,0) {$\label$};
  }
\end{tikzpicture}
"""


def bilinear_picture():
    # Orthographic projection of 3D coordinates. Geometry is model-based,
    # viewpoint/scale are illustrative reconstructions of the original figure.
    def project(p):
        x, y, z = p
        return 3 * (-.78 * x + .96 * y), 3 * (-.5 * x - .3 * y + z)

    def coord(p):
        x, y = project(p)
        return f"({x:.5f},{y:.5f})"

    def surface(points, u, v):
        return tuple((1-u)*(1-v)*points[0][k] + u*(1-v)*points[1][k]
                     + (1-u)*v*points[2][k] + u*v*points[3][k] for k in range(3))

    def line(a, b, style="book grid"):
        return f"\\draw[{style}] {coord(a)} -- {coord(b)};"

    lines = [r"% Fig. 8.1: exact bilinear interpolation, equation (8.1).",
             r"% Representative coordinates and orthographic view inferred from scan.",
             r"\begin{tikzpicture}[book line]"]
    for offset, points, panel in (
        (10.5, [(1,0,.65), (1,1,0), (0,0,1), (0,1,.35)], "a"),
        (0, [(1,0,1), (1,1,0), (0,0,0), (0,1,1)], "b"),
    ):
        lines.append(f"\\begin{{scope}}[yshift={offset}cm]")
        if panel == "a":
            # Plane z=1-.35*x-.65*y with a margin around the surface.
            plane = [(x,y,1-.35*x-.65*y) for x,y in [(1.22,-.2),(1.22,1.2),(-.22,1.2),(-.22,-.2)]]
            lines.append("\\draw[dashed] " + " -- ".join(coord(p) for p in plane) + " -- cycle;")
            lines.append(r"\node at (-1.3,3) {$\Pi$};")
        else:
            for x in (0, 1):
                for y in (0, 1):
                    lines.append(line((x,y,0), (x,y,1), "dashed"))
            for z in (0, 1):
                for y in (0, 1):
                    lines.append(line((0,y,z), (1,y,z), "dashed"))
                for x in (0, 1):
                    lines.append(line((x,0,z), (x,1,z), "dashed"))
        for end, label in (((1.4,0,0), "x"), ((0,1.45,0), "y"), ((0,0,1.5), "z")):
            lines.append(line((0,0,0), end, "book axis"))
            anchor = "below left" if label == "x" else "above right"
            lines.append(f"\\node[{anchor}] at {coord(end)} {{${label}$}};")
        for j in range(21):
            t = j / 20
            # Isoparametric lines of a bilinear patch are straight, exactly.
            lines.append(line(surface(points,t,0), surface(points,t,1)))
            lines.append(line(surface(points,0,t), surface(points,1,t)))
        for p, label, anchor in zip(points, ["0,0", "1,0", "0,1", "1,1"],
                                    ["left", "below", "above", "right"]):
            if panel == "b" and label == "0,1":
                lines.append(f"\\fill {coord(p)} circle (1.6pt);")
                lines.append(r"\draw[book axis] (-2.3,.4) node[left] {$\mathbf P_{0,1}$} -- (-.12,.04);")
            else:
                lines.append(f"\\fill {coord(p)} circle (1.6pt) node[{anchor}=3pt] {{$\\mathbf P_{{{label}}}$}};")
        lines.append(f"\\node at (0,-4.1) {{({panel})}};")
        lines.append(r"\end{scope}")
    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines) + "\n"


def main():
    data = json.loads((BASE / "manifest.json").read_text(encoding="utf-8"))
    for item in data["images"]:
        target = ROOT / item["tex"]
        source = None
        if item["kind"] == "inline":
            source = "% Migrated from chapter/1.tex; native drawing retained.\n" + item["original"] + "\n"
            # Correct an existing TikZ node with missing node text.
            source = source.replace("node[right];", "node[right] {};")
        elif item["tex"] == "image_tex/ch02/fig_2_01.tex":
            source = PIECEWISE
        elif item["tex"] == "image_tex/ch02/fig_2_03.tex":
            source = basis_picture()
        elif item["tex"] == "image_tex/ch08/fig_8_01.tex":
            source = bilinear_picture()
        if source and not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source, encoding="utf-8")
            print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
