from pathlib import Path
import json
from gordon_network_data import construct,UC
from knot59_data import insert_surface
from surface_refinement import verify_directional_identity
root=Path(__file__).resolve().parents[1];nets=construct();reports=[]
for index,name in enumerate(('L1','L2','T')):
    before=nets[name];current=before;checks=[]
    for axis,target in [('u',UC),('v',nets['S'][1])]:
        start=current;old=current[0 if axis=='u' else 1]
        for t in sorted(set(target)):
            for _ in range(target.count(t)-old.count(t)):current=insert_surface(*current,axis,t)
        checks.append(dict(axis=axis,**verify_directional_identity(start,current,axis)))
    assert current==nets['refined'][index];reports.append(dict(name=name,identities=checks))
(root/'image_tex/build/gordon-refinement-check.json').write_text(json.dumps(dict(exact_refinement=True,stages=reports),indent=2)+'\n',encoding='utf-8')
print('PASS exact Gordon refinement:',sum(c['identical_directional_polynomial_spans'] for r in reports for c in r['identities']),'whole polynomial span identities.')
