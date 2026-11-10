"""Combine9.52a-e with one complete caption adjacent to tensor approximation."""
import re,json
import image_tex as p
d=p.load();entries=[next(e for e in d['images'] if e['tex']==f'image_tex/ch09/fig_9_{n}.tex') for n in (60,61,62)];assert all(e['applied'] for e in entries)
r=json.loads((p.ROOT/'image_tex/build/bounded-surface-comparison-check.json').read_text())
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
for e in entries:
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.52\.[^\n]*'
    s,n=re.subn(pat,'',s,count=1);assert n==1
s=s.replace('436 曲线和表面拟合','',1)
anchor='算法 A9.10 和相应的表面算法实际上是数据简化算法';assert s.count(anchor)==1
shapes='；'.join('('+x['letter']+') $'+str(x['control_shape'][0])+r'\times'+str(x['control_shape'][1])+'$' for x in r['panels'])
errors='，'.join('('+x['letter']+') $'+f"{x['maximum_actual_Euclidean_error']:.4f}"+'$' for x in r['panels'][1:])
block=('\\begin{center}\n\\begin{minipage}{34cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+entries[0]['replacement']+'\\par\\smallskip\n'+entries[1]['replacement']+'\\par\\smallskip\n'+entries[2]['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.52. 同一组$13\times13$代表性数据的插值与误差受控逼近；所有子图统一视角、坐标尺度、线宽和字号。'+'\\\\\n'+
       r'(a) 数据点$Q_{ij}=(X_i,Y_j,z(X_i,Y_j))$，$X_i=Y_i=-2+i/3$，$i,j=0,\ldots,12$，其中'+'\\\\\n'+
       r'$z(x,y)=3(2-x)^4/[(2-x)^4+(2+x)^4]+(1-x^2/4)^2(1-y^2/4)/10$。'+'\\\\\n'+
       r'(b) $(2,2)$次零误差插值；(c)、(d) 同次曲面的$E=1/2,1$逼近；(e) $(3,3)$次、$E=1$逼近。控制网分别为'+shapes+'。'+'\\\\\n'+
       r'从二次插值面开始，按 A9.10 的曲面扩展流程受控移除、重新拟合并在 (e) 中升次；移除采用逐点累计$L^1$保守误差界。'+'\\\\\n'+
       r'公共弦长参数处的最大欧氏误差为'+errors+r'，均不超过相应容差；(b) 的全部一百六十九个插值误差精确为零。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Grouped9.52AB/CD/Ewithonecompletecaption,samedata/camera/font;explicitdataformula/controlcounts/actualerrors/conservativevariant;removedduplicatecontinuations/OCR436.')
