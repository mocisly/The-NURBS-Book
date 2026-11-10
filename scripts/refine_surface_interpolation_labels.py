"""Move explicitly identified9.14labels off adjacent control/data edges."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
changes={14:{'Q_{1,1}':'left','Q_{2,0}':'below left','Q_{2,2}':'above right','R_{2,0}':'below left','R_{1,0}':'above right','R_{1,1}':'above right','R_{1,2}':'above right'},15:{'P_{0,1}':'left','P_{1,1}':'left','P_{2,1}':'left','P_{3,1}':'below right','P_{1,0}':'left'}}
for n,labels in changes.items():
    f=root/f'image_tex/ch09/fig_9_{n:02}.tex';s=f.read_text(encoding='utf-8')
    for name,anchor in labels.items():
        pat=r'(\\node\[)[^\]]+(\] at [^\n]*\{\$\\mathbf '+re.escape(name)+r'\$\};)'
        s,count=re.subn(pat,lambda m:m[1]+anchor+'=5pt'+m[2],s);assert count==1,(name,count)
    f.write_text(s,encoding='utf-8')
print('Refined twelve identified labels away from adjacent lines;no geometry changed.')
