"""Group9.54before the cubic subsection,not inside unrelated cubic formulae."""
import re,json
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n}.tex') for n in (64,65,66)];assert all(e['applied'] for e in entries)
r=json.loads((p.ROOT/'image_tex/build/local-conic-spiral-check.json').read_text())
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.54\.[^\n]*'
    s,n=re.subn(pat,'',s,count=1);assert n==1
anchor=r'\subsection{局部非有理三次曲线逼近}';assert s.count(anchor)==1
counts='、'.join(str(x['segments']) for x in r['panels']);errors='、'.join(f"{x['maximum_exact_checked_datum_distance']:.6f}" for x in r['panels'])
block=('\\begin{center}\n\\begin{minipage}{34cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+'\\par\\smallskip\n'+entries[1]['replacement']+'\\par\\smallskip\n'+entries[2]['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.54. 对数螺旋$r=\tfrac12 e^{\theta/5}$的局部有理二次逼近；统一取$\theta_j=3\pi j/50$，$j=0,\ldots,50$的五十一个数据点。'+'\\\\\n'+
       r'(a)—(d) 使用上文列出的容差与$K_{\max}$，实线为拟合圆锥，虚线为实际控制多边形，空心圆为同一组数据点；四图分别使用'+counts+r'个圆锥段。'+'\\\\\n'+
       r'按算法 A9.11 平均肩点参数，每段通过两个端点并共享端切向，所有连接精确满足$G^1$；所取曲线参数点的最大数据距离分别为'+errors+r'，均小于相应容差。'+'\\\\\n'+
       r'(e) 为 (b) 所得二次 NURBS 曲线在公共弦长节点参数$u=j/50$处的十字标记；五图保持同一坐标尺度、字号和线宽，(a)—(d) 统一边界。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Grouped9.54AB/CD/Ebeforecubicsubsection,explicitanalytic51samples/actual4-7-9-5conicfits/G1/errorproof/trueuniformNURBSparameters;removedunrelatedcubicinterruptions.')
