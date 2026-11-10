"""10.16exact Frenet reversal and actual collapsed middle skin cross section."""
from pathlib import Path
import json
from frenet_flip_data import construct,view
root=Path(__file__).resolve().parents[1];base,v,Q,r=construct();P=[view(p) for row in base[-1] for p in row]
(root/'image_tex/build/frenet-flip-data.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
print('PASS10.16:actual Frenet limits opposite/global norms exact;56whole-sectioncontrols;wholemidisocurvecollapsesexactly;bounds',[(float(min(p[d] for p in P)),float(max(p[d] for p in P))) for d in range(2)])
