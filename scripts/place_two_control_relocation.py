import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_06.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.6\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
old=r'\(\gamma  = {0.47}\) (由公式 [11.8] 计算的默认值)';new=r'\(\gamma=8/17\simeq0.47\)（由公式[11.8]计算的默认值）';assert s.count(old)==1;s=s.replace(old,new,1)
anchor='使用这些工具，可以轻松实现';assert s.count(anchor)==1
captions=[r'图 11.6. 同时移动$P_3$和$P_4$，两例均采用图11.3的曲线及$\bar u=0.43$。',r'(a) 按式(11.8)取默认$\gamma=8/17\simeq0.47$；(b) 取$\gamma=4/5$，使$P_4$承担更大比例的移动。',r'两例均按式(11.9)求$\alpha$，使同一选定点沿单位方向$(7/25,-24/25)$精确移动$6/5$。',r'粗箭头为控制点移动，细线为同参数点的实际位移；实线和虚线分别为原曲线和修改曲线。',r'两图与此前例子使用相同尺度和字号，修改支撑域扩大为$[0,.9)$；控制数据记录于源码。']
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+'\\\\\n'.join(captions)+'\n\\end{minipage}\n\\end{center}\n\n'
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.6placedafteritsgammaexplanationbeforeincrementalrelocation;exactdefaultgammaqualified.')
