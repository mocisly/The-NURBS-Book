import re
import image_tex as p
d=p.load();entries=[next(e for e in d['images']if e['tex']==f'image_tex/ch11/fig_11_{n}.tex')for n in(29,30)];assert all(e['applied']for e in entries);f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*11\.24\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor=r'\subsection{扁平化}';assert s.count(anchor)==1
caption=r'图 11.24. 曲面折线变形：五条明确的字母中心折线驱动同一组控制点。'+'\\\\\n'+r'(a) 直接定义的NURBS折线笔画；(b) 到任一线段的精确距离不超过$r=1/100$的控制点（+）及包围框。'+'\\\\\n'+r'(c) 在代表性平面细化得到的$67\times67$控制网上，对选中控制点沿$W=(0,0,1)$移动$d=3/5$后的实际曲面。'+'\\\\\n'+r'最近线段投影、端点截断和4489个候选点的距离逐一核验；四条外边界保持不变，过渡范围由基函数支撑决定。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+entries[0]['replacement']+'\n\\par\\medskip\n'+entries[1]['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.24 AB/C coherent group before flattening; restored flattening instruction list from intervening scans.')
