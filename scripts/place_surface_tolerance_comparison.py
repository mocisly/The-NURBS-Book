"""Place ONE5.31-5.34 comparison beside the common surface tolerance explanation."""
import argparse,re,json
from pathlib import Path
import image_tex as pipeline
p=argparse.ArgumentParser(description=__doc__);p.add_argument('figure',type=int,choices=range(531,535));a=p.parse_args()
index=a.figure-531;printed='5.'+str(a.figure-500);number=43+index
data=pipeline.load();entry=next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_{number}.tex');assert entry['applied']
path=pipeline.ROOT/'chapter/5.tex';s=path.read_text(encoding='utf-8');ref=entry['replacement'];assert s.count(ref)==1
pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*'+re.escape(printed)+r'\.[^\n]*'
s,count=re.subn(pattern,'',s,count=1);assert count==1
if a.figure==531:
    old='196 基本几何算法 (b)两个曲面的等参数线。';assert s.count(old)==1;s=s.replace(old,'')
if a.figure==534:
    old='198 基本几何算法 (b)两个曲面的等参数线。(b)两个曲面的等参数线。';assert s.count(old)==1;s=s.replace(old,'')
proof=json.loads((pipeline.ROOT/f'image_tex/build/surface-tolerance-{a.figure}-check.json').read_text())
n,m=proof['new_control_count'];eps=('0.05','0.1','0.3','0.5')[index]
caption=(r'图 '+printed+r'. 在两个方向以容差$'+eps+r'$移除图5.30曲面的节点，视角与尺度保持一致。'
         '\\\\\n'+r'(a)原$9\times8$控制网（虚线）与$'+str(n)+r'\times'+str(m)+r'$近似控制网（实线）；(b)两曲面的对应等参数线。'
         '\\\\\n'+r'虚线与实线分别表示原始数据和近似结果；示意拟合的全域误差上界不超过所列容差。')
block=('\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+ref+
       '\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n')
anchor=r'\section{次数提升}';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
assert s.count(ref)==1;path.write_text(s,encoding='utf-8');print('Placed'+printed+' after previous tolerance comparison, before degree elevation.')
