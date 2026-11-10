"""Place only the selected printed Gordon stage beside its explanation."""
import argparse,re
import image_tex as p
a=argparse.ArgumentParser();a.add_argument('number',type=int,choices=(19,20,21,22,23));args=a.parse_args()
d=p.load();f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8')
specs={19:([26],r'\(v\) 方向的升高',[
r'图 10.19. 同一兼容网络的$u$向放样曲面$L_1(u,v)$。',
r'(a) $4\times5$实际控制网；(b) 精确插值四条$C_\ell(v)$的曲面，粗实线为输入$v$曲线，虚线为另一组参考曲线。',
r'使用三次Bezier的$u$基与原二次$V^C$基；两图使用相同投影、尺度和字号。']),
20:([27],'张量积曲面如图',[
r'图 10.20. 同一兼容网络的$v$向放样曲面$L_2(u,v)$。',
r'(a) $6\times5$实际控制网；(b) 精确插值五条$C_k(u)$的曲面，粗实线为输入$u$曲线，虚线为另一组参考曲线。',
r'代表性数据采用$V^* =\{0,0,0,.321,.647,1,1,1\}$，后续交点插值复用此基。']),
21:([28],'注意节点向量',[
r'图 10.21. 二十个网络交点的张量积插值曲面$T(u,v)$。',
r'(a) $4\times5$实际控制网；(b) 曲面通过全部圈点，曲面网格为真实等参数曲线。',
r'重绘复用$L_1$的三次$u$基和$L_2$的二次$V^*$基，以保证式(10.32)的精确抵消。']),
22:([29,30],'如前所述，输入曲线的度',[
r'图 10.22. 在公共B样条基中表示三个曲面，几何形状保持不变。',
r'(a) $L_1$，(b) $L_2$，(c) $T$细化后的实际控制网，均为$6\times7$控制点。',
r'本重绘共用$U^C$与$V=\{0,0,0,.321,.4,.6,.647,1,1,1\}$；三图投影、尺度和字号一致。']),
23:([31],r'\section{库恩斯表面}',[
r'图 10.23. 同一网络的Gordon曲面$S=L_1+L_2-T$。',
r'(a) 在公共基中逐控制点相加减所得的$6\times7$控制网；(b) 最终曲面。',
r'粗实线为全部九条输入曲线；整条曲线的控制系数恒等式验证了双向精确插值。',
r'圈点满足$P_{5,1}=P^{L_1}_{5,1}+P^{L_2}_{5,1}-P^T_{5,1}$。'])}
sources,anchor,captions=specs[args.number];entries=[]
for n in sources:
    e=next(e for e in d['images'] if e['tex']==f'image_tex/ch10/fig_10_{n:02}.tex');assert e['applied'];entries.append(e)
    if args.number==22:
        caption=r'图 10\.22\.[^\n]*'
    else:caption=r'图 10\.'+str(args.number)+r'\.[^\n]*'
    pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*'+caption
    s,nremoved=re.subn(pat,'',s,count=1);assert nremoved==1,(args.number,n)
body=entries[0]['replacement']
if len(entries)==2:body+='\\par\\vspace{.5cm}\n'+entries[1]['replacement']
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+body+'\n\\par\\smallskip\n'+('\\\\\n'.join(captions))+'\n\\end{minipage}\n\\end{center}\n\n'
assert s.count(anchor)==1,(anchor,s.count(anchor));s=s.replace(anchor,block+anchor,1)
if args.number==19:
    note=(r'（重绘说明：本组图采用相同的代表性控制点及交点参数；为严格满足式(10.31)—(10.32)，$L_2$与$T$复用同一插值基$V^*=\{0,0,0,.321,.647,1,1,1\}$，采用下文建议的近邻节点复用。正文所列独立计算的节点数值仍属原例。）'+'\n\n')
    marker='图 \\({10.19}\\mathrm{a}\\)';assert s.count(marker)==1;s=s.replace(marker,note+marker,1)
for ocr in ['双向曲线网络的插值 491','490 高级表面构造技术','492 高级表面构造技术 双向曲线网络的插值 493','双向曲线网络的插值 495']:s=s.replace(ocr,'')
f.write_text(s,encoding='utf-8');print('Placed10.'+str(args.number)+'nexttoitsactualexplanation/knots.')
