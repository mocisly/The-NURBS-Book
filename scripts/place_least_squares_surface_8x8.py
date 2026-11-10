"""Move9.46AB from accuracy theory into the common-data fit comparison."""
import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n}.tex') for n in (54,55)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.46\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='也可以交换两个方向的拟合顺序';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{34cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+'\\hspace{1.3cm}'+entries[1]['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.46. 将控制网增加到$8\times8$的$(2,3)$次最小二乘拟合；数据、参数与图 9.45 完全相同。'+'\\\\\n'+
       r'(a) 拟合面与原始数据点；(b) 相同参数处三维误差的折线网格，误差高度仍放大四倍，视角和尺度均与图 9.45 相同。'+'\\\\\n'+
       r'均方根误差约$0.05993$，最大误差约$0.1684$；网格起伏明显减小，但逼近面仍可能在数据之间出现过冲。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Placed9.46AB directly after9.45,same dimensions/camera/fonts/error magnification;removed both misplaced scans and continuation caption.')
