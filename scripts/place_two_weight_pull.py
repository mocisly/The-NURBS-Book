import argparse,re
import image_tex as p
a=argparse.ArgumentParser();a.add_argument('figure',type=int,choices=(15,16));fig=a.parse_args().figure;d=p.load();e=next(e for e in d['images'] if e['tex']==f'image_tex/ch11/fig_11_{fig+2:02}.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.'+str(fig)+r'。[^\n]*';s,n=re.subn(pat,'',s,count=1);assert n==1
anchor='同时权重修改的用户界面可能如下所示。';assert s.count(anchor)==1
caption=(r'图 11.15. 在$\bar u=(t_4+t_5)/2=0.608$处沿$RQ$拉动$d=0.088$。'+'\\\\\n'+r'$w_4=w_5=0.05$同时改为$\widehat w_4=\widehat w_5=1.23$；权重比保持不变。' if fig==15 else r'图 11.16. 在$\bar u=0.612$处沿不同于$RQ$的方向拉动$d=0.088$。'+'\\\\\n'+r'$w_4=w_5=0.05$改为$\widehat w_4=1.89$、$\widehat w_5=0.48$；权重比发生变化。')
caption+='\\\\\n'+r'两图共用一组代数构造的代表性控制点；参数、指定权重和拉动距离均严格满足，数值记录于源码。'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n';s=s.replace(anchor,block+anchor,1)
if fig==15:s=s.replace('图 11.15 中曲线变化是令人愉悦且对称的，而在图 11.16 中则不是。','图11.15采用保持权重比的协调拉动，而图11.16改变权重比，产生向一侧偏移的效果。')
f.write_text(s,encoding='utf-8');print('Placed',fig,'after ratio discussion, before complete interface paragraph.')
