"""Recover the existing manifest record for figure12.3(c), without duplication."""
import image_tex as p
d=p.load();e=next(e for e in d['images']if '_581_354_248_827_744_0.jpg'in e['image'])
assert e['kind']=='unused'and not e.get('applied')and not(p.ROOT/e['tex']).exists()
s=(p.ROOT/'chapter/12.tex').read_text(encoding='utf-8');line=next(x for x in s.splitlines()if '<img src='in x);assert s.count(line)==1
e.update(kind='inline_ocr',chapter=12,chapter_file='chapter/12.tex',tex='image_tex/ch12/fig_12_03c.tex',original=line,options=r'max width=\linewidth',note='Recovered original12.3(c) HTML reference; same existing manifest record, native semantic redraw.')
p.save(d);print('Activated existing HTML figure12.3(c); no duplicate record.')
