---
title: "自然と建造環境は、同じ文章に現れるか"
description: "4つのユートピア文学をNature–Built軸で比較し、Bennett (2026) のNews from Nowhere読解で検証する10分発表"
lang: ja
---

:::: {.section .screen .center .title-slide}
::: kicker
10-minute research talk
:::

# 自然と建造環境は、同じ文章に現れるか

::: lead
4つのユートピア文学を意味軸で比較し、文学研究の具体例で検証する
:::

::: {.title-axis aria-label="Nature to Built axis"}
<span class="nature-word">river · tree · meadow</span>
<span class="axis-line"></span>
<span class="built-word">house · street · building</span>
:::

::: byline
*News from Nowhere* / *Looking Backward* / *Erewhon* / *A Crystal Age*<br>
Stage 2 analysis + Bennett (2026) external comparison
:::
::::

:::: {.section .screen}
::: kicker
1 — Question
:::

## Morrisは自然と都市を、より強く混ぜるのか？

::: lead
直感は「そうだ」。しかし、作品全体の量と、特徴的な一場面は分けて測る必要がある。
:::

::::: axis
::: {.panel .nature-panel}
**Nature pole**

river / tree / meadow / flower / mist
:::

::: arrow
×
:::

::: {.panel .built-panel}
**Built pole**

house / street / wall / building / window
:::
:::::

::: quote
**問い**

両極のstrong語が、同じ50語の窓に1語以上ずつ現れる割合を比較する。
:::
::::

:::: {.section .screen}
::: kicker
2 — Design
:::

## 固定した意味軸を、4作品へ同じ条件で適用

::: {.three-col .method-grid}
::: panel
**① 語の極性**

GloVe embeddingからNature–Built軸を作り、strong語彙をStage 1で凍結。
:::

::: panel
**② 局所窓**

50 word tokens、step 25。章境界を越えず、両極語があればmixed。
:::

::: panel
**③ 比較**

観測値、global shuffle、段落内shuffleを各1,000回比較。
:::
:::

::: {.case-tags .corpus-tags}
- 1891 *News from Nowhere*
- 1888 *Looking Backward*
- 1872 *Erewhon*
- 1919 rev. *A Crystal Age*
:::

::: note
本文・版・前処理・axisのSHA-256を固定し、同じNLTK pipelineで再現可能にした。
:::
::::

:::: {.section .screen}
::: kicker
3 — Main result
:::

## 全体では *A Crystal Age* が最もmixed

::: lead
主仮説「*News from Nowhere* が比較作品より多く両極を共存させる」は支持されなかった。
:::

<img class="hero-chart" src="assets/work_densities_and_mixing.png" alt="4作品のNature・Built語密度とmixed window率" />

::: {.result-strip}
<span><b>0.269</b><small>A Crystal Age</small></span>
<span><b>0.171</b><small>Erewhon</small></span>
<span class="focus"><b>0.159</b><small>News from Nowhere</small></span>
<span><b>0.087</b><small>Looking Backward</small></span>
:::
::::

:::: {.section .screen}
::: kicker
4 — Null model
:::

## 4作品とも、ランダム配置より両極が分離する

<img class="null-chart" src="assets/observed_vs_expected.png" alt="観測mixed率とglobal shuffle期待値" />

::: {.two-col .takeaway-grid}
::: panel
**global shuffle比**

Morrisは **0.756**。どの作品も1を下回り、Nature/Built語はランダムより凝集・分離する。
:::

::: panel
**段落内shuffle比**

Morrisは **0.927**。分離の多くは「別段落に置かれる」ことから生じる。
:::
:::
::::

:::: {.section .screen}
::: kicker
5 — Close reading: A Crystal Age
:::

## 自然が室内へ入り、人工物が自然形態を保存する

::: {.two-col .evidence-grid}
::: {.panel .excerpt-card .nature-panel}
**海が家の内部に響く**<br>
第5章 / mixed rank 4

> “the ocean’s voice is in their rooms … salt spray … low tide … the whitewinged bird”

`tide · sea · bird` × `roof · room · floor`
:::

::: {.panel .excerpt-card .built-panel}
**花が素材へ固定される**<br>
第14章 / mixed rank 7

> “The only flowers in the house … wrought in metal and carved in wood”

`flower` × `house · metal`
:::
:::

::: note
量的首位は、自然描写の多さだけでなく、室内・装飾・素材との反復的な結合による。
:::
::::

:::: {.section .screen}
::: kicker
6 — Close reading: News from Nowhere
:::

## Morrisの強みは「総量」より都市再編の場面にある

::: {.three-col .evidence-grid}
::: {.panel .excerpt-card}
**産業の荒廃**<br>
第10章 / rank 1

“manufacturing districts … Houses … trees were cut down … building”

`tree` × `manufacturing · house · building`
:::

::: {.panel .excerpt-card}
**開かれた古い家**<br>
第31章 / rank 2

“river … meadow … house … door and windows … flowers”

`river · meadow · flower` × `house · door · window`
:::

::: {.panel .excerpt-card}
**都市のMuseum**<br>
第8章 / rank 7

“railings were gone … boughs of the trees … pigeons … building”

`tree` × `building`
:::
:::

::: {.verdict}
作品全体の優越ではなく、London・建築・産業の変容を描く局所に注目する。
:::
::::

:::: {.section .screen}
::: kicker
7 — External comparison
:::

## Bennett (2026) の「rewilded Thames」で外部検証

::: {.paper-card}
<div class="paper-label">GREEN LETTERS · 20 SEP 2026</div>
<h3>Wild Belongings</h3>
<p>Stories of Rewilding in William Morris’s <i>News from Nowhere</i> and Diane Setterfield’s <i>Once Upon a River</i></p>
<p class="paper-author">Phillippa Bennett</p>
<a href="https://doi.org/10.1080/14688417.2026.2733353">doi:10.1080/14688417.2026.2733353</a>
:::

::: {.two-col .paper-points}
::: panel
**論文の焦点**

Thamesのagency、都市と田園の接続、環境正義、建築と土地の関係。
:::

::: panel
**照合単位**

論文が引用・要約するMorrisの **13場面** を採用版本文の文字offsetへ対応。
:::
:::
::::

:::: {.section .screen}
::: kicker
8 — Audit
:::

## 「12/13検出」だけでは、成功とは言えない

::: {.metric-grid}
::: {.metric .good}
<b>9</b>
<span>実質的ヒット</span>
<small>橋・道路・家・都市の森など</small>
:::

::: {.metric .weak}
<b>1</b>
<span>弱い／曖昧</span>
<small>tree × space</small>
:::

::: {.metric .bad}
<b>2</b>
<span>形式的誤検出</span>
<small>power / morning / night</small>
:::

::: {.metric .miss}
<b>1</b>
<span>未検出</span>
<small>town–countryの関係概念</small>
:::
:::

::: {.audit-line}
<span>binary mixed</span><b>12 / 13</b><span>→ 人手監査</span><b>9 + 1</b><span>有効候補</span>
:::

::: {.note .warn}
static embeddingは語義を分けない。数値は「物理的自然と都市」ではなく、凍結した意味軸の両極共存をまず測っている。
:::
::::

:::: {.section .screen}
::: kicker
9 — What was caught, what was missed
:::

## 橋は拾えた。町と田舎の関係は落ちた。

::: {.two-col .contrast-grid}
::: {.panel .caught}
**✓ 捕捉：Hammersmith Bridge**

論文頁5の「澄んだThames・鮭・工場の消失・新しい橋」。

Stage 2 rank 12：<br>
`river` × `building · booth · shop`

上位20と直接重なる論文事例はこの1クラスター。
:::

::: {.panel .missed}
**△ 未捕捉：town ↔ country**

論文頁6の「町と田舎が相互に影響し、差が小さくなる」。

10 overlapping windows中 **mixed = 0**

物体語ではなく、関係・変化を表す概念だからである。
:::
:::

::: quote
**改善の方向**

場所語・関係表現の辞書、または文脈埋め込みを加え、語義監査済みの結果と比較する。
:::
::::

:::: {.section .screen .center .closing-slide}
::: kicker
10 — Conclusion
:::

## 結論は「Morrisが最多」ではない

::: {.closing-points}
<div><b>1</b><span>*A Crystal Age* が4作品中もっとも高いlocal mixing。</span></div>
<div><b>2</b><span>Morrisの特徴は、都市・建築の再編を自然と結ぶ特定場面にある。</span></div>
<div><b>3</b><span>Bennettの13場面は9件を実質的に捕捉。ただし誤検出と概念的な取りこぼしが残る。</span></div>
:::

::: {.verdict .final-verdict}
量的比較で仮説を絞り、外部の文学研究とclose readingで意味を確かめる。
:::
::::

:::: {.section .flow .appendix}
::: kicker
Appendix — Sources & reproducibility
:::

## Sources

- Bennett, Phillippa. “Wild Belongings: Stories of Rewilding in William Morris’s *News from Nowhere* and Diane Setterfield’s *Once Upon a River*.” *Green Letters*, 2026. <https://doi.org/10.1080/14688417.2026.2733353>
- Morris, William. *News from Nowhere*. Reeves & Turner, 1891.
- Hudson, W. H. *A Crystal Age*. Duckworth, 1919 revised edition.
- Bellamy, Edward. *Looking Backward: 2000–1887*. Ticknor, 1888.
- Butler, Samuel. *Erewhon*. Trübner, 1872.

## Repository artifacts

- `slides.md`: editable source of truth
- `index.html`: generated presentation
- `data/work_summary.csv`: work-level results
- `data/permutation_summary.csv`: null-model results
- `data/bennett_2026_nfn_alignment.csv`: 13-case external alignment

::: note
Main window: 50 tokens / step 25. Global and paragraph-preserving permutations: 1,000 each. The primary frozen axis was not retuned after observing Stage 2 results.
:::
::::
