"""Three same-scale views of5.24; reconnect the narrowly interrupted A5.7 if branch."""
import re
import image_tex as pipeline
data=pipeline.load();entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in (30,31)]
assert all(e['applied'] for e in entries)
path=pipeline.ROOT/'chapter/5.tex';text=path.read_text(encoding='utf-8')
for e in entries:
    ref=e['replacement'];assert text.count(ref)==1
    pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.24\.[^\n]*'
    text,count=re.subn(pattern,'',text,count=1);assert count==1
anchor=r'\hspace*{2em} if (dir == U\_DIRECTION)';start=text.index(anchor)+len(anchor)
end=text.index(r'\{',start);old=text[start:end]
assert re.sub(r'\s|\\HRule','',old)=='178基本几何算法'
text=text[:start]+'\n\n'+text[end:]
caption=(r'图 5.24. 四次曲线的即时Bézier分解，三个视图使用同一曲线与坐标尺度。(a)第一段；(b)第二段；(c)第三段。'
         '\\\\\n'+r'实心点表示当前段的五个Bézier控制点，空心点保留原控制多边形。采用代表性七点控制网和节点向量$\{0,0,0,0,0,1/3,2/3,1,1,1,1,1\}$。')
panels=('\\begin{minipage}[b]{12.2cm}\n'+entries[0]['replacement']+'\n\\end{minipage}\\hfill\n'
        '\\begin{minipage}[b]{25.2cm}\n'+entries[1]['replacement']+'\n\\end{minipage}')
block=('\\begin{center}\n\\begin{minipage}{38cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+panels+
       '\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n')
anchor='算法 A5.7 显示了表面分解的组织';assert text.count(anchor)==1;text=text.replace(anchor,block+anchor,1)
for e in entries:assert text.count(e['replacement'])==1
path.write_text(text,encoding='utf-8');print('Placed three5.24 views horizontally at native scale; restored A5.7 if brace continuity.')
