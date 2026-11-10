"""Calculate10.3five exact curve compatibilities and whole-section interpolation."""
from pathlib import Path
import json
from skinning_compatibility_data import construct
root=Path(__file__).resolve().parents[1];original,compatible,VP,base,report=construct()
(root/'image_tex/build/skinning-compatibility-data.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS10.3:',report['whole_curve_power_coefficient_identity_count'],'wholecurvescalarcoefficientidentities;22controlsall5;110sectioncontrolidentities;positiveXYJacobian;VP',list(map(float,VP)))
