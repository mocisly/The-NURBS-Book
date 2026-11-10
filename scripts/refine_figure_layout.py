"""Apply the individual size-proof review corrections."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'tmp/figure-layout'
profiles=json.loads((B/'profiles.json').read_text(encoding='utf-8'))
manual=json.loads((B/'manual-profile-changes.json').read_text(encoding='utf-8'))
suggested={e['path']:e for e in json.loads((B/'suggested-profile-changes.json').read_text(encoding='utf-8'))}
tag_files=[];changed=[]
for e in profiles:
    p=ROOT/'image_tex'/e['path'];s=p.read_text(encoding='utf-8')
    panels=len(set(re.findall(r'\{\(([a-h])\)',s)))
    if panels>e['panels']and panels>=2:
        e.update(panels=panels,target_width_cm=min(17,6*panels),target_height_cm=6.5,kind='annotated multiple panels')
    if e['path']in suggested:
        fix=suggested[e['path']];e.update(target_width_cm=max(e['target_width_cm'],fix['target_width_cm']),target_height_cm=max(e['target_height_cm'],fix['target_height_cm']))
    if panels>=2 and s.count('yshift=')>s.count('xshift='):e['target_height_cm']=max(9.5,e['target_height_cm'])
    if e['path']in manual:e.update(manual[e['path']])
    if e['path']in ['ch13/fig_13_03.tex','ch13/fig_13_04.tex','ch13/fig_13_05.tex','ch13/fig_13_06.tex','ch13/fig_13_08.tex']:
        e['min_scale']={'03':.75,'04':.7,'05':.6,'06':.65,'08':.65}[p.stem[-2:]]
    s=s.replace('[use as bounding box]','[book figure bounds]')
    if e['path']not in ['ch06/fig_6_11.tex','ch06/fig_6_12.tex','ch06/fig_6_14.tex','ch06/fig_6_15.tex','ch12/fig_12_01.tex']:
        def tag(m):
            options=m[1]or'[]'
            if 'book panel tag'in options:return m[0]
            return r'\node'+options[:-1]+(','if options!='[]'else'')+'book panel tag]'+m[2]+'{'+m[3]+'};'
        updated=re.sub(r'\\node(\[[^\]\n]*\])?(\s+at\s+\([^\n)]*\)\s*)\{(\([a-h]\)(?:\s*\$n[^;\n]*)?)\};',tag,s)
        if updated!=s:tag_files.append(e['path'])
        s=updated
    if s!=p.read_text(encoding='utf-8'):p.write_text(s,encoding='utf-8');changed.append(e['path'])
(B/'profiles.json').write_text(json.dumps(profiles,ensure_ascii=False,indent=2),encoding='utf-8')
(B/'refinements.json').write_text(json.dumps(dict(tag_files=tag_files,changed_sources=changed,manual_profiles=manual),ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Applied {len(manual)} individually flagged size profiles; adjusted {len(tag_files)} panel-label files.')
