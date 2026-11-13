#!/usr/bin/env python3
# Copyright 2026 Pantalytics B.V.
# SPDX-License-Identifier: Apache-2.0
"""Figure 0: the one-picture answer. Accuracy against price, per engine.

Usage:
    python src/fig_overview.py results figures

y: share of documents bookable without correction, the mean of the three
sets (each set weighs the same). x: AI cost per document, log scale. Odoo is
a range, from its largest to its smallest credit pack. Writes
figures/fig0_overview.png and .svg.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FixedLocator, NullLocator  # noqa: E402

from aggregate import ODOO_CREDIT_EUR, ODOO_CREDIT_EUR_BULK, USD_EUR  # noqa: E402
from figures import GRID, INK, LLM, MUTED, NAMES, ODOO, SETS, load, mean, save  # noqa: E402

RULES = "gemini-flash"  # the H3 arm shown as its own point
PLACE = {
    "Gemini 3.8 Flash + 4 rules": (0, 11, "center"),
    "GPT-5.5": (6, 9, "left"),
    "Gemini 2.5 Pro": (6, -10, "left"),
    "GPT-5.6 Terra": (0, -12, "center"),
    "Mistral OCR + Medium": (-8, 0, "right"),
    "Claude Sonnet 5.5": (0, -11, "center"),
}


def points(root: Path) -> list[tuple[str, float, float]]:
    """(label, EUR per document, mean bookable %) per engine, plus the H3 arm."""
    out = []
    per_set = {key: load(root, key) for key, _ in SETS}
    for e, name in NAMES.items():
        books, costs = [], []
        for runs in per_set.values():
            m = mean(runs, e, "book", "book_n")
            if m is None:
                break
            books.append(m)
            costs.append(sum(r[e]["cost"] / r[e]["docs"] for r in runs if e in r) / len(runs))
        if len(books) == len(SETS):
            cost = ODOO_CREDIT_EUR if e == "odoo" else sum(costs) / len(costs) / 0.86 * USD_EUR
            out.append((name, cost, 100 * sum(books) / len(books)))
    h3 = [json.loads((root / k / "h3" / "summary.json").read_text()) for k, _ in SETS]
    if all(RULES in s for s in h3):
        book = sum(s[RULES]["book"] / s[RULES]["book_n"] for s in h3) / len(h3)
        cost = sum(s[RULES]["cost"] / s[RULES]["docs"] for s in h3) / len(h3) / 0.86 * USD_EUR
        out.append((f"{NAMES[RULES]} + 4 rules", cost, 100 * book))
    return out


def main() -> None:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    pts = points(root)
    fig, ax = plt.subplots(figsize=(8, 5.2))
    for name, cost, book in pts:
        if name == "Odoo":
            ax.plot([ODOO_CREDIT_EUR_BULK, ODOO_CREDIT_EUR], [book, book], color=ODOO, lw=3,
                    solid_capstyle="round", zorder=2)  # fmt: skip
            for x in (ODOO_CREDIT_EUR_BULK, ODOO_CREDIT_EUR):
                ax.scatter(x, book, marker="D", s=70, color=ODOO, edgecolor="white", lw=2, zorder=3)
            ax.annotate("Odoo digitization\nEUR 0.05 to 0.15, by credit pack",
                        (ODOO_CREDIT_EUR_BULK, book), xytext=(0, 12), textcoords="offset points",
                        ha="left", fontsize=9.5, fontweight="bold", color=INK)  # fmt: skip
            continue
        rules = name.endswith("rules")
        ax.scatter(cost, book, s=70, marker="s" if rules else "o", color=LLM,
                   edgecolor="white", lw=2, zorder=3)  # fmt: skip
    # The models sit in one tight cluster; each label is placed by hand so none
    # overlaps (offset in points, horizontal alignment). Unknown names go right.
    for name, cost, book in pts:
        if name != "Odoo":
            dx, dy, ha = PLACE.get(name, (8, 0, "left"))
            ax.annotate(f"{name}  {book:.0f}%", (cost, book), xytext=(dx, dy),
                        textcoords="offset points", ha=ha, va="center", fontsize=8.5,
                        color=INK)  # fmt: skip
    ax.set_xscale("log")
    ax.set_xlim(0.0022, 0.4)
    ticks = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xticklabels([f"{t:g}" for t in ticks])
    ax.set_xlabel("AI cost per document, EUR (log scale)")
    ax.set_ylim(0, 105)
    ax.set_yticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100%"])
    ax.grid(color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    ax.annotate("better ↑", (0.0025, 62), fontsize=8.5, color=MUTED, ha="left")
    ax.annotate("cheaper ←", (0.0025, 3), fontsize=8.5, color=MUTED, ha="left")
    fig.suptitle("Bills bookable without correction, against what reading one costs",
                 x=0.01, ha="left", fontsize=13, fontweight="bold", color=INK)  # fmt: skip
    ax.set_title("Mean of three public test sets (223 documents): Donut invoices, EN 16931 "
                 "invoices, SROIE receipts", loc="left", fontsize=9, color=MUTED)  # fmt: skip
    fig.tight_layout()
    save(fig, out, "fig0_overview")
    for p in sorted(pts, key=lambda p: -p[2]):
        print(f"{p[0]:32} {p[1]:.4f} {p[2]:.1f}")


if __name__ == "__main__":
    main()
