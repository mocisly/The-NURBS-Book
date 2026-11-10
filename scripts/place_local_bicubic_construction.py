"""Group all four9.32construction stages after A9.5 and its explanation."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex') for n in (38,39)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.32\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
assert s.count('402 曲线和表面拟合 ')==1;s=s.replace('402 曲线和表面拟合 ','',1)
s,n=re.subn('并考虑插值这些点的三次曲线\\s+','并考虑插值这些点的三次曲线 ',s,count=1);assert n==1
old='图 9.32 显示了表面构造过程。在图 9.32a 中，数据点用小立方体标记。'
new='图 9.32 显示了表面构造过程。在图 9.32a 中，数据点用空心方框标记。'
assert s.count(old)==1;s=s.replace(old,new,1)
anchor='该插值方案可以轻松生成闭合的';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\smallskip\n'+entries[1]['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.32. 公式 (9.55)—(9.59) 的局部双三次曲面构造，沿用图 9.15—9.17 的同一组十六个代表性数据点。'+'\\\\\n'+
       r'(a) $4\times4$数据网格；(b) 九个双三次 Bézier 片的$10\times10$复合控制网；(c) 两方向各移除两个节点，得到$8\times8$的 B 样条控制网；(d) 实际曲面的四十一条等参数曲线。'+'\\\\\n'+
       r'空心方框为输入数据，小实心点为控制点；四图采用相同视角、尺度与字体。全部数据均被精确插值，节点移除不改变任何 Bézier 片，片间沿整条边满足$C^1$连接。'+'\\\\\n'+
       r'公共参数按算法 A9.5 累加各行、列弦长得到；边界混合导数采用公式 (9.32) 的单侧估计。(d) 的曲线族包含四条数据参数线。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Grouped9.32a/b/c/d after A9.5;rejoined interrupted curve paragraph and removed OCR402header.')
