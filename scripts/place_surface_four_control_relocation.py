import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch11/fig_11_11.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.9\.[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='类似于曲线情况，节点插入可以用来限制';assert s.count(anchor)==1
captions=[r'图 11.9. 对图11.8的同一曲面，按式(11.13)—(11.14)同时移动四个相邻控制点。',r'(a) $P_{4,3},P_{5,3},P_{4,4},P_{5,4}$的实际移动及新邻接边；按节点平均值取$\delta=24/55$、$\gamma=1/2$。',r'(b) 在$\bar u=\bar v=3/5$处的选定点精确向上移动$3/5$，虚线与箭头表示真实局部曲面及位移。',r'修改范围扩大为$[.2,1)\times[.2,1)$，全部四条边界曲线仍保持不变；网格来自同一组原曲面数据。',r'两图与图11.8共用投影、尺度、字号和线宽；控制点、混合系数和核验数据记录于源码。']
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+'\\\\\n'.join(captions)+'\n\\end{minipage}\n\\end{center}\n\n'
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('11.9placedbeside11.8afterfour-controlformula,beforelocal-insertiondiscussion;removedscanfromweightsection.')
