"""Keep the z label above every control net in the unplaced5.20/5.21 previews."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for p in [root/'scripts/create_surface_bezier_decomposition.py']+[root/f'image_tex/ch05/fig_5_{n}.tex' for n in (24,25,26)]:
    text=p.read_text(encoding='utf-8')
    assert '(0,0,7.3)' in text
    text=text.replace('(0,0,7.3)','(0,0,8.3)').replace('(13.5,7.2)','(13.5,8.2)').replace('(6.5,7.2)','(6.5,8.2)')
    p.write_text(text,encoding='utf-8')
