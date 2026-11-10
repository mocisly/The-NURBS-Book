from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
progress=json.loads((root/'image_tex/build/progress.json').read_text(encoding='utf-8')) if (root/'image_tex/build/progress.json').exists() else json.loads((root/'image_tex/progress.json').read_text(encoding='utf-8'))
note='''# LATEST LIVE OVERRIDE - 2026-11-09 after 10.17

352 applied /353 authored;82 ordinary+1 HTML pending. Chapters1..9 and printed10.1..10.17 all native/reviewed/applied/actual chapter visually checked and checkpointed. Current next10.18 source25 original493_316_247_890_829 VIEWED/prose READ, no math/native yet. 10.14 analytic orthogonal frame qualification fixed in prose. 10.15 exact transverse offset self-intersection;10.16 exact Frenet reversal/whole middle isocurve zero;10.17 actual Eq10.27 PN/Frenet comparison, preview and actualchapter12 VIEWED. Reports and creation/placement scripts retained. Root main.pdf remains published through10.13 (257pages/347 frozen applied/SHA fbb0f17e1ec6d2a6646f10389225c1e260c87f13e7d98fc163507de68ca53b04) until frame-sweeps batch is compiled/visually checked/published. Batch chapter10-frame-sweeps-batch.json created, freeze/compile status follows active tool handles. No agents/no commits/no contours/no final until all images+HTML+final book. Do not edit common.tex or image_tex.py. All older states below superseded.

'''
p=root/'image_tex/current_work.md';p.write_text(note+p.read_text(encoding='utf-8'),encoding='utf-8')
print(progress['applied_drawings'],progress['remaining_active_original_images'])
