import re
import image_tex as p
d=p.load();f=p.ROOT/'chapter/12.tex';s=f.read_text(encoding='utf-8');es=[]
for n in(5,6,7):
    e=next(e for e in d['images']if e['tex']==f'image_tex/ch12/fig_12_{n:02d}.tex');assert e['applied'];es.append(e)
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 12\.4[.。][^\n]*';s,c=re.subn(pat,'',s,count=1);assert c==1
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+es[0]['replacement']+'\n\\par\\medskip\n'+es[1]['replacement']+'\n\\par\\medskip\n'+es[2]['replacement']+'\n\\par\\smallskip\n'
caption=r'图 12.4. 按算法A12.1对四次曲线左端解夹的三步回代。'+'\\\\\n'+r'(a) 原始控制点；(b) $i=0$后得到$P_0^0$；(c) $i=1$后得到$P_0^1,P_1^1$；(d) $i=2$后得到$P_0^2,P_1^2,P_2^2$。'+'\\\\\n'+r'采用代表性八点曲线，原节点为$\{0,0,0,0,0,1/4,1/2,3/4,1,1,1,1,1\}$；四幅图的实线均为原区间$[0,1]$上的同一条曲线。'+'\\\\\n'+r'虚线展示算法的原始、中间和最终控制点工作数组；中间数组尚非完整的解夹表示。全部六次回代恒等式及最终曲线的全部多项式系数均已精确核验。'+'\\\\\n'+r'各图使用相同坐标尺度、字号和线宽；四次曲线的原生B\'{e}zier显示误差上界为$10^{-5}$厘米。'
block+=caption+'\n\\end{minipage}\n\\end{center}\n';needle='图 12.4a-12.4d 显示了';start=s.index(needle);end=s.index('\n',start);s=s[:end]+'\n\n'+block+s[end:];f.write_text(s,encoding='utf-8');print('Placed complete A/BC/D quartic algorithm group next to explanation; restored later prose.')
