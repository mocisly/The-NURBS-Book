"""Group the five views of5.27 and restore their surrounding explanation."""
import re
import image_tex as pipeline
data=pipeline.load();entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in (34,35,36)]
assert all(e['applied'] for e in entries)
path=pipeline.ROOT/'chapter/5.tex';s=path.read_text(encoding='utf-8')
for e in entries:
    ref=e['replacement'];assert s.count(ref)==1
    pattern=r'\\begin\{center\}\s*'+re.escape(ref)+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*5\.27\.[^\n]*'
    s,count=re.subn(pattern,'',s,count=1);assert count==1,e['tex']
assert s.count('188 基础几何算法')==1;s=s.replace('188 基础几何算法','')
old='如何计算新的控制点。';assert s.count(old)==1
s=s.replace(old,'如何计算新的控制点，以及原始曲线与去节点曲线之间的偏差。')
old='点；以及原始曲线与去结点曲线之间的偏差。';assert s.count(old)==1;s=s.replace(old,'')
caption=(r'图 5.27. 三次曲线的近似节点移除，采用代表性十点控制网。各图尺度相同，(b)～(e)均从(a)独立移除。'
         '\\\\\n'+r'(a)$U=\{0,0,0,0,3/10,1/2,1/2,1/2,7/10,7/10,1,1,1,1\}$；(b)移除$3/10$一次；(c)、(d)、(e)分别移除$1/2$一、二、三次。'
         '\\\\\n'+r'(a)虚线为原控制多边形；(b)～(e)虚线为原曲线，实线为近似曲线及其控制多边形。示意采用局部逆节点插入拟合，保留未受影响的控制点。')
firstrow=('\\begin{minipage}[b]{12.2cm}\n'+entries[0]['replacement']+'\n\\end{minipage}\\hfill\n'
          '\\begin{minipage}[b]{25.2cm}\n'+entries[1]['replacement']+'\n\\end{minipage}')
block=('\\begin{center}\n\\begin{minipage}{38cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+firstrow+
       '\n\\par\\medskip\n'+entries[2]['replacement']+'\n\\par\\smallskip\n'+caption+
       '\n\\end{minipage}\n\\end{center}\n\n')
anchor='曲面结点移除的示例显示在';assert s.count(anchor)==1;s=s.replace(anchor,block+anchor,1)
for e in entries:assert s.count(e['replacement'])==1
path.write_text(s,encoding='utf-8')
print('Grouped5.27 five views3+2 after its explanation; restored triple1/2 caption, joined interrupted deviation paragraph.')
