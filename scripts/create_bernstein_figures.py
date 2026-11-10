"""Author Fig. 1.13 from its Bernstein definition, with editable labels."""
from pathlib import Path
from math import comb

ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    1: [(0,.2,.88),(1,.78,.88)],
    2: [(0,.25,.85),(1,.5,.62),(2,.75,.85)],
    3: [(0,.13,.83),(1,.29,.57),(2,.71,.57),(3,.87,.83)],
    9: [(0,.09,.78),(1,.16,.5),(8,.84,.5),(9,.91,.78)],
}


def main():
    for ordinal, (degree, labels) in enumerate(LABELS.items(),18):
        path = ROOT / f"image_tex/ch01/fig_1_{ordinal}.tex"
        if path.exists():
            raise FileExistsError(path)
        lines = [f"% Fig. 1.13({chr(ordinal-18+97)}): exact degree-{degree} Bernstein basis.",
                 r"\begin{tikzpicture}[x=6cm,y=3.7cm,book line,line cap=round]",
                 r"\path[use as bounding box] (-.11,-.35) rectangle (1.16,1.18);",
                 r"\draw[book axis,line width=.45pt] (0,0)--(1.09,0) node[right] {$u$};",
                 r"\draw[book axis,line width=.45pt] (0,0)--(0,1.12);",
                 r"\node[below left] at (0,0) {$0$};",
                 r"\foreach \x/\label in {.5/{\frac12},1/1}",
                 r"  \draw[line width=.45pt] (\x,0)--++(0,-2pt) node[below] {$\label$};",
                 r"\draw[line width=.45pt] (0,1)--++(-2pt,0) node[left] {$1$};"]
        for i in range(degree+1):
            factors = [str(comb(degree,i))]
            if i:
                factors.append(r"\u" if i==1 else rf"\u^{i}")
            if degree-i:
                factors.append(r"(1-\u)" if degree-i==1 else rf"(1-\u)^{degree-i}")
            lines.append(r"\draw plot[variable=\u,domain=0:1,samples=121] ({\u},{"+"*".join(factors)+"});")
        for i,x,y in labels:
            lines.append(rf"\node at ({x},{y}) {{$B_{{{i},{degree}}}$}};")
        if degree==9:
            lines.append(r"\node at (.5,.5) {$\cdots$};")
        lines.extend([rf"\node at (.5,-.27) {{({chr(ordinal-18+97)}) $n={degree}$}};",
                      r"\end{tikzpicture}"])
        path.write_text("\n".join(lines)+"\n",encoding="utf-8")


if __name__ == "__main__":
    main()
