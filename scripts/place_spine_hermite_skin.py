"""10.7after its interpolation explanation, before positioning examples."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_10.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.7\.[^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1;s=s.replace('466 高级表面构造技术','',1)
anchor='截面曲线的位置对表面形状有明确的影响';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{34cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.7. 用图 10.4～10.6 的同一组数据进行带脊导数约束的三次蒙皮。'+'\\\\\n'+
       r'(a) 实际$7\times10$控制网与给定截面；(b) 插值曲面的真实等参数网格，粗线标出五条给定截面。'+'\\\\\n'+
       r'$\bar v_k$按式(10.8)计算，$V$按式(9.23)设置；各控制列同时插值位置与式(10.10)、(10.11)的导数。'+'\\\\\n'+
       r'曲面对整条截面满足$S(u,\bar v_k)=C_k(u)$、$S_v(u,\bar v_k)\parallel D_k$；两面板共用视角、尺度和字号。'+'\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8');print('10.7moved from rational discussion to actual Hermite interpolation explanation;whole-section constraints explicitly captioned.')
