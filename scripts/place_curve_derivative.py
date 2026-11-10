"""Place reviewed Fig3.15 next to Ex3.1 and reconcile its derivative coefficients."""
from pathlib import Path
import re,subprocess,sys

root=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(root/'scripts/place_chapter_figure.py'),
    '--tex','ch03/fig_3_15.tex','--figure','3.15','--before','Ex3.2 设','--width','18cm'],check=True,cwd=root)
p=root/'chapter/3.tex';text=p.read_text(encoding='utf-8')
a,b=text.index('Ex3.1 设'),text.index('Ex3.2 设');part=text[a:b]
denoms=(r'\frac25-0',r'\frac35-0',r'1-\frac25',r'1-\frac35')
multipliers=('5',r'\frac{10}{3}',r'\frac{10}{3}','5')
lines=part.splitlines()
for i,(denom,multiplier) in enumerate(zip(denoms,multipliers)):
    matches=[j for j,line in enumerate(lines) if line.startswith(r'{\mathbf{Q}}_{'+str(i)+'}')]
    assert len(matches)==1
    difference=r'\left(\mathbf P_{'+str(i+1)+r'}-\mathbf P_{'+str(i)+r'}\right)'
    lines[matches[0]]=r'\mathbf Q_{'+str(i)+r'}=\frac{2'+difference+'}{'+denom+'}='+multiplier+difference
part='\n'.join(lines)+'\n\n'
text=text[:a]+part+text[b:]
caption=r"图 3.15. (a) \(U=\{0,0,0,2/5,3/5,1,1,1\}\) 上的二次曲线；切向量按 \(1/2\) 缩放显示。\\ (b) \(U'=\{0,0,2/5,3/5,1,1\}\) 上的一次导数曲线，控制点由式(3.4)计算。"
text,n=re.subn(r'(?m)^图 3\.15\..*$',lambda m:caption,text);assert n==1
assert text.count('96 B-spline 曲线和曲面')==1
text=text.replace('96 B-spline 曲线和曲面','',1)
p.write_text(text,encoding='utf-8')
print('Placed Fig3.15 with Ex3.1; Eq3.4 multipliers reconciled to5,10/3,10/3,5; tangent display scale stated.')
