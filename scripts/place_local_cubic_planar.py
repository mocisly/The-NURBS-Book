"""Place9.57afterinputsettingsand statevalidityconditionoferror shortcut."""
import re,json
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_69.tex');assert e['applied']
r=json.loads((p.ROOT/'image_tex/build/local-cubic-planar-check.json').read_text())
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.57\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
old='图 [latex0] 的输入数据为';assert s.count(old)==1;s=s.replace(old,'',1)
anchor='注意从图 9.57a 到图 9.57b';assert s.count(anchor)==1
counts='、'.join(str(p['segments']) for p in r['panels']);errors='、'.join(f"{p['maximum_exact_checked_datum_distance']:.5f}" for p in r['panels'])
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.57. 同一组五十一个代表性平面数据点的局部三次逼近，三个子图保持相同坐标尺度、边界和字号。'+'\\\\\n'+
       r'按算法 A9.12 的点与切向最小二乘方程计算、平均控制柄，并逐点检查实际距离；(a)—(c) 分别使用'+counts+r'个曲线段。'+'\\\\\n'+
       r'虚线为拼接后双内部节点 B 样条的实际控制多边形，空心圆为数据点；通过节点参数调整，各连接处精确满足$C^1$。'+'\\\\\n'+
       r'最大数据距离分别为'+errors+r'，均低于各自容差；数据由源码记录的四段多项式曲线采样，采用其已知切向，未从扫描图提取坐标。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
old=r'回想一下 \({\mathbf{Q}}_{k} = {\mathbf{C}}_{k}\left( {\widehat{u}}_{k}\right)\) 。';assert s.count(old)==1
s=s.replace(old,r'若逐点构造精确满足\({\mathbf{Q}}_k={\mathbf C}_k(\widehat u_k)\)，则有如下误差关系。',1)
old='方程 (9.110) 可以用作快速接受测试:如果它小于或等于 \\(E\\) ，则不需要牛顿迭代。'
assert s.count(old)==1
s=s.replace(old,r'当逐点构造精确插值数据点时，方程 (9.110) 可用作快速接受测试：若其小于或等于\(E\)，则不需要牛顿迭代。若平面最小二乘系统存在非零的点约束残差，则必须将该残差计入误差界，或直接检查实际距离。',1)
f.write_text(s,encoding='utf-8');print('Placed9.57aftersettings,explicitrepresentative51data/globalC1controlpolygons/actualerrors;clarified9.110shortcutrequireszeroindividualpointresidual,removedlatex0OCRplaceholder.')
