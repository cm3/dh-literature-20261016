"""Prepare 116-word Gutenberg permutation metrics and an exact example window."""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
CORPUS = ROOT / "work/utopian-text-corpus/corpus_alternatives"
REPO = ROOT / "repos/utopian-nature-built-talk"
STAGE = ROOT / "work/utopian-local-mixing-analysis/scripts/run_stage2.py"
FROZEN = ROOT / "work/nature-built-semantic-axis/semantic_axis/frozen_axis.json"
LEXICON = REPO / "data/expanded_lexicon.csv"
WORKS = (("news_from_nowhere", 3261), ("looking_backward", 624),
         ("erewhon", 1906), ("crystal_age", 7401))

spec = importlib.util.spec_from_file_location("stage2", STAGE)
stage2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage2)
stage2.ensure_nltk()
frozen = json.loads(FROZEN.read_text())
scores = pd.read_csv(ROOT / frozen["artifacts"]["vocabulary_scores"]["path"])
lookup = scores.set_index("lemma")[["polarity", "relevance"]].to_dict("index")
with LEXICON.open(newline="") as handle:
    lexicon = list(csv.DictReader(handle))
nature = {r["lemma"] for r in lexicon if r["semantic_class"] == "nature"}
built = {r["lemma"] for r in lexicon if r["semantic_class"] == "built"}
summaries = []
example = None

for work, pg_id in WORKS:
    stem = f"{work}_pg{pg_id}"
    body = (CORPUS / f"{stem}.txt").read_text()
    chapters = pd.read_csv(CORPUS / f"{stem}_chapters.csv")
    chapters["work"] = work
    frame = stage2.tokenize_work(work, body, lookup, frozen["thresholds"], chapters)
    labels = np.zeros(len(frame), dtype=np.int8)
    noun = frame["pos"].isin(["NN", "NNS"]).to_numpy()
    labels[noun & frame["lemma"].isin(nature).to_numpy()] = 1
    labels[noun & frame["lemma"].isin(built).to_numpy()] = -1
    starts = []
    for chapter, group in frame.groupby("chapter", sort=True):
        first, last = int(group.index.min()), int(group.index.max()) + 1
        starts.extend(range(first, last - 50 + 1, 25))
    starts = np.array(starts, dtype=int)
    ends = starts + 50
    def rate(values):
        n = np.r_[0, np.cumsum(values == 1)]
        b = np.r_[0, np.cumsum(values == -1)]
        return np.mean(((n[ends] - n[starts]) > 0) & ((b[ends] - b[starts]) > 0))
    observed = rate(labels)
    rng = np.random.default_rng(20261016)
    shuffled = np.array([rate(rng.permutation(labels)) for _ in range(1000)])
    summaries.append({"work": work, "observed_mixed_rate": observed,
                      "expected_mixed_rate": shuffled.mean(),
                      "q025": np.quantile(shuffled, 0.025),
                      "q975": np.quantile(shuffled, 0.975),
                      "permutations": 1000, "seed": 20261016})
    if work == "news_from_nowhere":
        for start in starts:
            part = frame.iloc[start:start+50]
            n = set(part.loc[labels[start:start+50] == 1, "lemma"])
            b = set(part.loc[labels[start:start+50] == -1, "lemma"])
            if "river" in n and "meadow" in n and "house" in b and int(part.iloc[0]["chapter"]) == 10:
                example = {"work": work, "chapter": 10, "window_start": int(start),
                           "window_end": int(start+50), "text": body[int(part.iloc[0]["char_start"]):int(part.iloc[-1]["char_end"])],
                           "tokens": [{"surface": row.surface, "lemma": row.lemma,
                                       "label": int(labels[start+i])}
                                      for i, row in enumerate(part.itertuples(index=False))]}
                break
    print(work, len(frame), len(starts), observed, shuffled.mean(), flush=True)

pd.DataFrame(summaries).to_csv(REPO / "data/expanded_gutenberg_permutation_summary.csv", index=False)
(REPO / "data/expanded_gutenberg_example_window.json").write_text(json.dumps(example, indent=2) + "\n")
print("example", json.dumps(example, ensure_ascii=False)[:1800])
