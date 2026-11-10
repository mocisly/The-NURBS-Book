"""Calculate the actual10.7 Hermite skin without producing a picture."""
from pathlib import Path
import json
from spine_skinning_surfaces import construct
from spine_skinning_example_data import view
root=Path(__file__).resolve().parents[1];b,v,Q,r=construct(True)
(root/'image_tex/build/spine-hermite-skin-data.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
p=[view(p) for row in b[-1] for p in row]
print('PASS10.7:70 exact vector constraint identities;all5 complete sections and derivative fields;VP',list(map(float,v)),'projectedcontrolbounds',[(float(min(p[d] for p in p)),float(max(p[d] for p in p))) for d in range(2)])
