"""Use inherited book colors and the containing minipage's native width."""
import image_tex as p
d=p.load();chapter=p.ROOT/'chapter/5.tex';s=chapter.read_text(encoding='utf-8')
for n in range(47,51):
    e=next(e for e in d['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex')
    f=p.ROOT/e['tex'];t=f.read_text(encoding='utf-8');assert 'fill=bookbg' in t
    f.write_text(t.replace('fill=bookbg','fill=none'),encoding='utf-8')
    old=e['replacement'];assert s.count(old)==1
    e['options']=r'max width=\linewidth'
    e['replacement']=r'\BookFigure[max width=\linewidth]{ch05/fig_5_'+str(n)+'.tex}'
    s=s.replace(old,e['replacement'],1)
chapter.write_text(s,encoding='utf-8');p.save(d)
print('Fixed local marker color and retained native physical font/stroke sizes within30.2cm figure group.')
