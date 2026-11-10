"""Place9.50beside bounded-curve discussion,not inside surface definition."""
import re,json
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_58.tex');assert e['applied']
r=json.loads((p.ROOT/'image_tex/build/bounded-wavy-curve-check.json').read_text())
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.50\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='在算法 A9.10 的节点移除步骤中';assert s.count(anchor)==1
err=r['actual_maximum_Euclidean_same_parameter_error'];n=len(r['data']);count=len(r['controls'])
block=('\\begin{center}\n\\begin{minipage}{25cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.50. '+str(n)+r'个代表性数据点在容差$E=7/100$内的三次逼近，共'+str(count)+r'个控制点。'+'\\\\\n'+
       r'(a) 空心数据点与拟合曲线；(b) 同一曲线的控制多边形，十字对应$u=j/40$，下方标尺标出实际节点及其重数。'+'\\\\\n'+
       r'采用算法 A9.10 的逐次升次、受控移除和重新拟合流程；移除时使用逐点累计的$L^1$误差界，作为欧氏误差的保守上界。'+'\\\\\n'+
       r'本例数据点到所取曲线参数点的最大欧氏误差约$'+f'{err:.5f}'+r'<E$；所有曲线段、控制点与参数标记均由计算结果绘制。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
f.write_text(s,encoding='utf-8');print('Placed9.50ABbesideA9.10curveexamples;removedsurface-definition interruption,documented representative data andconservativeboundvariant.')
