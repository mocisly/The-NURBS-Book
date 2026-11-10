"""Separate final two9.14c labels from short projected edges."""
from pathlib import Path
import re
from global_surface_interpolation_data import P,camera
from native_bspline import point
f=Path(__file__).resolve().parents[1]/'image_tex/ch09/fig_9_15.tex';s=f.read_text(encoding='utf-8')
s,n=re.subn(r'(\\node\[)left=5pt(\] at [^\n]*\{\$\\mathbf P_\{1,0\}\$\};)',lambda m:m[1]+'below left=5pt'+m[2],s);assert n==1
s,n=re.subn(r'\\node\[[^\]]+\] at [^\n]*\{\$\\mathbf P_\{2,1\}\$\};',lambda m:r'\node[anchor=west] (p21) at (0,-2.8) {$\mathbf P_{2,1}$};'+'\n'+r'\draw[book grid] '+point(camera(P[2][1]))+'--(p21.west);',s);assert n==1
f.write_text(s,encoding='utf-8');print('Final P1,0/P2,1 clearance adjustments applied.')
