import argparse,re
import image_tex as p
a=argparse.ArgumentParser();a.add_argument('figure',type=int,choices=(11,12));arg=a.parse_args();fig=arg.figure;d=p.load();e=next(e for e in d['images'] if e['tex']==f'image_tex/ch11/fig_11_{fig+2:02}.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.'+str(fig)+r'[.。][^\n]*'
s,n=re.subn(pat,'',s,count=1);assert n==1
u,w=('t_4=\\bar u=0.52','2.45') if fig==11 else ('\\bar u=0.46','0.97')
caption=rf'图 11.{fig}. 仅改变$w_4=0.2$，在${u}$处将点$P$朝$P_4$拉动$d=0.075$。'+'\\\\\n'+rf'式(11.25)给出$\widehat w_4={w}$；实线为原曲线，虚线为修改曲线，细线连接同参数点。'+'\\\\\n'+r'图11.11、11.12共用一组代表性控制点；两组指定权重和距离均严格满足，数据见源码。'
block='\\begin{center}\n\\begin{minipage}{26cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n'
anchor=r'\begin{itemize}'+'\n'+r'\item 与控制点重新定位的情况一样'
assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
if fig==11:
    old='则根据公式 (11.25)，可以得出';start=s.index(old);end=s.index('；',start)
    s=s[:start]+r'由式(11.25)有$d(u)=|\Delta w_k|R_{k,p}(u)|P_k-C(u)|/|w_k+\Delta w_k R_{k,p}(u)|$。因此位移峰值还取决于曲线点到控制点的距离；一般不能仅由$R_{k,p}$的峰值决定（图11.11）'+s[end:]
f.write_text(s,encoding='utf-8');print('Placed',fig,'after weight modification notes, before node insertion.')
