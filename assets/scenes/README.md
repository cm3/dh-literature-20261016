# Scene backgrounds

第8節 *News from Nowhere: local evidence* と第9節 *Comparative counterexample* の
事例カード背景。いずれも本文記述を視覚化するため、OpenAIの組み込み画像生成を
使用して2026-10-01に生成した。史料画像や原著挿絵ではない。

## Common prompt direction

- use case: `historical-scene`
- academic HTML presentation card background
- restrained nineteenth-century wood engraving with muted watercolor wash
- wide composition、低彩度、文字を重ねられる穏やかな中央部
- no text、no watermark、no border、no modern objects

## Files

- `nfn-industrial-decay.png`: 荒廃する産業地区、家屋、工場、伐採木。
- `nfn-old-house-river.png`: Thames、草地、庭、花と開かれた古い家。
- `nfn-museum-trees.png`: 柵を失ったMuseum、樹木、建築を飛び交う鳩。
- `crystal-ocean-rooms.png`: 海・潮・砂・海鳥が室内へ響くHouse of Coradine。
- `crystal-artificial-flowers.png`: 金属・木・石に固定された人工花の室内装飾。

CSSで暗いgradient overlayを重ね、投影時の本文可読性を確保する。
