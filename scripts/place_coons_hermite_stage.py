import argparse,re
import image_tex as p
parser=argparse.ArgumentParser();parser.add_argument('number',type=int,choices=(27,28,29,30));args=parser.parse_args();n=args.number;source=n+10
d=p.load();e=next(e for e in d['images'] if e['tex']==f'image_tex/ch10/fig_10_{source:02}.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 10\.'+str(n)+r'\.[^\n]*';s,nremoved=re.subn(pat,'',s,count=1);assert nremoved==1
texts={27:[r'图 10.27. 按式(10.41)构造的$u$向三次混合曲面$S_2(u,v)$。',r'(a) $4\times5$实际控制网；(b) 曲面在$u$方向为三次Bezier、在$v$方向为二次B样条。',r'粗线为精确插值的两条$C_\ell(v)$；对应$u$偏导数整条满足给定$D_\ell(v)$，虚线为另一组参考边界。'],
28:[r'图 10.28. 按式(10.40)构造的$v$向三次混合曲面$S_1(u,v)$。',r'(a) $6\times4$实际控制网；(b) 曲面在$u$方向为三次B样条、在$v$方向为三次Bezier。',r'粗线为精确插值的两条$C_k(u)$；对应$v$偏导数整条满足给定$D_k(u)$，虚线为另一组参考边界。'],
29:[r'图 10.29. 由角点、端点偏导数与扭矢量构成的双三次张量积曲面$T(u,v)$。',r'(a) $4\times4$Bezier控制网；(b) 角点Hermite插值曲面，虚线为四条原参考边界。',r'四角处的位置、两个一阶偏导数及混合偏导数分别与给定数据完全一致。'],
30:[r'图 10.30. 双三次混合Coons补片$S=S_1+S_2-T$。',r'(a) 统一次数、节点后相加减得到的$6\times8$控制网；(b) 最终曲面精确满足四条边界及四个跨边界导数场。',r'采用公共三次基$U=\{0,0,0,0,.3,.7,1,1,1,1\}$、$V=\{0,0,0,0,.4,.4,.6,.6,1,1,1,1\}$。']}
captions=texts[n]+[r'各图使用图10.24～10.26的同一组兼容数据；投影、尺度、字号与线宽保持一致，控制数据与恒等式核验记录于源码。']
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+'\\\\\n'.join(captions)+'\n\\end{minipage}\n\\end{center}\n\n'
anchor='在算法 A10.4 中';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
for ocr in ['Coons 表面 503','504 高级表面构造技术 Coons 表面 505','506 高级表面构造技术']:s=s.replace(ocr,'')
if n==30:
    # Remove the obsolete scan-page rule separating two halves of one algorithm.
    first=s.index('ALGORITHM A10.4');last=s.index('\\}',first)
    s=s[:first]+s[first:last].replace(r'\HRule','')+s[last:]
f.write_text(s,encoding='utf-8');print('10.'+str(n)+'placedinorderedconstructiongroupbeforeA10.4;scansremovedfromalgorithm.')
