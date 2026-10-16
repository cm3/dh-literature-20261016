# Utopian Nature–Built Talk

約10分のHTMLスライドです。Bennett (2026) の *News from Nowhere* 読解を、
自然物・人工物の116語による4作品の再集計、Morrisの章別分布、本文の場面で検討します。
4作品の共存率とMorrisの章別分布はProject Gutenberg版本文で再計算しました。
後半ではBennettの13事例について、Internet Archive版・GloVe軸由来の314語を使った
別分析で、自然と建造環境の実質的な共存を9場面に人手で確認した結果を紹介します。
Setterfieldの*Once Upon a River*（2018）はBennett論文の比較対象として本編で紹介します。
現時点で小説全文の分析入力はなく、4作品の共存率グラフには含めていません。
116語は、LLMの語単位判定と利用者・編集者の判断による114語に、利用者が承認した `wood`（自然）・`bridge`（人工）を加えた暫定リストです。
比喩的な用例があるという理由だけで語を落としません。
人による全語監査はまだ完了していません。

## Build

```sh
sh scripts/build.sh
```

`slides.md` が編集元、`index.html` が生成物です。スライドは縦に連続しており、
通常の縦スクロールにはsnapをかけません。左右矢印キーを押したときだけ、
前後のスライド先頭へ移動します。

語彙の選び方によって比較結果が変わるため、元の314語による集計も資料として
保存しています。今回の主な結果は116語で再計算した数値です。元の114語版も保存しています。

## Contents

- `slides.md`: 発表原稿
- `index.html`: 配布・GitHub Pages用HTML
- `readings/morris/annotated-reader/`: Morris『News from Nowhere』第2・10・23章の対訳読書稿
- `readings/hudson/annotated-reader/`: Hudson『A Crystal Age』第3・5・14章の対訳読書稿と家の模式図。スライドで引用する第2章は模式図ページに原文根拠を掲載し、対訳は未収録
- `assets/`: CSSと分析図
- `assets/scenes/`: 旧版で使った本文情景の生成イラスト
- `data/curated_*.csv`: 114語版の記録と採否判断
- `data/expanded_*.csv`: 116語版の語彙・作品別・章別・無作為化・Bennett事例の再集計
- `data/expanded_gutenberg_example_window.json`: スライド内で示す第10章の実例窓
- `colab/fixed_lexicon_demo.ipynb`: MorrisとHudsonの固定116語・50語窓を再計算するColab実演（[開く](https://colab.research.google.com/github/cm3/dh-literature-20261016/blob/main/colab/fixed_lexicon_demo.ipynb)）
- `colab/data/`: 実演用のProject Gutenberg未加工TXT2冊。出典と配布条件は[Colab説明](colab/README.md)に記載
- `scripts/build_gutenberg_charts.py`: Gutenberg版の図をCSVから再生成
- `data/work_summary.csv` など従来ファイル: 元の314語による集計
- `templates/`: Pandoc HTML template
- `scripts/build.sh`: 再生成スクリプト
- `scripts/recompute_expanded_metrics.py`: `wood`・`bridge` を加えた116語版をIA/PG両入力で再集計
- `scripts/analyze_setterfield.py`: 利用可能な全文TXTと章境界CSVを受け取り、同じ116語・50語窓で集計する準備済みツール。本文は成果物に複製しません。

## GitHub Pages用の配置

このリポジトリのルートを公開ディレクトリにすると、`index.html` から二つの読書稿へ相対リンクで移動できます。
読書稿のCSS・スクリプト・挿絵と、Morrisの写真の出典表示も `readings/` に同梱しました。
二つの読書稿は親プロジェクトの校訂済みHTMLから作った公開用スナップショットです。
Morrisの読書稿には46件の読書注、36枚の典拠つき資料画像、第10章の東ロンドンの位置関係を示す概略図を収録しています。舞台地図はLeafletとOpenStreetMapのオンライン配信を利用します。

- [スライド](index.html)
- [Morris第10章の対訳](readings/morris/annotated-reader/chapter-10.html)
- [Hudson対訳読書稿](readings/hudson/annotated-reader/index.html)
- [Hudson第2章の家の記述と模式図](readings/hudson/annotated-reader/landscape.html#house-exterior)

## Source analysis

114語の選定は親プロジェクトの
`work/nature-built-lexicon-review/scripts/recompute_mixing.py` で行った。
116語版のGutenberg・Internet Archive作品別・章別集計とInternet Archive版のBennett事例照合は
`scripts/recompute_expanded_metrics.py` による。Gutenberg版の13事例の補助的な位置照合は
`scripts/recompute_gutenberg_bennett_alignment.py` で再計算し、
`data/expanded_gutenberg_bennett_alignment.csv` とメタデータJSONに保存する。
IA版とGutenberg版の同じ引用範囲を章内の語列で対応づけ、位置と窓数を検証する。
シャッフル結果と実例窓は `scripts/recompute_gutenberg_metrics.py` による。
名詞判定・原形化と50語窓は `work/utopian-local-mixing-analysis/` のStage 2処理に合わせた。
論文の正しいDOIは
<https://doi.org/10.1080/14688417.2026.2733353>。

## Setterfieldの本文が入手できた場合

`scripts/analyze_setterfield.py` は本文全体を前後の資料を除いたUTF-8 TXT、
章境界を `chapter_number,start_character,end_character` 列のCSVとして受け取ります。
`--text`、`--chapters`、`--edition`、`--output` を指定します。
章境界CSVは本文の全範囲を隙間なく覆う必要があります。
本文・章境界のハッシュと、作品全体・章別の集計値だけをJSONに保存します。
MorrisのGutenberg本文を入力した検証では、116語版の220/3,047窓（7.22%）を再現します。
Setterfieldは時代・ジャンルの異なる現代作品のため、数値が得られても
同時代4作品と同一の群として順位付けせず、Bennettの二作品比較として示します。
