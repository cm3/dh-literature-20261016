#!/usr/bin/env python3
"""Render the Gutenberg-input charts from the slide repository's frozen CSVs."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
WORKS = ["news_from_nowhere", "looking_backward", "erewhon", "crystal_age"]
TITLES = ["News from Nowhere", "Looking Backward", "Erewhon", "A Crystal Age"]

work = pd.read_csv(DATA / "expanded_gutenberg_work_summary.csv")
work = work[(work.source == "PG") & (work.vocabulary == "lexical_116")].set_index("work").loc[WORKS]
null = pd.read_csv(DATA / "expanded_gutenberg_permutation_summary.csv").set_index("work").loc[WORKS]
x = np.arange(len(WORKS))

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].bar(x - .18, work.nature_tokens / work.token_count * 1000, .36, label="Nature", color="#4C956C")
axes[0].bar(x + .18, work.built_tokens / work.token_count * 1000, .36, label="Built", color="#577590")
axes[0].set_ylabel("retained tokens per 1,000 words")
axes[0].legend()
axes[1].bar(x, work.mixed_rate, color="#B56576")
axes[1].set_ylabel("50-word mixed-window rate")
axes[1].yaxis.set_major_formatter(PercentFormatter(1))
for ax in axes:
    ax.set_xticks(x, TITLES, rotation=20, ha="right")
fig.tight_layout()
fig.savefig(ASSETS / "gutenberg_work_densities_and_mixing.png", dpi=180)
plt.close(fig)

fig, ax = plt.subplots(figsize=(13, 3.2))
ax.bar(x - .18, null.observed_mixed_rate, .36, label="Observed", color="#B56576")
ax.bar(x + .18, null.expected_mixed_rate, .36, label="Global-shuffle expected", color="#90A4AE")
ax.errorbar(x + .18, null.expected_mixed_rate,
            yerr=[null.expected_mixed_rate - null.q025, null.q975 - null.expected_mixed_rate],
            fmt="none", color="black", capsize=3)
ax.set_xticks(x, ("Morris", "Bellamy", "Butler", "Hudson"))
ax.set_ylabel("mixed-window rate")
ax.yaxis.set_major_formatter(PercentFormatter(1))
ax.legend()
fig.tight_layout()
fig.savefig(ASSETS / "gutenberg_observed_vs_expected.png", dpi=180)
plt.close(fig)
