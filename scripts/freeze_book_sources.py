"""Freeze a reviewed batch's complete TeX input tree for an independent book build.

Run BEFORE starting that batch's compiler. The working chapters may then evolve
while the frozen book compiles. The publisher verifies frozen hashes and reports
the frozen manifest's counts, so later edits cannot be mistaken for compiled work.
"""
from pathlib import Path
from datetime import datetime
import argparse,hashlib,json,re,shutil
import image_tex as p

a=argparse.ArgumentParser(description=__doc__);a.add_argument('batch',type=Path);args=a.parse_args()
root=p.ROOT;batch=json.loads(args.batch.read_text(encoding='utf-8'))
assert re.fullmatch(r'[A-Za-z0-9_-]+',batch['id'])
assert not batch.get('source_snapshot'),'This batch already has a frozen source tree.'
name=batch['id']+'-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')
snapshot=(root/'image_tex/build/book-snapshots'/name).resolve()
assert root.resolve() in snapshot.parents and not snapshot.exists()
sources=set(root.glob('*.tex'))
for suffix in ('.cls','.sty','.bst','.bib'):sources.update(root.glob('*'+suffix))
for folder in ('chapter','cover','preface','introduction','colophon','images'):
    sources.update(path for path in (root/folder).rglob('*') if path.is_file())
sources.add(root/'image_tex/common.tex')
for folder in (root/'image_tex').glob('ch[0-9][0-9]'):
    sources.update(path for path in folder.rglob('*') if path.is_file())
data=p.load();snapshot.mkdir(parents=True);hashes={}
for source in sorted(sources):
    relative=source.relative_to(root);target=snapshot/relative;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,target)
    hashes[relative.as_posix()]=hashlib.sha256(target.read_bytes()).hexdigest()
for entry in data['images']:
    if entry.get('applied'):
        assert (snapshot/entry['tex']).exists()
        assert (snapshot/entry['chapter_file']).read_text(encoding='utf-8').count(entry['replacement'])==1
        assert entry['compiled']==entry['reviewed']==p.signature(entry)
manifest=snapshot/'image_tex/manifest.json';manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
metadata={'id':name,'batch_id':batch['id'],'input_sha256':hashes,
          'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),
          'applied_drawings':sum(bool(e.get('applied')) for e in data['images']),
          'authored_sources':sum((snapshot/e['tex']).is_file() for e in data['images'])}
(snapshot/'snapshot.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
batch['source_snapshot']=snapshot.relative_to(root).as_posix()
args.batch.write_text(json.dumps(batch,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'snapshot':batch['source_snapshot'],'tex_to_compile':str(snapshot/'main.tex'),
                  'frozen_applied_drawings':metadata['applied_drawings'],'copied_files':len(hashes)},indent=2))
