"""10.10 actual chosen control data/weight matrix and continuity demonstration."""
from fractions import Fraction as F
import json,re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch10/fig_10_13.tex');assert e['applied']
f=p.ROOT/'chapter/10.tex';s=f.read_text(encoding='utf-8');r=json.loads((p.ROOT/'image_tex/build/rational-skin-continuity-check.json').read_text())
assert r['negative_surface_weight_indices_ij']==[[1,2],[3,2]]
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*10\.10。[^\n]*'
block=('\\begin{center}\n\\begin{minipage}{37cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+
       r'图 10.10. 正权有理截面的三维光滑性不一定由齐次空间蒙皮保留。'+'\\\\\n'+
       r'(a) 采用正文四组权值和共同二次节点$U=\{0,0,0,1/2,1/2,1,1,1\}$的代表性截面，均为$C^1$；'+'\\\\\n'+
       r'(b) 按式(10.14)求参数后进行齐次三次插值的曲面，粗线为$u=1/2$接缝。'+'\\\\\n'+
       r'四条截面在接点的左右导数均为$(0,4,0)$，曲面在接缝的中间位置却出现导数与切平面跳变。'+'\\\\\n'+
       r'控制点记录于源码，上方矩阵由同一数据重算；虽有负控制权值，本例整个参数域的分母仍严格大于$1/2$。'+'\n\\end{minipage}\n\\end{center}')
s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1
lead='在 \\(v\\) 方向的插值后，表面权重为:'
assert s.count(lead)==1
s=s.replace(lead,'为重绘选取的代表性控制点记录于源码。按式(10.14)进行四维弦长参数平均并在 \\(v\\) 方向三次插值后，曲面权值约为（矩阵的行对应 \\(j\\)，列对应 \\(i\\)）:',1)
rows=[' & '.join('1' if F(x)==1 else f'{float(F(x)):.4f}' for x in row) for row in r['surface_weight_rows_j_columns_i']]
matrix=r'{w}_{i,j}\simeq\left[\begin{matrix}'+r' \\ '.join(rows)+r'\end{matrix}\right]'
old=r'\{w\}_\{i,j\} = \\left\\lbrack\s*\\begin\{matrix\}.*?\\end\{matrix\}\\right\\rbrack'
s,n=re.subn(old,lambda _:matrix,s,count=1,flags=re.S);assert n==1
s=s.replace('(注意 \\({\\mathbf{P}}_{3,2}\\) 处的负权重)。','（本重绘例中的负权值为$w_{1,2}$和$w_{3,2}$。）',1)
f.write_text(s,encoding='utf-8');print('10.10actual C1sections/C0skin caption;matrix recomputed/approximately labelled with rowsj/columnsi;bothnegativeweightsindexedcorrectly.')
