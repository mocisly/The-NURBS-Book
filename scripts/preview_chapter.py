"""Compile one chapter using the book's exact preamble, geometry and fonts."""
import argparse
import re
from pathlib import Path
import shutil
import subprocess
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chapter", type=int)
    args = parser.parse_args()
    main_source = (ROOT / "main.tex").read_text(encoding="utf-8")
    source_hashes={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in [ROOT/'main.tex',ROOT/f'chapter/{args.chapter}.tex']}
    preamble = main_source.split(r"\begin{document}", 1)[0]
    chapter_line = next(line for line in main_source.splitlines()
                        if line.startswith(r"\chapter{") and
                        rf"\label{{sec:{args.chapter}}}" in line)
    build = ROOT / "image_tex" / "build" / "chapter-review"
    build.mkdir(parents=True, exist_ok=True)
    wrapper = build / f"chapter-{args.chapter}.tex"
    uses_minted = r"\usepackage{minted}" in preamble
    options = (f"\\PassOptionsToPackage{{outputdir={build.relative_to(ROOT).as_posix()}}}{{minted}}\n"
               if uses_minted else "")
    wrapper.write_text(options + preamble + "\n\\begin{document}\n" + chapter_line +
                       f"\n\\subfile{{chapter/{args.chapter}.tex}}\n\\end{{document}}\n",
                       encoding="utf-8")
    engine = shutil.which("xelatex") or r"C:\Programs\texlive\2024\bin\windows\xelatex.exe"
    output = build / f"chapter-{args.chapter}.console.txt"
    with output.open("w", encoding="utf-8") as log:
        result = subprocess.run([engine, "-interaction=nonstopmode", "-halt-on-error",
                                 "-shell-escape" if uses_minted else "-no-shell-escape",
                                 f"-output-directory={build}", str(wrapper)],
                                cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, text=True)
    if result.returncode:
        print(output.read_text(encoding="utf-8")[-6000:])
        return result.returncode
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in source_hashes.items()),'Source changed during chapter compilation'
    wrapper.with_suffix('.compile.json').write_text(json.dumps(dict(chapter=args.chapter,exit_code=0,source_hashes=source_hashes),indent=2)+'\n',encoding='utf-8')
    pdf = wrapper.with_suffix(".pdf")
    subprocess.run(["pdftotext", "-layout", str(pdf), str(wrapper.with_suffix(".txt"))], check=True)
    pages = wrapper.with_suffix(".txt").read_text(encoding="utf-8").split("\f")
    for index, page in enumerate(pages, 1):
        captions = [line.strip() for line in page.splitlines()
                    if re.match(r"^\s*(图|表)\s*\d+\.", line)]
        if captions:
            print(f"Page {index}: " + " | ".join(captions))
    print(pdf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
