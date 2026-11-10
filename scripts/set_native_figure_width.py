"""Set a selected unapplied drawing to its containing block's natural width."""
import argparse
import image_tex as p
a=argparse.ArgumentParser(description=__doc__);a.add_argument('tex',nargs='+');args=a.parse_args()
d=p.load()
for path in args.tex:
    e=next(e for e in d['images'] if e['tex']=='image_tex/'+path)
    assert not e['applied'],path
    e['options']=r'max width=\linewidth'
p.save(d);print('Set native container width for '+', '.join(args.tex))
