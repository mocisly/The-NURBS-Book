"""Behavioral checks for safe replacement, restoration and rescanning."""
import argparse
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import image_tex as pipeline
from create_image_tex_samples import basis


def args(**kwargs):
    options = dict(ids=None, tex=None, chapter=None, note="Visual check", render=False, dark=False)
    options.update(kwargs)
    return argparse.Namespace(**options)


class PipelineTests(unittest.TestCase):
    def setUp(self):
        build = pipeline.ROOT / "image_tex/build"
        build.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=build)
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.root = root
        self.base = root / "image_tex"
        self.base.mkdir()
        (root / "images").mkdir()
        (root / "chapter").mkdir()
        for name in ("a", "b", "unused"):
            (root / f"images/{name}.jpg").write_bytes(b"fixture")
        self.chapter = root / "chapter/1.tex"
        self.original = ('\ufeff% ignore \\includegraphics{images/unused.jpg}\r\n'
                         '\\includegraphics[max width=.8\\textwidth]{images/a.jpg}\r\n'
                         '\\includegraphics[width=2cm]{images/b.jpg}\r\n').encode("utf-8")
        self.chapter.write_bytes(self.original)
        self.addCleanup(patch.stopall)
        patch.object(pipeline, "ROOT", root).start()
        patch.object(pipeline, "BASE", self.base).start()
        patch.object(pipeline, "MANIFEST", self.base / "manifest.json").start()
        (self.base / "common.tex").write_text("% style\n")
        with contextlib.redirect_stdout(io.StringIO()):
            pipeline.scan(args())

    def ready(self, count=1):
        data = pipeline.load()
        for entry in data["images"][:count]:
            pipeline.write(pipeline.local(entry["tex"]), r"\begin{tikzpicture}\draw (0,0)--(1,1);\end{tikzpicture}")
            entry["compiled"] = entry["reviewed"] = pipeline.signature(entry)
        pipeline.save(data)

    def test_comments_and_unused(self):
        self.assertEqual(len(pipeline.load()["images"]), 3)
        self.assertEqual(sum(e["kind"] == "unused" for e in pipeline.load()["images"]), 1)
        active = pipeline.uncomment("x\\% visible % hidden \\includegraphics{bad}\nnext")
        self.assertIn(r"\% visible", active)
        self.assertNotIn("includegraphics", active)
        self.assertEqual(active.index("next"), len("x\\% visible % hidden \\includegraphics{bad}\n"))

    def test_byte_exact_roundtrip_and_idempotence(self):
        self.ready()
        pipeline.replace(args())
        applied = self.chapter.read_bytes()
        pipeline.replace(args())
        self.assertEqual(applied, self.chapter.read_bytes())
        pipeline.replace(args(), restore=True)
        self.assertEqual(self.original, self.chapter.read_bytes())

    def test_rescan_after_partial_apply_preserves_names(self):
        self.ready()
        pipeline.replace(args())
        before = {e["id"]: e["tex"] for e in pipeline.load()["images"]}
        pipeline.scan(args())
        after = {e["id"]: e["tex"] for e in pipeline.load()["images"]}
        self.assertEqual(before, after)
        pipeline.check(args())

    def test_restore_preserves_unrelated_edits(self):
        self.ready()
        pipeline.replace(args())
        self.chapter.write_bytes(self.chapter.read_bytes() + b"% later edit\r\n")
        pipeline.replace(args(), restore=True)
        self.assertEqual(self.chapter.read_bytes(), self.original + b"% later edit\r\n")

    def test_refuses_stale_or_missing_review(self):
        self.ready()
        data = pipeline.load()
        source = pipeline.local(data["images"][0]["tex"])
        source.write_bytes(source.read_bytes() + b"% changed")
        with self.assertRaisesRegex(ValueError, "current compilation"):
            pipeline.replace(args())
        self.assertEqual(self.original, self.chapter.read_bytes())

    def test_preflights_all_changes_before_writing(self):
        self.ready(2)
        self.chapter.write_bytes(self.chapter.read_bytes().replace(b"width=2cm", b"width=3cm"))
        before = self.chapter.read_bytes()
        with self.assertRaisesRegex(ValueError, "Ambiguous"):
            pipeline.replace(args())
        self.assertEqual(before, self.chapter.read_bytes())

    def test_escape_rejected(self):
        with self.assertRaisesRegex(ValueError, "escapes repository"):
            pipeline.local("../outside.tex")

    def test_rejects_retired_system_layer_contours(self):
        self.ready()
        entry = pipeline.load()["images"][0]
        pipeline.write(pipeline.local(entry["tex"]),
                       r"\begin{tikzpicture}\pgfsys@moveto{1pt}{2pt}\pgfsys@fill\end{tikzpicture}")
        with self.assertRaisesRegex(ValueError, "Contour/system-layer"):
            pipeline.tex_source_ok(entry)

    def test_basis_partition_and_recurrence(self):
        knots = [0, 0, 0, 0, 1, 2, 3, 3, 3, 3]
        for u in (.01, .5, 1, 1.7, 2.99):
            self.assertAlmostEqual(sum(basis(i, 3, u, knots) for i in range(6)), 1)
        self.assertEqual(basis(0, 2, 2, [0, 1, 2, 3]), .5)


if __name__ == "__main__":
    unittest.main()
