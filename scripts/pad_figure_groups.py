"""Keep native figure groups clear of the zero-headsep book's running header."""
from pathlib import Path
import re,argparse

p=argparse.ArgumentParser(description=__doc__);p.add_argument('chapter',type=int);a=p.parse_args()
root=Path(__file__).resolve().parents[1];path=root/'chapter'/f'{a.chapter}.tex'
text=path.read_text(encoding='utf-8')
pattern=r'(\\begin\{minipage\}\{[^}]+\}\n)(?!\\vspace\*\{\.6\\baselineskip\})'
updated,count=re.subn(pattern,lambda m:m[1]+r'\vspace*{.6\baselineskip}'+'\n',text)
path.write_text(updated,encoding='utf-8')
print(f'Added consistent top padding to {count} figure groups in chapter{a.chapter}.')
