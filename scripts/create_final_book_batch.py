from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
audit=json.loads((root/'image_tex/build/final-native-audit.json').read_text(encoding='utf-8'));assert audit['remaining_original_images']==audit['remaining_HTML_images']==0
def src(*indices):return[f'ch01/fig_1_{i:02d}.tex'for i in indices]
figures={'1.3':src(3),'1.4':src(4),'1.5':src(5),'1.6':src(6),'1.7':src(7,8),'1.8':src(9,10),'1.9':src(11),'1.10':src(12),'1.11':src(13,14,15,16),'1.12':src(17),'1.13':src(18,19,20,21),'1.14':src(22),'1.15':src(23),'1.16':src(26),'1.17':src(27),'1.18':src(28),'1.19':src(29),'1.20':src(30),'1.21':src(31),'1.22':src(32),'13.1':[]}
figures.update({f'13.{i+1}':[f'ch13/fig_13_{i:02d}.tex']for i in range(1,9)})
text_regions={'图1.1:':src(1),'图1.2:':src(2),'表1.1.':src(24),'表1.2.':src(25),'typedef struct enode':[]}
b=dict(id='final-native-book',figures=figures,text_regions=text_regions,next_figure='complete',geometry_report='image_tex/build/final-native-audit.json',geometry_note='All435active originalreferences replaced by currentcompiled/reviewed semantic native sources,all13contentchapters plusbibliography/index checked,noactive raster/HTML references.436authoredmanifest sources include1coveredunusedreference. Finalbatch checks all8implementation figures, restoredinline13.1POINT/CPOINTtable andENODEbrace, andfreshens32legacychapter1layoutrecords withactualpage inspections,withoutchangingtheirgeometry. Everyactive source hascurrentlayoutsignature/evidence. Allpreviouschapterbatches compiled/published; finalfullsnapshot verifiesentireinputtree. Original40x80cmgeometry/11ptbody preserved;invalidheadfootoption fixed.')
path=root/'image_tex/build/final-native-book-batch.json';assert not path.exists();path.write_text(json.dumps(b,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('Created final fullbook batch with40reviewedsources,inline13.1andENODEregions;all435native references audited.')
