"""Keep8.16 at the rolling-ball introduction,before stereographic construction."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch08/fig_8_21.tex');assert e['applied']
f=p.ROOT/'chapter/8.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*8\.16\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
anchor='除了获得角落圆角表面外';assert s.count(anchor)==1
block=('\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 8.16. 三平面角点的圆角过渡；两图采用相同投影、比例和坐标原点。'+'\\\\\n'+
       r'(a) 示例平面$\mathbf S_1:z=3/2$、$\mathbf S_2:y=1$、$\mathbf S_3:x=1$及其三条交线。'+'\\\\\n'+
       r'(b) 取共同圆角半径$R=11/20$，边缘圆角$\mathbf S_4,\mathbf S_5,\mathbf S_6$分别为沿$x,z,y$方向的四分之一圆柱面；$\mathbf S_7$为球面角片。'+'\\\\\n'+
       r'球心为$(9/20,9/20,19/20)$；球面角片与三个圆柱面相切，圆柱面分别与原平面相切。实线表示过渡面的边界，虚线表示原尖锐交线。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);s=s.replace('一个角落 352 常见表面的圆角','一个角落圆角')
assert s.count(e['replacement'])==1;f.write_text(s,encoding='utf-8')
print('Placed8.16 after rolling-ball explanation,before quadric/stereographic construction.')
