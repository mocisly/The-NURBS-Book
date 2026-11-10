#!/usr/bin/env python3
"""Smoke-test shared drawings through subfiles from both working directories.

Uses an isolated minimal parent, so pre-existing book errors cannot hide new
package/path errors. This does not claim that the full book compiles.
"""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    folder = ROOT / "image_tex/build/integration"
    (folder / "chapter").mkdir(parents=True, exist_ok=True)
    (folder / "image_tex").mkdir(exist_ok=True)
    shutil.copy2(ROOT / "image_tex/common.tex", folder / "image_tex/common.tex")
    targets = sorted((ROOT / "image_tex").glob("ch*/*.tex"))
    if not targets:
        raise SystemExit("No drawing sources found")
    for path in targets:
        target = folder / path.relative_to(ROOT)
        target.parent.mkdir(exist_ok=True)
        shutil.copy2(path, target)
    (folder / "main.tex").write_text(
        "\\documentclass{article}\n\\usepackage{amsmath,amssymb,bm}\n"
        "\\usepackage{subfiles}\n\\input{\\subfix{image_tex/common.tex}}\n"
        "\\begin{document}\n\\subfile{chapter/probe.tex}\n\\end{document}\n", encoding="utf-8")
    body = "\\documentclass[../main.tex]{subfiles}\n\\begin{document}\n"
    for path in targets:
        relative = path.relative_to(ROOT / "image_tex").as_posix()
        body += "\\begin{center}\\BookFigure[max width=.8\\linewidth,max height=.7\\textheight]{" + relative + "}\\end{center}\n\\clearpage\n"
    body += "\\end{document}\n"
    (folder / "chapter/probe.tex").write_text(body, encoding="utf-8")
    for cwd, filename in ((folder, "main.tex"), (folder / "chapter", "probe.tex")):
        pdf = cwd / Path(filename).with_suffix(".pdf")
        pdf.unlink(missing_ok=True)
        result = subprocess.run(["xelatex", "-halt-on-error", "-interaction=nonstopmode", "-no-shell-escape", filename],
                                cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
        (cwd / "console.txt").write_bytes(result.stdout)
        if result.returncode or not pdf.is_file():
            raise SystemExit(f"FAIL: {cwd / filename}; see console.txt")
        print(f"PASS: {cwd.relative_to(ROOT) / filename}", flush=True)


if __name__ == "__main__":
    main()
