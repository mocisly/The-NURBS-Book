"""Place the three exceptional quadratic constructions together after Eq9.44."""
import re
import image_tex as p

d=p.load()
entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n:02}.tex') for n in (27,28)]
assert all(e['applied'] for e in entries)
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.22\.[^\n]*'
    s,n=re.subn(pattern,'',s,count=1);assert n==1
s,n=re.subn('定义了一个圆锥弧\\s+由','定义了一个圆锥弧，由',s,count=1);assert n==1
anchor='图 9.23-9.25 显示了几个示例。';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+
       '\n\\par\\smallskip\n'+entries[1]['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.22. 公式 (9.41)—(9.44) 的三个代表性分段二次构造，采用统一的坐标尺度。'+'\\\\\n'+
       r'(a) 平行且反向的端切向，按半弦长取$\gamma_k=\gamma_{k+1}=3$；(b) 原切线交点不满足条件 (9.34)，取$\alpha=2/3$，得$\gamma_k=195/103$、$\gamma_{k+1}=195/89$。'+'\\\\\n'+
       r'(c) 等腰控制三角形，$\cos\theta=3/5$、$\gamma=5/2$；新控制点和连接点恰为原抛物线在中点细分的结果。'+'\\\\\n'+
       r'两段曲线分别由$(\mathbf Q_{k-1},\mathbf R_k^{\prime},\mathbf Q_k^{\prime})$与$(\mathbf Q_k^{\prime},\mathbf R_{k+1}^{\prime},\mathbf Q_k)$定义；箭头段表示真实单位切向，前接细线为延长引导线。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Grouped9.22a/b/c after complete Eq9.44;rejoined interrupted formulas and local rational introduction.')
