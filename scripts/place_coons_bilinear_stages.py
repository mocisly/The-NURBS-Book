import re
import image_tex as p
d=p.load();f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');entries=[]
for n in (33,34,35):
    e=next(e for e in d['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex');assert e['applied'];entries.append(e)
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 10\.25\.[^\n]*'
    s,removed=re.subn(pat,'',s,count=1);assert removed==1,n
anchor='Coons 在 1960 年代中期';assert s.count(anchor)==1
captions=[r'图 10.25. 用图10.24的同一组边界构造双线性混合Coons补片。',r'(a) $R_1=(1-v)C_0(u)+vC_1(u)$；(b) $R_2=(1-u)C_0(v)+uC_1(v)$。',r'(c) 四角点的双线性插值$T$，仅通过角点，虚线为参考边界；(d) $S=R_1+R_2-T$精确通过全部四条边界。',r'粗实线为各阶段已插值的原边界，细线为真实曲面等参数线；四图同投影、同尺度、同字号。',r'双线性混合不要求最终曲面为双线性曲面；本例的$u$、$v$方向次数分别为3和2。']
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+'\\par\\vspace{.5cm}\n'+entries[1]['replacement']+'\\hspace{1cm}'+entries[2]['replacement']+'\n\\par\\smallskip\n'+'\\\\\n'.join(captions)+'\n\\end{minipage}\n\\end{center}\n\n'
s=s.replace(anchor,block+anchor,1);s=s.replace('498 高级表面构造技术','',1);f.write_text(s,encoding='utf-8');print('10.25all4panelsplacedtogetherafterconstructionbeforeCoonsHistory;derivative/twistproseunbroken.')
