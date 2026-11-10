"""Render a caption and the preceding page area for visual layout review."""
import argparse
import re
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf',type=Path)
    parser.add_argument('figure',help='Printed figure number, e.g. 1.18')
    parser.add_argument('output',type=Path)
    parser.add_argument('--height',type=float,default=360,help='Crop height in PDF points')
    parser.add_argument('--after',type=float,default=30,help='PDF points below the first caption line, for wrapped captions')
    parser.add_argument('--dpi',type=int,default=100)
    parser.add_argument('--text',action='store_true',help='Locate a unique literal phrase instead of a numbered caption')
    args=parser.parse_args()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    bbox=args.output.with_suffix('.bbox.html')
    subprocess.run(['pdftotext','-bbox',str(args.pdf),str(bbox)],check=True)
    ns={'h':'http://www.w3.org/1999/xhtml'}
    xml=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '',bbox.read_text(encoding='utf-8'))
    pages=ET.fromstring(xml).findall('.//h:page',ns)
    matches=[]
    for index,page in enumerate(pages,1):
        words=page.findall('h:word',ns)
        if args.text:
            combined=''.join(word.text or '' for word in words)
            needle=re.sub(r'\s+','',args.figure)
            position=combined.find(needle)
            if position>=0:
                assert combined.find(needle,position+1)<0
                length=0
                for word in words:
                    length+=len(word.text or '')
                    if length>position:
                        matches.append((index,page,word));break
            continue
        for i,word in enumerate(words):
            if word.text==args.figure+'.' and i and words[i-1].text in ('图','表'):
                matches.append((index,page,word))
    if len(matches)!=1:
        raise ValueError(f'Expected one caption, got {len(matches)} for {args.figure}')
    number,page,caption=matches[0]
    yend=min(float(page.attrib['height']),float(caption.attrib['yMax'])+args.after)
    ystart=max(0,yend-args.height)
    scale=args.dpi/72
    subprocess.run(['pdftoppm','-f',str(number),'-singlefile','-r',str(args.dpi),
                    '-x','0','-y',str(round(ystart*scale)),
                    '-W',str(round(float(page.attrib['width'])*scale)),
                    '-H',str(round((yend-ystart)*scale)),'-png',str(args.pdf),str(args.output)],check=True)
    print(f'Figure {args.figure}: PDF page {number}, {args.output.with_suffix(".png")}')


if __name__=='__main__':
    main()
