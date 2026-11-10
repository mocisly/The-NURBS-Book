"""Group9.21a/b after the C1/chord parameterization comparison."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex') for n in (25,26)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.21\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='现在我们去掉公式 (9.34) 中给出的限制';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{29cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\smallskip\n'+entries[1]['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.21. 图 9.20 的同一组二次曲线段在不同参数化下的均匀参数采样。'+'\\\\\n'+
       r'(a) 按公式 (9.37)、(9.39) 构造$C^1$参数，数据参数为$(0,2/11,4/11,7/11,9/11,1)$；(b) 弦长参数下的$G^1$曲线。'+'\\\\\n'+
       r'每幅图均在$u=j/40$处取值；三十九个内部样本以“$+$”标记，端点以数据点符号标记。几何曲线相同，采样点的间距随参数化改变。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Grouped9.21a/b before exceptional tangent cases;corrected C1formula references and documented actual uniform-u samples.')
