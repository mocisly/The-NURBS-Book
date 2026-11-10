"""Place Fig3.19 after its tensor-product explanation and restore the five-step list."""
from pathlib import Path
import re,subprocess,sys

root=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(root/'scripts/place_chapter_figure.py'),
    '--tex','ch03/fig_3_20.tex','--figure','3.19','--before','计算固定 (u, v) 参数值','--width','18cm'],check=True,cwd=root)
p=root/'chapter/3.tex';text=p.read_text(encoding='utf-8')
# The paragraph starts with an inline U and includes the only split OCR V definition.
matches=[line for line in text.splitlines() if line.startswith(r'设 \(U\) 和') and '3.19' in line]
assert len(matches)==1
new=r'设 \(U\) 及三次基函数 \(N_{i,3}(u)\) 如图3.2a所示，二次基函数 \(N_{j,2}(v)\) 定义在 \(V=\{0,0,0,1/5,2/5,3/5,3/5,4/5,1,1,1\}\) 上。图3.19a、b分别显示张量积基函数 \(N_{4,3}(u)N_{4,2}(v)\) 和 \(N_{4,3}(u)N_{2,2}(v)\)。图3.20～3.25显示B样条曲面的示例。'
text=text.replace(matches[0],new,1)
caption=r'图 3.19. 三次 \(\times\) 二次张量积基函数：(a) \(N_{4,3}(u)N_{4,2}(v)\)；(b) \(N_{4,3}(u)N_{2,2}(v)\)。\\ \(U=\{0,0,0,0,1/4,1/2,3/4,1,1,1,1\}\)，\\ \(V=\{0,0,0,1/5,2/5,3/5,3/5,4/5,1,1,1\}\)。'
text,n=re.subn(r'(?m)^图 3\.19\..*$',lambda m:caption,text);assert n==1
p.write_text(text,encoding='utf-8')
print('Placed native3.19 after basis explanation, restored five-step list and clean U/V caption.')
