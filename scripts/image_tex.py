#!/usr/bin/env python3
"""Inventory, preview, review, replace and restore this book's drawings.

Uses Python's standard library. Does not infer drawings from raster images.
Run `python scripts/image_tex.py --help` from any working directory.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "image_tex"
MANIFEST = BASE / "manifest.json"
IMAGE = re.compile(r"\\includegraphics\*?(?:\[(?P<options>[^\]]*)\])?\s*\{(?P<image>[^}]+)\}")
TIKZ = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.S)
CALL = re.compile(r"\\BookFigure\[(?P<options>[^\]]*)\]\{(?P<tex>[^}]+)\}")


def read(path):
    return path.read_bytes().decode("utf-8")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def uncomment(text):
    """Blank comments without moving offsets; an odd backslash count escapes %."""
    result = list(text)
    comment_end = -1
    for match in re.finditer(r"%", text):
        if match.start() < comment_end:
            continue
        pos = match.start()
        slashes = 0
        while pos > 0 and text[pos - 1] == "\\":
            pos -= 1
            slashes += 1
        if slashes % 2 == 0:
            end = re.search(r"[\r\n]", text[match.start():])
            comment_end = match.start() + end.start() if end else len(text)
            result[match.start():comment_end] = " " * (comment_end - match.start())
    return "".join(result)


def local(path):
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError(f"Path escapes repository: {path}")
    return resolved


def load():
    if not MANIFEST.exists():
        raise ValueError("Run scan first.")
    return json.loads(read(MANIFEST))


def save(data):
    write(MANIFEST, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def signature(entry):
    # Shared styles and preview harness changes invalidate both compile and review.
    paths = [local(entry["tex"]), BASE / "common.tex", Path(__file__)]
    h = hashlib.sha256()
    for path in paths:
        h.update(path.read_bytes())
    return h.hexdigest()


def select(data, args):
    entries = data["images"]
    if args.ids:
        wanted = set(args.ids)
        known = {e["id"] for e in entries}
        if wanted - known:
            raise ValueError(f"Unknown IDs: {sorted(wanted - known)}")
        entries = [e for e in entries if e["id"] in wanted]
    if args.chapter is not None:
        entries = [e for e in entries if e["chapter"] == args.chapter]
    if args.tex:
        wanted = set(args.tex)
        known = {e["tex"].removeprefix("image_tex/") for e in data["images"]}
        if wanted - known:
            raise ValueError(f"Unknown drawings: {sorted(wanted - known)}")
        entries = [e for e in entries if e["tex"].removeprefix("image_tex/") in wanted]
    return entries


def scan(_args):
    BASE.mkdir(exist_ok=True)
    previous = {e["id"]: e for e in load()["images"]} if MANIFEST.exists() else {}
    entries = []
    referenced = set()
    for chapter in sorted((ROOT / "chapter").glob("*.tex"), key=lambda p: int(p.stem)):
        text = read(chapter)
        active = uncomment(text)
        matches = list(IMAGE.finditer(text))
        chapter_entries = []
        for match in matches:
            image = match["image"].replace("\\", "/")
            if not image.startswith("images/"):
                continue
            is_active = active[match.start():match.start() + 16].startswith("\\includegraphics")
            # Two existing drawings follow commented-out raster commands.
            limit = next((m.start() for m in matches if m.start() > match.start()), len(text))
            drawing = TIKZ.search(active, match.end(), limit) if not is_active else None
            if not is_active and not drawing:
                # An applied inline drawing still has the historical comment.
                if not any(e["image"] == image and e.get("applied") for e in previous.values()):
                    continue
                continue
            ordinal = len(chapter_entries) + 1
            ident = f"ch{int(chapter.stem):02d}-{Path(image).stem}"
            old = previous.get(ident, {})
            item = dict(old)
            item.update(id=ident, image=image, chapter=int(chapter.stem),
                        chapter_file=chapter.relative_to(ROOT).as_posix(),
                        line=text.count("\n", 0, match.start()) + 1)
            item.setdefault("tex", f"image_tex/ch{int(chapter.stem):02d}/fig_{chapter.stem}_{ordinal:02d}.tex")
            item.setdefault("kind", "inline" if drawing else "raster")
            item.setdefault("options", "" if drawing else match["options"] or "")
            item.setdefault("original", text[drawing.start():drawing.end()] if drawing else match[0])
            item.setdefault("applied", False)
            item.setdefault("note", "")
            chapter_entries.append(item)
            referenced.add(image)
        # Applied entries no longer have an includegraphics command.
        calls = {m["tex"] for m in CALL.finditer(active)}
        for old in previous.values():
            if old["chapter"] == int(chapter.stem) and old.get("applied"):
                if old["tex"].removeprefix("image_tex/") not in calls:
                    raise ValueError(f"Applied reference is missing: {old['tex']}; restore or resolve manually.")
                if not any(e["id"] == old["id"] for e in chapter_entries):
                    chapter_entries.append(old)
                    referenced.add(old["image"])
        entries.extend(chapter_entries)
    for image_path in sorted((ROOT / "images").iterdir()):
        if not image_path.is_file():
            continue
        image = image_path.relative_to(ROOT).as_posix()
        if image in referenced:
            continue
        old = next((e for e in previous.values() if e["image"] == image), {})
        entries.append(old or dict(id="unused-" + image_path.stem, image=image, chapter=None,
                                   chapter_file=None, line=None, tex="image_tex/unused/" + image_path.stem + ".tex",
                                   kind="unused", applied=False, note="No active chapter reference."))
    # Do not silently drop previous records if a chapter was edited concurrently.
    lost = set(previous) - {e["id"] for e in entries}
    if lost:
        raise ValueError(f"Previous entries disappeared: {sorted(lost)}")
    if len({e["tex"] for e in entries}) != len(entries):
        raise ValueError("Duplicate target names; keep existing manifest names and resolve new names manually.")
    for entry in entries:
        local(entry["tex"]).parent.mkdir(parents=True, exist_ok=True)
    save(dict(version=1, images=sorted(entries, key=lambda e: (e["chapter"] or 999, e["tex"]))))
    status(_args)


def status(args):
    entries = select(load(), args)
    print(f"Images: {len(entries)}; kinds: {dict(Counter(e['kind'] for e in entries))}")
    present = [e for e in entries if local(e["tex"]).is_file()]
    print(f"Source files: {len(present)}; applied: {sum(e.get('applied', False) for e in entries)}")
    print(f"Current compiled: {sum(e.get('compiled') == signature(e) for e in present)}; "
          f"current reviewed: {sum(e.get('reviewed') == signature(e) for e in present)}")
    for entry in present:
        print(f"  {entry['tex']} ({'applied' if entry.get('applied') else 'not applied'})")


def tex_source_ok(entry):
    source = local(entry["tex"])
    if not source.is_file():
        raise ValueError(f"Drawing not created: {entry['tex']}")
    active = uncomment(read(source))
    if re.search(r"\\(?:includegraphics|includepdf|documentclass|input|include|BookFigure)\b", active):
        raise ValueError(f"Drawing must be self-contained native LaTeX: {entry['tex']}")
    if re.search(r"\\(?:pgfsys@|pgfsysprotocol@)", active):
        raise ValueError(f"Contour/system-layer output is retired; use semantic TikZ/PGFPlots and editable labels: {entry['tex']}")
    if not re.search(r"\\begin\{(?:tikzpicture|tabular|tabularx)\}", active):
        raise ValueError(f"No native drawing/table found: {entry['tex']}")


def preview(args):
    data = load()
    entries = [e for e in select(data, args) if local(e["tex"]).is_file()]
    if not entries:
        raise ValueError("No drawing sources for this selection.")
    engine = shutil.which("xelatex")
    if not engine:
        raise ValueError("XeLaTeX is not on PATH.")
    folder = BASE / "build"
    folder.mkdir(exist_ok=True)
    failures = []
    for entry in entries:
        tex_source_ok(entry)
        # Overwrite the wrapper and remove old artifacts so a failed build cannot pass.
        name = Path(entry["tex"]).stem + "_ch" + str(entry["chapter"])
        wrapper = folder / (name + ".tex")
        body = (r"\documentclass[border=10pt]{standalone}" + "\n" +
                r"\usepackage{amsmath,amssymb,bm}" + "\n" +
                r"\input{image_tex/common.tex}" + "\n")
        if args.dark:
            body += "\\definecolor{bookbg}{HTML}{181818}\n\\definecolor{bookfg}{HTML}{E0E0E0}\n"
            body += "\\pagecolor{bookbg}\n\\color{bookfg}\n"
        body += "\\begin{document}\n\\input{" + entry["tex"] + "}\n\\end{document}\n"
        write(wrapper, body)
        pdf = wrapper.with_suffix(".pdf")
        pdf.unlink(missing_ok=True)
        entry.pop("compiled", None)
        result = subprocess.run([engine, "-halt-on-error", "-interaction=nonstopmode",
                                 "-no-shell-escape", f"-output-directory={folder}", str(wrapper)],
                                cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
        write(wrapper.with_suffix(".console.txt"), result.stdout.decode("utf-8", errors="replace"))
        if result.returncode or not pdf.exists():
            failures.append(entry["tex"])
            print(f"FAIL {entry['tex']}; see {wrapper.with_suffix('.console.txt')}")
            continue
        entry["compiled"] = signature(entry)
        entry["preview_pdf"] = pdf.relative_to(ROOT).as_posix()
        entry["preview_theme"] = "dark" if args.dark else "light"
        if args.render:
            poppler = shutil.which("pdftoppm")
            if not poppler:
                failures.append("pdftoppm not on PATH")
            else:
                subprocess.run([poppler, "-png", "-singlefile", "-scale-to", "1600", str(pdf),
                                str(wrapper.with_suffix(""))], check=True, timeout=120)
        print(f"PASS {entry['tex']}")
    save(data)
    if failures:
        raise ValueError(f"Preview failures: {failures}")


def review(args):
    if not args.ids and not args.tex and args.chapter is None:
        raise ValueError("Select IDs or a chapter explicitly after inspecting previews.")
    data = load()
    entries = [e for e in select(data, args) if local(e["tex"]).is_file()]
    if not entries:
        raise ValueError("No drawing sources for this selection.")
    for entry in entries:
        tex_source_ok(entry)
        if entry.get("compiled") != signature(entry):
            raise ValueError(f"Compile current source before review: {entry['tex']}")
    for entry in entries:
        entry["reviewed"] = signature(entry)
        entry["note"] = args.note
    save(data)
    print(f"Recorded visual review for {len(entries)} drawings.")


def check(args):
    data = load()
    failures = []
    for entry in select(data, args):
        try:
            if not local(entry["image"]).is_file():
                raise ValueError(f"Missing original: {entry['image']}")
            if local(entry["tex"]).exists():
                tex_source_ok(entry)
            if entry.get("applied"):
                text = uncomment(read(local(entry["chapter_file"])))
                if text.count(entry["replacement"]) != 1:
                    raise ValueError(f"Applied reference missing or duplicated: {entry['tex']}")
                if entry.get("reviewed") != signature(entry) or entry.get("compiled") != signature(entry):
                    raise ValueError(f"Applied source changed since compile/review: {entry['tex']}")
        except (ValueError, OSError) as error:
            failures.append(str(error))
    if failures:
        raise ValueError("\n".join(failures))
    print("PASS: original files, native sources, applied references and verification signatures.")


def replace(args, restore=False):
    data = load()
    entries = select(data, args)
    plans = {}
    changed = []
    for entry in entries:
        if restore:
            if not entry.get("applied"):
                continue
        else:
            if entry.get("applied") or not local(entry["tex"]).exists():
                continue
            tex_source_ok(entry)
            digest = signature(entry)
            if entry.get("compiled") != digest or entry.get("reviewed") != digest:
                raise ValueError(f"Needs current compilation and visual review: {entry['tex']}")
        if entry["kind"] == "unused":
            continue
        path = local(entry["chapter_file"])
        content = plans.get(path, read(path))
        replacement = (r"\BookFigure[" + entry["options"] + "]{" +
                       entry["tex"].removeprefix("image_tex/") + "}")
        before, after = (entry["replacement"], entry["original"]) if restore else (entry["original"], replacement)
        if content.count(before) != 1 or (not restore and after in uncomment(content)):
            raise ValueError(f"Ambiguous or edited replacement in {entry['chapter_file']}: {entry['tex']}")
        plans[path] = content.replace(before, after, 1)
        entry["replacement"] = replacement
        entry["applied"] = not restore
        changed.append(entry)
    if not changed:
        print("No changes.")
        return
    # Validate every target first; keep backups as an additional recovery aid.
    for path, content in plans.items():
        backup = BASE / "backups" / path.relative_to(ROOT)
        if not backup.exists():
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, backup)
        write(path, content)
    save(data)
    print(f"{'Restored' if restore else 'Applied'} {len(changed)} drawings in {len(plans)} chapters.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["scan", "status", "preview", "review", "check", "apply", "restore"])
    parser.add_argument("--chapter", type=int)
    parser.add_argument("--ids", nargs="+")
    parser.add_argument("--tex", nargs="+", help="Drawing paths relative to image_tex, e.g. ch02/fig_2_01.tex")
    parser.add_argument("--render", action="store_true", help="Also render PNG previews with pdftoppm")
    parser.add_argument("--dark", action="store_true", help="Preview against the book's dark page")
    parser.add_argument("--note", default="", help="Review findings, fidelity and approximations")
    args = parser.parse_args()
    if args.command == "review" and not args.note.strip():
        parser.error("review requires --note with the actual visual review findings")
    try:
        if args.command == "restore":
            replace(args, restore=True)
        elif args.command == "apply":
            replace(args)
        else:
            globals()[args.command](args)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
