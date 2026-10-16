# Colab実演

[ノートブックをColabで開く](https://colab.research.google.com/github/cm3/dh-literature-20261016/blob/main/colab/fixed_lexicon_demo.ipynb)

Morris『*News from Nowhere*』とHudson『*A Crystal Age*』の2作品について、固定116語と50語窓・25語移動の共存率を再計算します。PythonとNLTK 3.10.3を使い、ノートブック内で2冊の原版テキストから章本文を切り出します。結果はスライドのMorris 220/3,047窓（7.22%）、Hudson 190/2,323窓（8.18%）と一致するよう検証します。

配布したProject Gutenbergの未加工TXTは以下の2ファイルです。ライセンス全文を含み、バイト列を変更していません。研究用の整形テキストはノートブック実行時に作ります。入力のSHA-256と整形後本文のSHA-256はノートブック内で照合します。`data/expanded_lexicon.csv` が語彙入力です。

- `data/news_from_nowhere_pg3261.txt`: [Project Gutenberg eBook #3261](https://www.gutenberg.org/ebooks/3261)。転写の底本は1908年刊本。
- `data/crystal_age_pg7401.txt`: [Project Gutenberg eBook #7401](https://www.gutenberg.org/ebooks/7401)。改訂版系統の本文。

Project Gutenbergの配布条件： “This eBook is for the use of anyone anywhere in the United States and most other parts of the world at no cost and with almost no restrictions whatsoever. You may copy it, give it away or re-use it under the terms of the Project Gutenberg License included with this eBook or online at www.gutenberg.org.” [ライセンス全文](https://www.gutenberg.org/policy/license)

ノートブックは本文の準備、名詞の品詞判定と原形化、共存窓の集計、章別図、本文例、窓長の変更を順に示します。Bennettの13場面の9/13は別条件の人手判定なので、ここでは再計算しません。
