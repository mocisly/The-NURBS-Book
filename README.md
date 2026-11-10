# The-NURBS-Book
The-NURBS-Book

## 纸张与页眉页脚

页面采用 ISO A1 竖版（594 × 841 mm），左右页边距 22 mm。页眉和页脚计入版心边距，页眉高度 24 pt，页眉下方留白 12 mm，页脚基线距正文底部 14 mm。

普通页左上显示章名，右上显示书名；左下显示节名，右下显示绿色页码，以低对比度细线分隔正文。章首页省略重复页眉，保留统一页脚。正文维持 11 pt 和 1.5 倍行距。

## 代码与算法排版

代码使用 `minted` 和 `monokai` 样式；等宽字体为 Consolas，中文注释使用 Microsoft YaHei。字体、字号、背景色和换行设置统一放在 `main.tex`。

第13章的 C 示例直接使用原始代码，不需要给 `#`、`_`、`%`、花括号或缩进添加 LaTeX 转义：

```latex
\begin{minted}{c}
typedef struct curve
{
    CPOLYGON *pol;
    DEGREE p;
    KNOTVECTOR *knt;
} CURVE;
\end{minted}
```

前12章的编号算法保留为伪代码。其 `escapeinside=@@` 用于嵌入数学公式和中文说明，`mathescape` 用于注释中的公式；它们不代表可直接编译运行的 C 程序。代码块允许长行换行和跨页，避免用 `minipage` 包住长程序。

## 编译

本项目使用 XeLaTeX。当前 TeX Live 2024 的 `minted 2.9` 需要 PATH 中可运行的 `pygmentize`，并开启 `--shell-escape`。Windows 可运行 `make.bat`，也可以执行：

```powershell
latexmk -xelatex -shell-escape -interaction=nonstopmode -halt-on-error main.tex
```

使用独立输出目录时还需设置 minted 的 `outputdir`。`scripts/preview_chapter.py` 和 `scripts/compile_minted_book.py` 已处理该配置。后者先生成隔离的整书 PDF，检查并记录版面后才可发布到根目录。

`python -B scripts/build_a1_book.py` 在 `tmp/a1-review/` 编译 A1 整书，并检查纸张尺寸、61 个编号算法和章节源码。该脚本生成供检查的 PDF，不自动覆盖根目录成品。当前整书、参考文献和索引核验见 `image_tex/reports/backmatter-*.json`；逐图尺度与正文搭配见 `figure-layout-*.json`；`a1-layout-*.json` 为此前页眉页脚改版记录。

`image_tex/reports/code-listings-*.json` 保存本次代码排版的检查记录。临时编译、代码预览和迁移对照位于 `tmp/minted-review/` 与 `image_tex/build/`，可以清理，正式编译不依赖它们。`scripts/migrate_code_listings.py` 是本次迁移使用的一次性工具，日常修改直接编辑章节中的 minted 块即可。

## 图片尺寸

简单图以图1-1、图1-2为尺度参考，复杂多面板和数据结构图按信息密度保留较大尺寸。`image_tex/figure-scales.tex`逐图控制几何尺度，图中文字保持原字号。图1-2置于速度比较之后、球面介绍之前。

`python -B scripts/compile_figure_layout.py`在`tmp/figure-layout/book/`编译并验证整书，不直接覆盖根目录成品。正式源码、图片倍率、脚本、原图和核验报告需要保留；临时样张与编译缓存可以用清理脚本删除。

## 参考文献与索引

第14章使用原生 `\bibitem[作者年份编号]{key}`；正文通过 `\cite{key}` 引用。合并年份已展开为完整文献键，173条文献的原始内容保留。文献条目中的期刊/论文页码属于文献本身，不随本书分页修改。

第15章使用 MakeIndex 自动排页码，四栏显示，主条目按拼音或英文名称排序。359个条目在 `backmatter/index-entries.json` 中维护；正文的 `\BookIndexMark{pNNNN}` 对应 `backmatter/index-locations.json` 和生成的 `index-marks.tex`。页码均可点击跳至正文；重新分页后无需手工改索引数字。

`.latexmkrc` 为 MakeIndex 指定 `backmatter/book.ist`，因此应使用 `make.bat`、`make` 或上面的 latexmk 命令，不能只执行两次 XeLaTeX 后就认为索引已更新。需要手工构建时，按 XeLaTeX → `makeindex -s backmatter/book.ist main.idx` → XeLaTeX 的顺序执行，并继续编译至引用和页码稳定。

维护索引时，编辑 `backmatter/index-entries.json` 中的层级、排序键和精确定位条件，再执行 `python -B scripts/restore_backmatter.py index` 更新标记。`scripts/curate_book_index.py` 和 `restore_backmatter.py bibliography` 是本次OCR恢复的一次性迁移工具，日常不应覆盖已编辑的数据。

本次恢复流程的 `compile_backmatter_book.py`、`audit_backmatter_pdf.py` 和 `publish_backmatter_book.py` 保存隔离编译、核验和发布步骤，发布依赖对应的迁移基线及审阅报告。清理后如修改源码，应为新的审阅流程建立基线；日常重新排版直接使用 `make.bat` 或 latexmk。`backmatter/`、`.latexmkrc`、章节源码、脚本和报告是正式文件；`tmp/backmatter/` 与编译缓存可清理。
