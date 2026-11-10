import re,argparse
import image_tex as p
a=argparse.ArgumentParser();a.add_argument('figure',type=int,choices=(37,38));fig=a.parse_args().figure
d=p.load();e=next(e for e in d['images']if e['tex']==f'image_tex/ch11/fig_11_{fig+8}.tex');assert e['applied'];f=p.ROOT/'chapter/11.tex';s=f.read_text(encoding='utf-8')
caption=r'图 11.'+str(fig)+r'. 基于位置约束的曲面修改；$u=v=1/2$，$\Delta S=(0,0,1)$。'+'\\\\\n'+(r'允许所有12个有影响的局部控制点移动，按式(11.85)—(11.86)求最小范数解。'if fig==37 else r'只允许$P_{1,2},P_{2,2},P_{4,2}$移动，其余控制点固定；仍精确达到相同目标位置。')+'\\\\\n'+r'(a) 原控制网及修改后的虚线控制网，箭头表示控制点位移；(b) 实际张量积曲面的原网格与修改后的虚线等参线。'+'\\\\\n'+r'采用同一张代表性$3\times2$次、$6\times5$控制点曲面，四条完整边界保持不变；两图使用相同投影和尺度。'
block='\\begin{center}\n\\begin{minipage}{37cm}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}'
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图 11\.'+str(fig)+r'\.[^\n]*';s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1;f.write_text(s,encoding='utf-8');print('Placed surface constraint figure',fig)
