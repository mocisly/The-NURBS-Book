"""9.46: only control counts change,81data and parameters identical to9.45."""
from pathlib import Path
import json
from surface_least_squares_data import fit
from surface_comparison_native import draw
from surface_geometry import verify_tensor
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
for n in (54,55):assert not next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n}.tex')['applied']
base,squares,report=fit(8,8)
previous=json.loads((root/'image_tex/build/least-squares-surface-5x6-check.json').read_text())
assert report['sum_squared_error']<previous['sum_squared_error']
assert report['maximum_same_parameter_3D_error']<previous['maximum_same_parameter_3D_error']
checks=[]
for n,letter,errors in [(54,'a',None),(55,'b',squares)]:
    tex,proof=draw(base,letter,errors);checks.append(proof)
    (root/f'image_tex/ch09/fig_9_{n}.tex').write_text('% Actual A9.7tensor8x8fit;common81data/camera/error4x as9.45.\n'+tex,encoding='utf-8')
report.update(figure='9.46',same_data_parameters_camera_as='9.45',only_control_counts_changed=True,native_panels=checks,tensor_checks=verify_tensor(*base,steps=3),error_mesh='9x9polyline of Euclidean same-parameter residuals',error_vertical_magnification=4)
(root/'image_tex/build/least-squares-surface-8x8-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print('PASS9.46:8x8exact two-direction LS;common81data/params;all four corners and order commute exactly;RMS/max',report['RMS_same_parameter_3D_error'],report['maximum_same_parameter_3D_error'])
