# Utopian Nature–Built Talk

約10分のHTMLスライドです。Bennett (2026) の *News from Nowhere* 読解を
4作品のNature–Built local mixing、Morrisの全32章、13場面の直接照合によって
検証します。章別監査と *A Crystal Age* の6例は縦に読める長い証拠スライドです。

## Build

```sh
sh scripts/build.sh
```

`slides.md` が編集元、`index.html` が生成物です。スライドは縦に連続しており、
通常の縦スクロールにはsnapをかけません。左右矢印キーを押したときだけ、
前後のスライド先頭へ移動します。

## Contents

- `slides.md`: 発表原稿
- `index.html`: 配布・GitHub Pages用HTML
- `assets/`: CSSと分析図
- `data/`: work-level集計、permutation集計、Morris章別集計、Bennett照合表
- `templates/`: Pandoc HTML template
- `scripts/build.sh`: 再生成スクリプト

## Source analysis

このdeckは親プロジェクトの
`work/utopian-local-mixing-analysis/` にあるStage 2成果物から作成した。
論文の正しいDOIは
<https://doi.org/10.1080/14688417.2026.2733353>。
