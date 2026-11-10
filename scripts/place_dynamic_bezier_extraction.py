"""Restore A5.6 continuity and place its four construction views by the explanation."""
import re
import image_tex as pipeline
data=pipeline.load();entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in (27,28)]
assert all(e['applied'] for e in entries)
path=pipeline.ROOT/'chapter/5.tex';text=path.read_text(encoding='utf-8')
for e in entries:
    ref=e['replacement'];assert text.count(ref)==1
    pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.22\.[^\n]*'
    text,count=re.subn(pattern,'',text,count=1);assert count==1
# Remove only the now-empty old OCR page breaks that split A5.6.
start=text.index('\\HRule',text.index('DecomposeCurve(n, p, U, Pw, nb, Qw)'))
end=text.index('\\hspace*{1em} /* Input: n, p, U, Pw */',start)
old=text[start:end]
assert re.sub(r'\s|\\HRule','',old)=='174基本几何算法插入的节点；(c)插入第二个节点；(d)为第二个段做准备。'
text=text[:start]+text[end:]
anchor='for (i=0; i<=p; i++) Qw[nb][i] = Pw[i];';start=text.index(anchor)+len(anchor)
end=text.index('while (b < m)',start);old=text[start:end]
assert re.sub(r'\s|\\HRule','',old)==''
text=text[:start]+'\n\n'+text[end:]
old=(r'为第 \(k\) 个贝塞尔段的第 \(j\) 个控制点， \(k = 0,\ldots ,p\) 和 \(j = 0,1,2\)')
new=(r'为第 \(j\) 个贝塞尔段的第 \(k\) 个控制点， \(k = 0,\ldots ,p\) 和 \(j = 0,1,2\)')
assert text.count(old)==1;text=text.replace(old,new)
assert text.count('结插入α的计算')==1;text=text.replace('结插入α的计算',r'结插入\(\alpha\)的计算')
caption=(r'图 5.22. 三次曲线的动态Bézier分解，四图使用同一曲线与坐标尺度。'
         '\\\\\n'+r'(a)复制原控制点到工作数组；(b)在首个内部节点插入一次；(c)再插入一次，得到首段四个Bézier控制点；(d)准备下一段的工作数组。'
         '\\\\\n'+r'示意节点向量为$\{0,0,0,0,1/3,2/3,1,1,1,1\}$。$\mathbf Q_k^j$的上标$j$表示段号、下标$k$表示局部控制点；工作数组中的中间量尚未全部完成提取。')
block=('\\begin{center}\n\\begin{minipage}{28cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+
       entries[0]['replacement']+'\n\\par\\medskip\n'+entries[1]['replacement']+
       '\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n')
anchor='与使用一般结精细化相比';assert text.count(anchor)==1;text=text.replace(anchor,block+anchor,1)
for e in entries:assert text.count(e['replacement'])==1
path.write_text(text,encoding='utf-8')
print('Placed four5.22 views together; restored A5.6 continuity, corrected transposed Q indices and local math alpha.')
