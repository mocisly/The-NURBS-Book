"""Move9.6 out of Ex9.1 to its degree-comparison discussion."""
import re
import image_tex as p
d=p.load();e=next(e for e in d['images'] if e['tex']=='image_tex/ch09/fig_9_06.tex');assert e['applied']
f=p.ROOT/'chapter/9.tex';s=f.read_text(encoding='utf-8')
pattern=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*9\.6\.[^\n]*'
s,n=re.subn(pattern,'',s,count=1);assert n==1
s=s.replace('368 曲线与曲面拟合','',1)
anchor='图 9.7 显示了全局插值器无法处理共线点集的情况。';assert s.count(anchor)==1
block=('\n\n\\begin{center}\n\\begin{minipage}{27cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+e['replacement']+
       '\n\\par\\smallskip\n'+r'图 9.6. 同一组七点在不同次数下的全局插值，代表性数据与图 9.5 相同。'+'\\\\\n'+
       r'实线、虚线和点划线分别为二次、三次和四次曲线；均使用同一弦长参数，并按各次数平均计算节点。'+'\\\\\n'+
       r'下方三组标尺依次对应$p=2,3,4$；圆圈表示数据参数，短刻线表示节点。'+
       '\n\\end{minipage}\n\\end{center}\n\n')
s=s.replace(anchor,block+anchor,1);f.write_text(s,encoding='utf-8')
print('Moved9.6 before example;kept degree comparison and complete caption together.')
