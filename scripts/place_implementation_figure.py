"""Replace one printed implementation figure with its reviewed native record diagram."""
import argparse,re
from pathlib import Path
import image_tex as p
a=argparse.ArgumentParser();a.add_argument('figure');a.add_argument('tex');a.add_argument('caption',type=Path);a.add_argument('--width',default='26cm');a.add_argument('--before');args=a.parse_args()
d=p.load();e=next(e for e in d['images']if e['tex']=='image_tex/'+args.tex);assert e['applied'];f=p.ROOT/'chapter/13.tex';s=f.read_text(encoding='utf-8')
caption=args.caption.read_text(encoding='utf-8').strip();assert caption.startswith('图 '+args.figure+'.')
block='\\begin{center}\n\\begin{minipage}{'+args.width+'}\n\\centering\n'+e['replacement']+'\n\\par\\smallskip\n'+caption+'\n\\end{minipage}\n\\end{center}'
pat=r'\\begin\{center\}\s*'+re.escape(e['replacement'])+r'\s*\\end\{center\}\s*\\hspace\*\{3em\}\s*图\s*'+re.escape(args.figure)+r'\.[^\n]*';s,n=re.subn(pat,lambda _:block,s,count=1);assert n==1
if args.before:
    assert s.count(args.before)==1;s=s.replace(block,'',1).replace(args.before,'\n\n'+block+'\n\n'+args.before,1)
if args.figure=='13.5':s,n=re.subn(r'索引 \[j\]\s*是该列','索引[j]是该列',s,count=1);assert n==1
if args.figure=='13.6':s=s.replace(r'\hspace*{8em} *krv;',r'\hspace*{8em} *knv;')
if args.figure=='13.8':
    s,n=re.subn(r'调用例程\s*检查大多数错误','调用例程检查大多数错误',s,count=1);assert n==1
    s,n=re.subn(r'(typedef struct enode\s*)\\\(\\begin\{cases\}.*?\\end\{cases\}\\\)',lambda m:m.group(1)+r'\{',s,count=1,flags=re.S);assert n==1
f.write_text(s,encoding='utf-8');print('Placed implementation figure',args.figure,'at native text scale.')
