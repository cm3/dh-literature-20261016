#!/usr/bin/env python3
"""Count a locally supplied Once Upon a River text with the talk's fixed lexicon.

Input must be a cleaned UTF-8 TXT of the novel and a CSV of chapter boundaries.
The novel text stays at the caller's path; only aggregate results are written.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
REPO = Path(__file__).resolve().parents[1]
WORK = "setterfield_once_upon_a_river"
STAGE = ROOT / "work/utopian-local-mixing-analysis/scripts/run_stage2.py"
COMPARISON = ROOT / "work/nature-built-lexicon-review/scripts/compare_gutenberg_all.py"
FROZEN = ROOT / "work/nature-built-semantic-axis/semantic_axis/frozen_axis.json"
LEXICON = REPO / "data/expanded_lexicon.csv"


def module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text", required=True, type=Path, help="Clean UTF-8 novel text (not an excerpt)")
    parser.add_argument("--chapters", required=True, type=Path,
                        help="CSV: chapter_number,start_character,end_character")
    parser.add_argument("--output", required=True, type=Path, help="Aggregate JSON output")
    parser.add_argument("--edition", required=True, help="Edition / publisher / year for provenance")
    args = parser.parse_args()

    body = args.text.read_text(encoding="utf-8-sig")
    chapters = pd.read_csv(args.chapters)
    required = {"chapter_number", "start_character", "end_character"}
    if not required <= set(chapters.columns):
        parser.error(f"Chapter CSV needs columns: {', '.join(sorted(required))}")
    chapters = chapters.sort_values("chapter_number").copy()
    numbers = chapters["chapter_number"].astype(int).tolist()
    starts = chapters["start_character"].astype(int).tolist()
    ends = chapters["end_character"].astype(int).tolist()
    if (not numbers or numbers != list(range(1, len(numbers) + 1))
            or starts[0] != 0 or ends[-1] != len(body)
            or any(end != next_start for end, next_start in zip(ends, starts[1:]))
            or any(start >= end for start, end in zip(starts, ends))):
        parser.error("Chapter offsets must cover the entire text, contiguously, in chapter order")
    chapters["work"] = WORK

    stage2 = module(STAGE, "stage2_setterfield")
    comparison = module(COMPARISON, "comparison_setterfield")
    stage2.ensure_nltk()
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    scores = pd.read_csv(ROOT / frozen["artifacts"]["vocabulary_scores"]["path"])
    lookup = scores.set_index("lemma")[["polarity", "relevance"]].to_dict("index")
    nature, built = comparison.categories(LEXICON)
    tokens = stage2.tokenize_work(WORK, body, lookup, frozen["thresholds"], chapters)
    summary, by_chapter = comparison.window_summary(tokens, nature, built, "lexical_116")
    result = {
        "schema": "setterfield-lexical-116.v1",
        "work": WORK,
        "title": "Once Upon a River",
        "edition": args.edition,
        "method": "NLTK noun lemma (NN/NNS); fixed 116-word lexicon; 50-token windows, step 25, within chapters",
        "text_sha256": sha256(args.text),
        "chapters_sha256": sha256(args.chapters),
        "lexicon_sha256": sha256(LEXICON),
        "summary": summary,
        "chapters": by_chapter,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{summary['mixed_windows']}/{summary['window_count']} mixed windows "
          f"({summary['mixed_rate']:.2%}); {summary['token_count']} tokens")


if __name__ == "__main__":
    main()
