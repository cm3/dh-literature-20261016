#!/usr/bin/env python3
"""Recount IA/PG texts with the user-approved wood/bridge additions.

The original 114-word files remain intact. This script creates a documented
116-word lexicon, four-work summaries, and the IA Bennett alignment.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data"
TEXTS = ROOT / "work/utopian-text-corpus"
STAGE = ROOT / "work/utopian-local-mixing-analysis/scripts/run_stage2.py"
COMPARISON = ROOT / "work/nature-built-lexicon-review/scripts/compare_gutenberg_all.py"
FROZEN = ROOT / "work/nature-built-semantic-axis/semantic_axis/frozen_axis.json"
TOKENS = ROOT / "work/utopian-local-mixing-analysis/results/token_scores.csv.gz"
WORKS = (("news_from_nowhere", 3261), ("looking_backward", 624),
         ("erewhon", 1906), ("crystal_age", 7401))
WIDTH = 50
STEP = 25


def module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_lexicon() -> Path:
    base = DATA / "curated_lexicon.csv"
    output = DATA / "expanded_lexicon.csv"
    with base.open(newline="", encoding="utf-8") as stream:
        source = csv.DictReader(stream)
        rows = list(source)
        columns = source.fieldnames
    if len(rows) != 114 or {row["lemma"] for row in rows} & {"wood", "bridge"}:
        raise ValueError("Expected the unchanged 114-word source list")
    frequencies = {"wood": 0, "bridge": 0}
    with gzip.open(TOKENS, "rt", newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            if row["pos"] in ("NN", "NNS") and row["lemma"] in frequencies:
                frequencies[row["lemma"]] += 1
    for lemma, category, rule in (
        ("wood", "nature", "User-approved addition; woodland sense in NFN-07; timber senses remain a limitation"),
        ("bridge", "built", "User-approved addition; physical bridge in NFN-13"),
    ):
        rows.append({"lemma": lemma, "semantic_class": category,
                     "combined_frequency": frequencies[lemma],
                     "llm_lemma_label": "", "llm_context_labels": "",
                     "source": "user-approved addition, 2026-10-16", "rule": rule})
    rows.sort(key=lambda row: row["lemma"])
    with output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)
    return output


def case_alignment(nature: set[str], built: set[str]) -> pd.DataFrame:
    # Preserve the original IA case offsets and 50/25-window boundaries.
    frame = pd.read_csv(TOKENS, keep_default_na=False)
    frame = frame[frame["work"] == "news_from_nowhere"].reset_index(drop=True)
    frozen_windows = pd.read_csv(
        ROOT / "work/utopian-local-mixing-analysis/results/windows_main.csv",
        keep_default_na=False)
    frozen_windows = frozen_windows[frozen_windows["work"] == "news_from_nowhere"]
    noun = frame["pos"].isin(["NN", "NNS"])
    labels = np.zeros(len(frame), dtype=np.int8)
    labels[noun & frame["lemma"].isin(nature)] = 1
    labels[noun & frame["lemma"].isin(built)] = -1
    windows = []
    for _, frozen_window in frozen_windows.iterrows():
        start, end = int(frozen_window["window_start"]), int(frozen_window["window_end"])
        part = frame.iloc[start:end]
        n_terms = sorted(set(part.loc[labels[start:end] == 1, "lemma"]))
        b_terms = sorted(set(part.loc[labels[start:end] == -1, "lemma"]))
        windows.append({"window_start": start, "window_end": end,
                        "char_start": int(frozen_window["char_start"]),
                        "char_end": int(frozen_window["char_end"]),
                        "nature_terms": n_terms, "built_terms": b_terms})
    cases = pd.read_csv(DATA / "bennett_2026_nfn_alignment.csv", keep_default_na=False)
    output = []
    for _, case in cases.iterrows():
        overlap = [w for w in windows if w["char_start"] < int(case["char_end"])
                   and w["char_end"] > int(case["char_start"])]
        hits = [w for w in overlap if w["nature_terms"] and w["built_terms"]]
        output.append({"case_id": case["case_id"], "label": case["label"],
                       "article_page": case["article_page"],
                       "overlap_windows": len(overlap), "mixed_windows": len(hits),
                       "nature_terms": "|".join(sorted({term for w in hits for term in w["nature_terms"]})),
                       "built_terms": "|".join(sorted({term for w in hits for term in w["built_terms"]})),
                       "prior_manual_classification": case["manual_classification"]})
    return pd.DataFrame(output)


def main() -> None:
    lexicon = make_lexicon()
    comparison = module(COMPARISON, "expanded_comparison")
    stage2 = module(STAGE, "expanded_stage2")
    stage2.ensure_nltk()
    nature, built = comparison.categories(lexicon)
    if len(nature) != 56 or len(built) != 60:
        raise ValueError("Expected 56 nature and 60 built lemmas")
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    scores = pd.read_csv(ROOT / frozen["artifacts"]["vocabulary_scores"]["path"])
    lookup = scores.set_index("lemma")[["polarity", "relevance"]].to_dict("index")
    ia_chapters = pd.read_csv(TEXTS / "metadata/chapters.csv")
    works = pd.read_csv(TEXTS / "metadata/works.csv").set_index("id")
    summaries, chapters, inputs = [], [], []
    for work, pg_id in WORKS:
        ia_path = TEXTS / "corpus" / works.loc[work, "planned_corpus_filename"]
        ia = stage2.tokenize_work(work, ia_path.read_text(encoding="utf-8"),
                                  lookup, frozen["thresholds"], ia_chapters)
        pg_stem = f"{work}_pg{pg_id}"
        pg_path = TEXTS / "corpus_alternatives" / f"{pg_stem}.txt"
        pg_chapters_path = TEXTS / "corpus_alternatives" / f"{pg_stem}_chapters.csv"
        pg_chapters = pd.read_csv(pg_chapters_path)
        pg_chapters["work"] = work
        pg = stage2.tokenize_work(work, pg_path.read_text(encoding="utf-8"),
                                  lookup, frozen["thresholds"], pg_chapters)
        for source, tokens in (("IA", ia), ("PG", pg)):
            summary, by_chapter = comparison.window_summary(tokens, nature, built, "lexical_116")
            summaries.append({"work": work, "source": source, **summary})
            chapters.extend({"work": work, "source": source, "vocabulary": "lexical_116", **row}
                            for row in by_chapter)
        if work == "news_from_nowhere":
            case_alignment(nature, built).to_csv(DATA / "expanded_bennett_alignment.csv", index=False)
        inputs.append({"work": work, "ia_sha256": sha(ia_path), "pg_sha256": sha(pg_path),
                       "pg_chapters_sha256": sha(pg_chapters_path)})
        print(work, summaries[-1]["mixed_windows"], summaries[-1]["window_count"], flush=True)
    pd.DataFrame(summaries).to_csv(DATA / "expanded_gutenberg_work_summary.csv", index=False)
    pd.DataFrame(chapters).to_csv(DATA / "expanded_gutenberg_chapter_summary.csv", index=False)
    metadata = {"schema": "expanded-nature-built.v1", "vocabulary": "lexical_116",
                "additions": {"nature": ["wood"], "built": ["bridge"]},
                "baseline_lexicon_sha256": sha(DATA / "curated_lexicon.csv"),
                "expanded_lexicon_sha256": sha(lexicon),
                "width": WIDTH, "step": STEP, "inputs": inputs}
    (DATA / "expanded_run_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
