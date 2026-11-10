"""10.8immediately after10.7, restoring interrupted rational interpolation prose."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_11.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.8\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='截面曲线的位置对表面形状有明确的影响';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{34cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.8. 对图 10.7 的相同截面和相同$\bar v_k$进行不带导数约束的三次蒙皮。'+'\\\\\n'+
       r'(a) 实际$7\times5$控制网与给定截面；(b) 曲面的真实等参数网格，粗线为五条给定截面。'+'\\\\\n'+
       r'节点$V$由参数平均法确定；仍精确插值整条截面，截面上的$v$向导数则通常不再平行于脊切向量。'+'\\\\\n'+
       r'与图 10.7 共用投影、坐标尺度及字号，以便直接比较两种构造的形状变化。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1)
s=s.replace('在 468 高级表面构造技术部分的曲线中，没有明显的方法可以施加','截面曲线，但没有明显的方法可以施加',1)
s=re.sub(r'尽管设计师仍然可以使用脊曲线来定位和定向\s*截面曲线，但','尽管设计师仍然可以使用脊曲线来定位和定向截面曲线，但',s,count=1)
f.write_text(s,encoding='utf-8');print('10.8grouped after10.7/beforepositionexamples;restored rational-section sentence interrupted by old scans/OCR468.')
