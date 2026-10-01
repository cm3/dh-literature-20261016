---
title: "Bennett (2026) のMorris読解を計量的に検証する"
description: "4つの後期ヴィクトリア朝ユートピアをNature–Built軸で比較し、Bennett (2026) のNews from Nowhere読解を検証する10分発表"
lang: ja
---

:::: {.section .screen .center .title-slide}
::: kicker
10-minute research talk
:::

# Bennett (2026) のMorris読解を計量的に検証する

::: lead
「再野生化されたThames」と自然―建造環境の局所的な共存
:::

::: {.title-axis aria-label="Nature to Built axis"}
<span class="nature-word">river · tree · meadow</span>
<span class="axis-line"></span>
<span class="built-word">house · street · building</span>
:::

::: byline
*News from Nowhere* を、同時代のユートピア文学3作品と比較する<br>
Stage 2 quantitative analysis + close reading
:::
::::

:::: {.section .screen}
::: kicker
1 — Starting point: Bennett (2026)
:::

## 「rewilded Britain」という読解は、本文分布にも現れるか？

::: {.paper-card .paper-card-wide}
<div class="paper-label">GREEN LETTERS · 20 SEP 2026</div>
<h3>Wild Belongings</h3>
<p>Stories of Rewilding in William Morris’s <i>News from Nowhere</i> and Diane Setterfield’s <i>Once Upon a River</i></p>
<p class="paper-author">Phillippa Bennett</p>
<a href="https://doi.org/10.1080/14688417.2026.2733353">doi:10.1080/14688417.2026.2733353</a>
:::

::: {.three-col .claim-grid}
::: panel
**Thamesのagency**

川は人間の背景ではなく、自律的な存在として回復する。
:::

::: panel
**都市と田園の接続**

Londonは森・草地・果樹・川によって再編される。
:::

::: panel
**土地に応答する建築**

家や橋は自然と対立せず、土地から育つように構想される。
:::
:::

::: quote
**検証課題**　この読解は、自然語と建造環境語の局所的共存として測れるか。またMorrisに固有なのか。
:::
::::

:::: {.section .screen}
::: kicker
2 — Literary corpus
:::

## 4作品の文学史的位置づけ

::: lead
同時代に「よりよい社会」を描きながら、産業・都市・自然への態度が異なる4作品を選ぶ。
:::

::: {.two-col .corpus-grid}
::: {.panel .work-card .morris-card}
**William Morris, *News from Nowhere*** <span>1890 / 1891</span>

革命後の未来イングランドをThamesの旅として描く社会主義的・田園的ユートピア。Bennettの検証対象。
:::

::: {.panel .work-card}
**Edward Bellamy, *Looking Backward*** <span>1888</span>

西暦2000年のBostonを、中央集権的な産業組織と都市制度によって描く技術・制度中心の対照作。
:::

::: {.panel .work-card}
**Samuel Butler, *Erewhon*** <span>1872</span>

機械・病気・制度を反転して批判する風刺的ユートピア／ディストピア。産業文明への両義性を担う。
:::

::: {.panel .work-card}
**W. H. Hudson, *A Crystal Age*** <span>1887 / 1919 rev.</span>

遠未来の共同体を田園、家、装飾、家族秩序から描く牧歌的ロマンス。自然密度の高い比較作。
:::
:::

::: note
同一ジャンルの均質な標本ではなく、後期ヴィクトリア朝ユートピアの「自然―産業」スペクトラムをつくる小規模な比較コーパスである。
:::
::::

:::: {.section .screen}
::: kicker
3 — Operationalization
:::

## Bennettの質的主張をNature–Built mixingへ翻訳する

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

::: {.three-col .method-grid}
::: panel
**① 意味軸を凍結**

GloVe embeddingから軸を作り、strong語彙をStage 1で固定。
:::

::: panel
**② 50語の局所窓**

25語ずつ移動（50%重複）。章境界を保持し、両極のstrong語があればmixed。
:::

::: panel
**③ 二段階で検証**

4作品の全体比較 → Bennettが挙げる13場面の直接照合。
:::
:::

::: note
作品比較は「Morrisに固有か」を、13場面照合は「Bennettの具体例を拾えるか」を問う。
:::
::::

:::: {.section .screen}
::: kicker
4 — Corpus-level test
:::

## Morrisは比較コーパスで最多ではなかった

::: lead
*News from Nowhere* が自然と建造環境を最も多く共存させる、という強い予測は支持されない。
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
5 — Null model
:::

## 4作品とも、ランダム配置より両極を分けて置く

<img class="null-chart" src="assets/observed_vs_expected.png" alt="観測mixed率とglobal shuffle期待値" />

::: {.two-col .takeaway-grid}
::: panel
**global shuffle比**

Morrisは **0.756**。どの作品も1を下回り、Nature/Built語はランダムより凝集・分離する。
:::

::: panel
**段落内shuffle比**

Morrisは **0.927**。分離の多くは、両極が別段落へ配分されることから生じる。
:::
:::

::: {.verdict}
Bennettの読解は、作品全体の単純な「混合量」ではなく、特定場面の構成として検証すべきである。
:::
::::

:::: {.section .screen .chapter-summary-slide}
::: kicker
6 — News from Nowhere: chapter-level test
:::

## 章別mixingはThames航行部で上がる

::: lead
全32章を物語段階に分けると、Bennettが重視する川の旅にmixingが集中する。
:::

::: {.phase-grid}
::: panel
**Londonでの遭遇**<br>
第1–10章

<b>17.5%</b><small>184 / 1,050 windows</small>
:::

::: panel
**制度説明・革命史**<br>
第11–18章

<b>5.3%</b><small>45 / 854 windows</small>
:::

::: {.panel .focus-phase}
**Thames航行・帰還**<br>
第19–32章

<b>22.4%</b><small>256 / 1,142 windows</small>
:::
:::

::: {.two-col .chapter-findings}
::: panel
**Bennettが例を採る11章（窓を合算）**

mixed率 **21.4%**（204 / 953窓）。その他21章の **13.4%** より7.9ポイント高い。
:::

::: panel
**ピーク**

- **50.6%**　第30章 *The Journey’s End*
- **35.0%**　第20章
- **34.1%**　第21章
:::
:::

::: {.note .warn}
各区分の比率は窓を合算した値。隣接窓は50%重複し、短い章ほど率が不安定になる。ここでは有意差検定ではなく、物語構造に沿った記述的な偏りとして読む。
:::
::::

:::: {.section .flow .chapter-audit-slide}
::: kicker
7 — News from Nowhere: all 32 chapters
:::

## 全章監査：高いのは「川」だけではなく、川と家・街・労働が接する章

::: lead
棒は各章のmixed-window率。●はBennettが具体例を採った章を示す。行を縦にたどると、説明中心の第11–18章で谷になり、旅の再開後に上昇する。
:::

```{=html}
<div class="chapter-audit" role="region" aria-label="News from Nowhere chapter-level mixed-window rates">
<table>
  <thead><tr><th>章</th><th>章題</th><th>mixed率</th><th>分布</th><th>Bennett事例</th></tr></thead>
  <tbody>
    <tr class="phase-row"><th colspan="5">I　Londonでの遭遇（第1–10章）</th></tr>
    <tr><td>1</td><td>Discussion and Bed</td><td>16.7%</td><td><span class="rate-bar"><i style="width:33%"></i></span></td><td><button class="case-chip good" type="button" data-cases="NFN-02" aria-haspopup="dialog">● NFN-02</button></td></tr>
    <tr><td>2</td><td>A Morning Bath</td><td>29.8%</td><td><span class="rate-bar"><i style="width:59%"></i></span></td><td><button class="case-chip mixed" type="button" data-cases="NFN-03,NFN-04" aria-haspopup="dialog">● NFN-03/04</button></td></tr>
    <tr><td>3</td><td>The Guest House and Breakfast Therein</td><td>17.6%</td><td><span class="rate-bar"><i style="width:35%"></i></span></td><td></td></tr>
    <tr><td>4</td><td>A Market by the Way</td><td>22.2%</td><td><span class="rate-bar"><i style="width:44%"></i></span></td><td><button class="case-chip good" type="button" data-cases="NFN-06" aria-haspopup="dialog">● NFN-06</button></td></tr>
    <tr><td>5</td><td>Children on the Road</td><td>9.8%</td><td><span class="rate-bar"><i style="width:19%"></i></span></td><td><button class="case-chip good" type="button" data-cases="NFN-07,NFN-08" aria-haspopup="dialog">● NFN-07/08</button></td></tr>
    <tr><td>6</td><td>A Little Shopping</td><td>10.0%</td><td><span class="rate-bar"><i style="width:20%"></i></span></td><td></td></tr>
    <tr><td>7</td><td>Trafalgar Square</td><td>25.0%</td><td><span class="rate-bar"><i style="width:49%"></i></span></td><td></td></tr>
    <tr><td>8</td><td>An Old Friend</td><td>21.6%</td><td><span class="rate-bar"><i style="width:43%"></i></span></td><td></td></tr>
    <tr><td>9</td><td>Concerning Love</td><td>8.5%</td><td><span class="rate-bar"><i style="width:17%"></i></span></td><td></td></tr>
    <tr><td>10</td><td>Questions and Answers</td><td>20.0%</td><td><span class="rate-bar"><i style="width:40%"></i></span></td><td><button class="case-chip miss" type="button" data-cases="NFN-05" aria-haspopup="dialog">● NFN-05</button></td></tr>
    <tr class="phase-row"><th colspan="5">II　制度説明・革命史（第11–18章）</th></tr>
    <tr><td>11</td><td>Concerning Government</td><td>0.0%</td><td><span class="rate-bar"><i style="width:0%"></i></span></td><td></td></tr>
    <tr><td>12</td><td>Concerning the Arrangement of Life</td><td>4.0%</td><td><span class="rate-bar"><i style="width:8%"></i></span></td><td></td></tr>
    <tr><td>13</td><td>Concerning Politics</td><td>0.0%</td><td><span class="rate-bar"><i style="width:0%"></i></span></td><td><small>3窓のみ</small></td></tr>
    <tr><td>14</td><td>How Matters Are Managed</td><td>6.5%</td><td><span class="rate-bar"><i style="width:13%"></i></span></td><td></td></tr>
    <tr><td>15</td><td>On the Lack of Incentive to Labour…</td><td>2.6%</td><td><span class="rate-bar"><i style="width:5%"></i></span></td><td></td></tr>
    <tr><td>16</td><td>Dinner in the Hall of the Bloomsbury Market</td><td>14.0%</td><td><span class="rate-bar"><i style="width:28%"></i></span></td><td></td></tr>
    <tr><td>17</td><td>How the Change Came</td><td>6.1%</td><td><span class="rate-bar"><i style="width:12%"></i></span></td><td></td></tr>
    <tr><td>18</td><td>The Beginning of the New Life</td><td>2.7%</td><td><span class="rate-bar"><i style="width:5%"></i></span></td><td></td></tr>
    <tr class="phase-row"><th colspan="5">III　Thames航行・帰還（第19–32章）</th></tr>
    <tr><td>19</td><td>The Drive Back to Hammersmith</td><td>11.7%</td><td><span class="rate-bar"><i style="width:23%"></i></span></td><td></td></tr>
    <tr><td>20</td><td>The Hammersmith Guest-House Again</td><td>35.0%</td><td><span class="rate-bar"><i style="width:69%"></i></span></td><td><small>20窓</small></td></tr>
    <tr><td>21</td><td>Going up the River</td><td>34.1%</td><td><span class="rate-bar"><i style="width:67%"></i></span></td><td></td></tr>
    <tr><td>22</td><td>Hampton Court</td><td>20.9%</td><td><span class="rate-bar"><i style="width:41%"></i></span></td><td></td></tr>
    <tr><td>23</td><td>An Early Morning by Runnymede</td><td>24.7%</td><td><span class="rate-bar"><i style="width:49%"></i></span></td><td><button class="case-chip false" type="button" data-cases="NFN-01" aria-haspopup="dialog">● NFN-01</button></td></tr>
    <tr><td>24</td><td>Up the Thames: The Second Day</td><td>21.5%</td><td><span class="rate-bar"><i style="width:42%"></i></span></td><td><button class="case-chip caveat" type="button" data-cases="NFN-09" aria-haspopup="dialog">● NFN-09</button></td></tr>
    <tr><td>25</td><td>The Third Day on the Thames</td><td>23.8%</td><td><span class="rate-bar"><i style="width:47%"></i></span></td><td><button class="case-chip caveat" type="button" data-cases="NFN-13" aria-haspopup="dialog">● NFN-13</button></td></tr>
    <tr><td>26</td><td>The Obstinate Refusers</td><td>21.9%</td><td><span class="rate-bar"><i style="width:43%"></i></span></td><td><button class="case-chip good" type="button" data-cases="NFN-11" aria-haspopup="dialog">● NFN-11</button></td></tr>
    <tr><td>27</td><td>The Upper Waters</td><td>15.9%</td><td><span class="rate-bar"><i style="width:31%"></i></span></td><td></td></tr>
    <tr><td>28</td><td>The Little River</td><td>19.3%</td><td><span class="rate-bar"><i style="width:38%"></i></span></td><td></td></tr>
    <tr><td>29</td><td>A Resting-Place on the Upper Thames</td><td>18.5%</td><td><span class="rate-bar"><i style="width:37%"></i></span></td><td><button class="case-chip weak" type="button" data-cases="NFN-12" aria-haspopup="dialog">● NFN-12</button></td></tr>
    <tr class="peak"><td>30</td><td>The Journey’s End</td><td><b>50.6%</b></td><td><span class="rate-bar"><i style="width:100%"></i></span></td><td></td></tr>
    <tr><td>31</td><td>An Old House amongst New Folk</td><td>25.4%</td><td><span class="rate-bar"><i style="width:50%"></i></span></td><td><button class="case-chip good" type="button" data-cases="NFN-10" aria-haspopup="dialog">● NFN-10</button></td></tr>
    <tr><td>32</td><td>The Feast’s Beginning — The End</td><td>12.4%</td><td><span class="rate-bar"><i style="width:24%"></i></span></td><td></td></tr>
  </tbody>
</table>
</div>
```

::: note
色付きタグは事例監査の判定：緑＝実質的、青＝要留保、橙＝弱い、赤＝未検出／形式的誤検出。章率が高くても個々の語義監査は別に必要である。
:::
::::

:::: {.section .screen}
::: kicker
8 — News from Nowhere: local evidence
:::

## Bennettの論点に対応するmixed場面は、局所的には強い

::: {.three-col .evidence-grid}
::: {.panel .excerpt-card .scene-card .scene-industrial}
**産業の荒廃**<br>
第10章 / rank 1

“manufacturing districts … Houses … trees were cut down … building”

`tree` × `manufacturing · house · building`
:::

::: {.panel .excerpt-card .scene-card .scene-old-house}
**開かれた古い家**<br>
第31章 / rank 2

“river … meadow … house … door and windows … flowers”

`river · meadow · flower` × `house · door · window`
:::

::: {.panel .excerpt-card .scene-card .scene-museum}
**都市のMuseum**<br>
第8章 / rank 7

“railings were gone … boughs of the trees … pigeons … building”

`tree` × `building`
:::
:::

::: {.verdict}
Morrisの特徴は全体量ではなく、London・建築・産業を自然との関係から作り直す場面にある。
:::

::: image-disclaimer
背景画像は本文の記述に基づく生成イラストであり、同時代の史料画像ではない。
:::
::::

:::: {.section .screen}
::: kicker
9 — Comparative counterexample
:::

## *A Crystal Age* は別の仕方で、より頻繁に両極を結ぶ

::: {.two-col .evidence-grid}
::: {.panel .excerpt-card .nature-panel .scene-card .scene-ocean-rooms}
**自然が家の内部に響く**<br>
第5章 / mixed rank 4

> “the ocean’s voice is in their rooms … salt spray … low tide … the whitewinged bird”

`tide · sea · bird` × `roof · room · floor`
:::

::: {.panel .excerpt-card .built-panel .scene-card .scene-artificial-flowers}
**自然形態が素材へ固定される**<br>
第14章 / mixed rank 7

> “The only flowers in the house … wrought in metal and carved in wood”

`flower` × `house · metal`
:::
:::

::: note
Morrisのrewildingが都市・社会の変容を語るのに対し、Hudsonでは自然と室内・装飾の接続が反復される。mixing率だけでは両者の文学的機能は区別できない。
:::

::: image-disclaimer
背景画像は本文の記述に基づく生成イラストであり、同時代の史料画像ではない。
:::
::::

:::: {.section .flow .crystal-evidence-slide}
::: kicker
10 — A Crystal Age: extended evidence
:::

## 自然と建築は、少なくとも6つの異なる仕方で接続される

::: lead
上位mixed窓を原文へ戻し、多義語による誤検出を除きながら読む。Hudsonの高いmixing率は、単一の反復語ではなく、室内・素材・眺望・比喩を横断する。
:::

::: {.long-evidence-list}
::: {.panel .long-example}
<b>1　花が窓と室内を変える</b><span>第3章 · rank 2</span>

> “lilies … This lovely window gave a fresh charm to the whole apartment …”

`lily` × `window · apartment`。花と採光が室内の見え方を変える。`hand/piece` は多義語由来なので解釈から除外。
:::

::: {.panel .long-example}
<b>2　海が家の内部に響く</b><span>第5章 · rank 4</span>

> “the ocean’s voice is in their rooms … salt spray … low tide … the whitewinged bird”

`tide · sea · bird` × `roof · room · floor`。海・風・砂・鳥がHouse of Coradineの室内へ入り込む比喩。
:::

::: {.panel .long-example}
<b>3　生花の不在を人工の花が示す</b><span>第14章 · rank 7</span>

> “The only flowers in the house … wrought in metal and carved in wood … stony flowers”

`flower` × `house · metal`。自然物を金属・木・石に固定する装飾が、家の秩序と禁忌を可視化する。
:::

::: {.panel .long-example}
<b>4　葉の形が金属の扉になる</b><span>第3章 · rank 9</span>

> “horse-chestnut leaves of brass or copper … a double door with agate handles”

`leaf` × `brass · door · handle`。植物形態が素材と建具へ翻訳される。色彩語`grey/shade/yellow`はNature hitから除外して読む。
:::

::: {.panel .long-example}
<b>5　ポルティコが川への視線を組み立てる</b><span>第4章 · rank 14</span>

> “a large portico-like place … the roof … the house … looked upon the river”

`river` × `roof · house`。開放された建築が自然を遮断せず、川を眺めるフレームとして働く。
:::

::: {.panel .long-example}
<b>6　ステンドグラスから川霧へ連続する</b><span>第12章 · rank 16</span>

> “stained glass in the windows … river … white mist … reeds and bushes … old trees”

`river · mist · tree` × `glass · window`。室内的な比喩から川景へ視線が滑り、人工光景と自然景が連続する。
:::
:::

::: {.verdict}
Hudsonでは「自然が都市を取り戻す」より、自然の形・音・眺望が家の内部と装飾体系へ取り込まれる。量的な高さは同じでも、Morrisとは物語上の機能が異なる。
:::
::::

:::: {.section .screen}
::: kicker
11 — Direct validation of Bennett's examples
:::

## Bennettの13場面を照合すると、9件は実質的に拾える

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
<span>binary mixed</span><b>12 / 13</b><span>→ 語義を人手監査</span><b>9 + 1</b><span>有効候補</span>
:::

::: {.note .warn}
「12/13を検出」だけなら過大評価になる。static embeddingの多義語を除くと、明確な支持は9件である。
:::
::::

:::: {.section .screen}
::: kicker
12 — Diagnostic cases
:::

## 橋は拾えた。町と田舎の関係は落ちた。

::: {.two-col .contrast-grid}
::: {.panel .caught}
**✓ 捕捉：Hammersmith Bridge**

Bennett論文頁5の「澄んだThames・鮭・工場の消失・新しい橋」。

Stage 2 rank 12：<br>
`river` × `building · booth · shop`

上位20と直接重なる論文事例はこの1クラスター。
:::

::: {.panel .missed}
**△ 未捕捉：town ↔ country**

論文頁6の「町と田舎が相互に影響し、差が小さくなる」。

10 overlapping windows中 **mixed = 0**

物体語ではなく、関係と変化を表す概念だからである。
:::
:::

::: quote
**次の改善**　場所語・関係表現の辞書、または文脈埋め込みを加え、語義監査済みの結果と比較する。
:::
::::

:::: {.section .screen .center .closing-slide}
::: kicker
13 — Answer to Bennett
:::

## 計量分析はBennettを「限定つきで」支持する

::: {.closing-points}
<div><b>1</b><span><strong>支持：</strong>論文の13場面中9件で、自然と建造環境の実質的な局所共存を確認した。</span></div>
<div><b>2</b><span><strong>限定：</strong>Morrisは比較コーパスで最多ではなく、rewildingの特徴は作品全体量より場面の機能にある。</span></div>
<div><b>3</b><span><strong>課題：</strong>town–countryのような関係概念と、static embeddingの多義語を別の方法で扱う必要がある。</span></div>
:::

::: {.verdict .final-verdict}
Bennettのclose readingを置き換えるのではなく、どの主張が分布として再現し、どこから解釈が必要かを可視化する。
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
- `data/nfn_chapter_summary.csv`: Morrisの全32章とBennett事例の対応
- `data/bennett_2026_nfn_alignment.csv`: 13-case external alignment

::: note
Main window: 50 tokens、25語ずつ移動（50%重複）。Global and paragraph-preserving permutations: 1,000 each. The primary frozen axis was not retuned after observing Stage 2 results.
:::
::::
