#!/usr/bin/env python3
"""Locate Bennett's 13 IA passages in Gutenberg and recount the 116-word windows."""

from __future__ import annotations

import bisect
import csv
import difflib
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

from recompute_expanded_metrics import COMPARISON, DATA, FROZEN, ROOT, STAGE, TEXTS, module


WORK = "news_from_nowhere"
PG_STEM = "news_from_nowhere_pg3261"
WORD = re.compile(r"[A-Za-z]+")
WIDTH = 50
STEP = 25


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(text: str, chapter: dict[str, str]) -> list[tuple[str, int, int]]:
    first, last = int(chapter["start_character"]), int(chapter["end_character"])
    return [(match.group().casefold(), first + match.start(), first + match.end())
            for match in WORD.finditer(text[first:last])]


def word_index(items: list[tuple[str, int, int]], offset: int, boundary: str) -> int:
    if boundary == "start":
        return bisect.bisect_right([item[2] for item in items], offset)
    return bisect.bisect_left([item[1] for item in items], offset) - 1


def mapped_index(index: int, mapping: dict[int, int], pg_length: int) -> tuple[int, bool]:
    if index in mapping:
        return mapping[index], True
    neighbors = sorted(mapping, key=lambda candidate: abs(candidate - index))[:2]
    if not neighbors or abs(neighbors[0] - index) > 5:
        raise ValueError(f"No close alignment for word {index}")
    estimates = [mapping[neighbor] + index - neighbor for neighbor in neighbors]
    if len(estimates) == 2 and abs(estimates[0] - estimates[1]) > 2:
        raise ValueError(f"Ambiguous alignment for word {index}: {estimates}")
    target = round(sum(estimates) / len(estimates))
    if not 0 <= target < pg_length:
        raise ValueError(f"Mapped word outside Gutenberg chapter: {target}")
    return target, False


def aligned_cases(ia_text: str, pg_text: str) -> list[dict[str, object]]:
    ia_chapters = {
        int(row["chapter_number"]): row for row in csv.DictReader(
            (TEXTS / "metadata/chapters.csv").open(newline="", encoding="utf-8"))
        if row["work"] == WORK
    }
    pg_chapters = {
        int(row["chapter_number"]): row for row in csv.DictReader(
            (TEXTS / "corpus_alternatives" / f"{PG_STEM}_chapters.csv").open(
                newline="", encoding="utf-8"))
    }
    cases = list(csv.DictReader((DATA / "bennett_2026_nfn_alignment.csv").open(
        newline="", encoding="utf-8")))
    chapter_cache: dict[int, tuple[list[tuple[str, int, int]],
                                   list[tuple[str, int, int]], dict[int, int]]] = {}
    output = []
    for case in cases:
        ia_start, ia_end = int(case["char_start"]), int(case["char_end"])
        chapter = next(number for number, row in ia_chapters.items()
                       if int(row["start_character"]) <= ia_start < ia_end
                       <= int(row["end_character"]))
        if chapter not in chapter_cache:
            ia_words = words(ia_text, ia_chapters[chapter])
            pg_words = words(pg_text, pg_chapters[chapter])
            matcher = difflib.SequenceMatcher(
                None, [item[0] for item in ia_words], [item[0] for item in pg_words],
                autojunk=False)
            mapping = {block.a + i: block.b + i
                       for block in matcher.get_matching_blocks() for i in range(block.size)}
            if len(mapping) / len(ia_words) < 0.95:
                raise ValueError(f"Insufficient chapter alignment for chapter {chapter}")
            chapter_cache[chapter] = ia_words, pg_words, mapping
        ia_words, pg_words, mapping = chapter_cache[chapter]
        first_ia = word_index(ia_words, ia_start, "start")
        last_ia = word_index(ia_words, ia_end, "end")
        first_pg, start_exact = mapped_index(first_ia, mapping, len(pg_words))
        last_pg, end_exact = mapped_index(last_ia, mapping, len(pg_words))
        if not first_pg <= last_pg:
            raise ValueError(f"Reversed passage for {case['case_id']}")
        similarity = difflib.SequenceMatcher(
            None, [item[0] for item in ia_words[first_ia:last_ia + 1]],
            [item[0] for item in pg_words[first_pg:last_pg + 1]],
            autojunk=False).ratio()
        if similarity < 0.9:
            raise ValueError(f"Low passage similarity for {case['case_id']}: {similarity:.3f}")
        output.append({
            "case_id": case["case_id"], "label": case["label"],
            "article_page": int(case["article_page"]), "chapter": chapter,
            "pg_char_start": pg_words[first_pg][1], "pg_char_end": pg_words[last_pg][2],
            "alignment_similarity": round(similarity, 4),
            "start_boundary_exact": start_exact, "end_boundary_exact": end_exact,
            "prior_manual_classification": case["manual_classification"],
        })
    if len(output) != 13:
        raise ValueError(f"Expected 13 Bennett cases, found {len(output)}")
    return output


def main() -> None:
    works = pd.read_csv(TEXTS / "metadata/works.csv").set_index("id")
    ia_path = TEXTS / "corpus" / works.loc[WORK, "planned_corpus_filename"]
    pg_path = TEXTS / "corpus_alternatives" / f"{PG_STEM}.txt"
    ia_text, pg_text = ia_path.read_text(encoding="utf-8"), pg_path.read_text(encoding="utf-8")
    cases = aligned_cases(ia_text, pg_text)

    stage2 = module(STAGE, "pg_bennett_stage2")
    comparison = module(COMPARISON, "pg_bennett_comparison")
    stage2.ensure_nltk()
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    scores = pd.read_csv(ROOT / frozen["artifacts"]["vocabulary_scores"]["path"])
    lookup = scores.set_index("lemma")[["polarity", "relevance"]].to_dict("index")
    chapters = pd.read_csv(TEXTS / "corpus_alternatives" / f"{PG_STEM}_chapters.csv")
    chapters["work"] = WORK
    tokens = stage2.tokenize_work(WORK, pg_text, lookup, frozen["thresholds"], chapters)
    nature, built = comparison.categories(DATA / "expanded_lexicon.csv")
    summary, _ = comparison.window_summary(tokens, nature, built, "lexical_116")
    published = pd.read_csv(DATA / "expanded_gutenberg_work_summary.csv")
    expected = published[(published["work"] == WORK) & (published["source"] == "PG")].iloc[0]
    if (summary["window_count"], summary["mixed_windows"]) != (
            int(expected["window_count"]), int(expected["mixed_windows"])):
        raise ValueError("Gutenberg window totals differ from the published 116-word run")

    noun = tokens["pos"].isin(["NN", "NNS"]).to_numpy()
    n_labels = noun & tokens["lemma"].isin(nature).to_numpy()
    b_labels = noun & tokens["lemma"].isin(built).to_numpy()
    windows: dict[int, list[dict[str, object]]] = {}
    for chapter, group in tokens.groupby("chapter", sort=True):
        first, last = int(group.index.min()), int(group.index.max()) + 1
        records = []
        for start in range(first, last - WIDTH + 1, STEP):
            end = start + WIDTH
            records.append({
                "char_start": int(tokens.iloc[start]["char_start"]),
                "char_end": int(tokens.iloc[end - 1]["char_end"]),
                "nature_terms": sorted(set(tokens.iloc[start:end].loc[n_labels[start:end], "lemma"])),
                "built_terms": sorted(set(tokens.iloc[start:end].loc[b_labels[start:end], "lemma"])),
            })
        windows[int(chapter)] = records

    for case in cases:
        overlap = [window for window in windows[case["chapter"]]
                   if window["char_start"] < case["pg_char_end"]
                   and window["char_end"] > case["pg_char_start"]]
        hits = [window for window in overlap
                if window["nature_terms"] and window["built_terms"]]
        case.update({
            "source": "PG", "vocabulary": "lexical_116",
            "overlap_windows": len(overlap), "mixed_windows": len(hits),
            "nature_terms": "|".join(sorted({term for hit in hits for term in hit["nature_terms"]})),
            "built_terms": "|".join(sorted({term for hit in hits for term in hit["built_terms"]})),
        })

    destination = DATA / "expanded_gutenberg_bennett_alignment.csv"
    pd.DataFrame(cases).to_csv(destination, index=False)
    metadata = {
        "source": "Project Gutenberg #3261", "vocabulary": "lexical_116",
        "width": WIDTH, "step": STEP,
        "passage_mapping": "IA and Gutenberg chapter word sequences aligned with difflib; mapped case boundaries checked by passage similarity",
        "ia_sha256": sha(ia_path), "pg_sha256": sha(pg_path),
        "lexicon_sha256": sha(DATA / "expanded_lexicon.csv"),
        "case_source_sha256": sha(DATA / "bennett_2026_nfn_alignment.csv"),
        "minimum_passage_similarity": min(case["alignment_similarity"] for case in cases),
        "exact_start_boundaries": sum(case["start_boundary_exact"] for case in cases),
        "exact_end_boundaries": sum(case["end_boundary_exact"] for case in cases),
    }
    (DATA / "expanded_gutenberg_bennett_alignment_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {destination} ({len(cases)} cases)")


if __name__ == "__main__":
    main()
