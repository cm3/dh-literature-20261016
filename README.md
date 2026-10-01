# Utopian Nature–Built Talk

約10分のHTMLスライドです。4作品のNature–Built local mixing分析と、
Bennett (2026) が論じる *News from Nowhere* の13場面との照合をまとめます。

## Build

```sh
sh scripts/build.sh
```

`slides.md` が編集元、`index.html` が生成物です。ブラウザでは
`index.html?present=1` を開くとscroll snapが強制され、矢印キーまたは
Page Up / Page Downで移動できます。

## Contents

- `slides.md`: 発表原稿
- `index.html`: 配布・GitHub Pages用HTML
- `assets/`: CSSと分析図
- `data/`: work-level集計、permutation集計、Bennett照合表
- `templates/`: Pandoc HTML template
- `scripts/build.sh`: 再生成スクリプト

## Source analysis

このdeckは親プロジェクトの
`work/utopian-local-mixing-analysis/` にあるStage 2成果物から作成した。
論文の正しいDOIは
<https://doi.org/10.1080/14688417.2026.2733353>。
