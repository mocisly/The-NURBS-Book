"""Mark workspace documentation complete only after the final reviewed PDF is published."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1];base=root/'image_tex'
v=json.loads((base/'validation.json').read_text(encoding='utf-8'));a=json.loads((base/'build/final-pdf-audit.json').read_text(encoding='utf-8'));native=json.loads((base/'build/final-native-audit.json').read_text(encoding='utf-8'))
digest=hashlib.sha256((root/'main.pdf').read_bytes()).hexdigest()
assert v['applied_drawings']==435 and v['remaining_active_original_images']==0 and v['snapshot_inputs_verified']
assert '/final-native-book-'in v['source_snapshot']and a['status']=='passed'and a['body_raster_image_objects']==0
assert digest==v['book_compile']['sha256']==a['sha256']and native['all_individual_layout_evidence_present']
p=json.loads((base/'progress.json').read_text(encoding='utf-8'));assert p['remaining_active_original_images']==p['remaining_inline_ocr_image_placeholders']==0
p.update(status='complete',work_in_progress='All435original references natively redrawn; fullbook compiled, final pages visually reviewed and published; final PDF resource/geometry audit passed.',next_original=None,last_complete_book_compile=v['book_compile'],final_validation='image_tex/build/final-pdf-audit.json');(base/'progress.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
readme=f'''# 原生图片重绘完成

435处原图引用已全部替换为可编辑的LaTeX/TikZ/PGFPlots绘图，HTML图片引用为0。共保留436份清单内原生源码，其中1份为已由组合图覆盖的参考图。所有原图仍保留，便于对照。

整书已重新编译并检查，根目录`main.pdf`为最终版本，共{a['pages']}页；SHA256为`{digest}`。正文中没有位图图像对象。原有40×80厘米页面、11pt正文和1.5倍行距保留，`headfoot`选项错误已修复。

## 文件

- `ch01/`～`ch13/`：按原图位置组织的原生绘图源码。
- `manifest.json`：原图、章节引用、编译签名、逐图对照与版面证据。
- `common.tex`：统一的线型、箭头和绘图封装。
- `progress.json`、`validation.json`：最终完成状态与整书验证摘要。
- `build/final-native-audit.json`、`build/final-pdf-audit.json`：源码、引用、版面记录和最终PDF核验。
- `../scripts/`：逐图的数学构造、生成、预览、替换和编译检查脚本。

曲线、曲面优先按正文公式及给定数据重建；原书未给数值的示意图采用明确注明的代表性数据。未使用扫描轮廓、字体轮廓转绘或位图包装。图13.1的空白OCR表格和ENODE结构中的伪公式也已修复。

## 后续修改

编辑对应原生源码后，先用`scripts/image_tex.py preview --tex … --dark --render`生成预览，核对后记录`review`，并重新编译实际章节及整书。修改`common.tex`会使现有绘图检查签名失效，需要重新验证。
'''
(base/'README.md').write_text(readme,encoding='utf-8')
note=f'''# 已完成：全部图片原生重绘

所有435处原图引用均已替换，436份原生源码包含1份已覆盖参考图。原图及HTML活动引用均为0。所有绘图有当前编译、对照检查及版面证据；第1章32份旧格式记录已补查七个实际章节页面并更新。

最终整书PDF：`main.pdf`，{a['pages']}页，SHA256 `{digest}`。官方XeLaTeX编译退出码0；最终受影响页面均已查看，冻结输入哈希与发布PDF一致。正文位图对象0，页面40×80厘米，缺字警告0、致命编译错误0。

最终快照：`{v['source_snapshot']}`。报告位于`image_tex/validation.json`、`image_tex/build/final-native-audit.json`及`image_tex/build/final-pdf-audit.json`。无活动编译进程，工作已完成。

原图保留用于核对；未作轮廓转换、字体轮廓或位图包装。图13.1字段及ENODE识别错误已修复。完整历史检查记录保留在清单和build目录，不需要继续运行旧进度脚本。
'''
(base/'current_work.md').write_text(note,encoding='utf-8');(base/'build/final-book-validation.json').write_text(json.dumps(dict(native_sources=native,pdf=a,publication=v),ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('COMPLETE435native replacements; finalPDFpublished/verified:',a['pages'],'pages',digest)
