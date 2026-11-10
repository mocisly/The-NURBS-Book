"""Group six5.29 views and reconnect the interrupted degree-elevation explanation."""
import re
import image_tex as pipeline
data=pipeline.load();entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in (39,40,41)]
assert all(e['applied'] for e in entries)
path=pipeline.ROOT/'chapter/5.tex';s=path.read_text(encoding='utf-8')
for e in entries:
    ref=e['replacement'];assert s.count(ref)==1
    pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.29\.[^\n]*'
    s,count=re.subn(pattern,'',s,count=1);assert count==1
# Remove the duplicated, incorrect OCR lead-in separated by the old final image.
start=s.index('由于提升度数的曲线');end=s.index('这导致',start)+len('这导致')
assert r'\({m}_{1},\ldots ,{m}_{s}\)' in s[start:end]
s=s[:start]+s[end:]
old=r'相同的连续性，因此可以得出相同的节点必须对 \({\mathbf{C}}_{p + 1}\left( u\right)\) 具有重数 \({m}_{i} + 1\) 。这导致'
assert s.count(old)==1
s=s.replace(old,r'为保持相同的连续性，同一节点在\(p+1\)次曲线中的重数必须增加为\(m_i+1\)。这导致')
caption=(r'图 5.29. 同一三次曲线在不同容差下的节点移除，采用代表性十一点控制网与局部逆插入拟合。'
         '\\\\\n'+r'原始$U=\{0,0,0,0,0.16,0.31,0.45,0.5501,0.702,0.8,0.901,1,1,1,1\}$。'
         '\\\\\n'+r'(a)原曲线；(b)～(f)的容差依次为$0.007$、$0.025$、$0.07$、$0.6$、$1.2$，各次均从同一原曲线计算。'
         '\\\\\n'+r'虚线表示原曲线与控制多边形，实线表示近似结果；圆圈标出实际移除的节点，各组全区间误差上界均不超过所列容差。')
drawings='\n\\par\\medskip\n'.join(e['replacement'] for e in entries)
block=('\\begin{center}\n\\begin{minipage}{31.4cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+drawings+
       '\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n')
anchor='图5.30a和5.30b至图5.34a和5.34b展示了类似的示例。';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
for e in entries:assert s.count(e['replacement'])==1
path.write_text(s,encoding='utf-8');print('Grouped six5.29 views in three same-scale rows beside tolerance explanation; repaired duplicated degree-elevation continuity lead-in.')
