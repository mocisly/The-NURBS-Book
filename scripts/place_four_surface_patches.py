"""Group Fig5.14's formerly separated net/surface panels side by side."""
from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1];data=json.loads((root/'image_tex/manifest.json').read_text(encoding='utf-8'))
entries=[next(e for e in data['images'] if e['tex']==f'image_tex/ch05/fig_5_{n}.tex') for n in (15,16)];assert all(e['applied'] for e in entries)
p=root/'chapter/5.tex';s=p.read_text(encoding='utf-8');intervals=[]
for e in entries:
    ref=e['replacement'];assert s.count(ref)==1;start=s.index('\\begin{center}\n'+ref);cap=re.search(r'(?m)^图\s*5\.14[.。].*$',s[start:]);assert cap
    intervals.append((start,start+cap.end()))
position=intervals[0][0]
for start,end in sorted(intervals,reverse=True):s=s[:start]+s[end:]
caption=(r'图 5.14. 同时在 \(u=2/5\)、\(v=7/10\) 处细分图 5.11 的曲面。(a) 四块子曲面的控制网；(b) 对应的子曲面。各块保持原参数化，实际沿公共边界相接；图中仅作平移分开显示。')
panels='\\begin{minipage}{12cm}\n\\centering\n'+entries[0]['replacement']+'\n\\end{minipage}\\hfill\n\\begin{minipage}{12cm}\n\\centering\n'+entries[1]['replacement']+'\n\\end{minipage}'
block='\\begin{center}\n\\begin{minipage}{24.5cm}\n\\vspace*{.6\\baselineskip}\n\\centering\n'+panels+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}\n\n'
s=s[:position]+block+s[position:];assert s.count('162 基本几何算法')==1;s=s.replace('162 基本几何算法','')
assert all(s.count(e['replacement'])==1 for e in entries);p.write_text(s,encoding='utf-8')
print('Grouped Fig5.14(a,b) together before the curve-extraction discussion; removed obsolete OCR page header.')
