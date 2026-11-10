"""Group allfour9.14panels after tensor-interpolation construction,before algorithm."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex') for n in (14,15,16)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.14\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
orphan=r'\(u\) -方向插值；(d) 显示控制点的表面插值。';assert s.count(orphan)==1;s=s.replace(orphan,'',1)
anchor='总结来说，表面插值的过程如下:';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\smallskip\n\\begin{minipage}{18cm}\\centering\n'+entries[1]['replacement']+
       '\n\\end{minipage}\\hfill\n\\begin{minipage}{18cm}\\centering\n'+entries[2]['replacement']+
       '\n\\end{minipage}\n\\par\\smallskip\n'+
       r'图 9.14. 全局曲面插值的两个方向求解过程，采用同一组$4\times4$代表性数据，$p=q=3$、$\bar u_i=\bar v_i=i/3$。'+'\\\\\n'+
       r'(a) 数据网格$\mathbf Q_{k,\ell}$；(b) 对固定$\ell$沿$u$插值，得到控制点$\mathbf R_{i,\ell}$及四条插值曲线。'+'\\\\\n'+
       r'(c) 对固定$i$沿$v$插值$\mathbf R_{i,\ell}$，得到最终控制点$\mathbf P_{i,j}$；空心点标出内部的$\mathbf R_{i,\ell}$。'+'\\\\\n'+
       r'(d) 通过全部十六个数据点的双三次曲面及其控制网格；四幅图使用相同视角、尺度和字号。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);assert all(s.count(e['replacement'])==1 for e in entries);f.write_text(s,encoding='utf-8')
print('Grouped9.14a/b top,c/d bottom,with one complete caption before A9.4;removed orphaned continuation fragment.')
