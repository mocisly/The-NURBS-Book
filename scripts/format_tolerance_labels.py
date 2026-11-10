"""Use leading zeros in the unplaced5.29 tolerance labels."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for n in (39,40,41):
    p=root/f'image_tex/ch05/fig_5_{n}.tex';s=p.read_text(encoding='utf-8')
    s=s.replace(r'\varepsilon=.',r'\varepsilon=0.');p.write_text(s,encoding='utf-8')
p=root/'scripts/create_tolerance_knot_removal.py';s=p.read_text(encoding='utf-8')
s=s.replace("('.007','.025','.07','.6','1.2')","('0.007','0.025','0.07','0.6','1.2')")
p.write_text(s,encoding='utf-8')
