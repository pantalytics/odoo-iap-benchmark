#!/usr/bin/env python3
# Copyright 2026 Pantalytics B.V.
# SPDX-License-Identifier: Apache-2.0
"""Social figure, 2D: accuracy against cost per bill, readable on a phone.

Usage:
    python src/fig_social_2d.py results figures

Same numbers as figure 0, in 4:5 portrait (1080 x 1350 px) with large type.
Writes figures/social_overview.png and .svg.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, NullLocator

from aggregate import ODOO_CREDIT_EUR, ODOO_CREDIT_EUR_BULK
from fig_overview import points
from figures import GRID, INK, LLM, MUTED, ODOO

plt.rcParams.update({"font.family": ["Inter", "Helvetica Neue", "DejaVu Sans"],
                     "savefig.bbox": "standard"})  # fixed 1080 x 1350, no tight crop

# Label offsets in points (dx, dy, ha); the models sit in one tight cluster.
PLACE = {  # four of the eight models, one per vendor plus the cheapest strong one
    "Claude Opus 5.5": (-10, 0, "right"),
    "Claude Sonnet 5.5": (0, 15, "center"),
    "GPT-5.5": (-10, 0, "right"),
    "Gemini 3.8 Flash": (10, -17, "right"),
}


def main() -> None:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    pts = [p for p in points(root) if p[0] == "Odoo" or p[0] in PLACE]

    fig = plt.figure(figsize=(5.4, 6.75), dpi=200)
    ax = fig.add_axes((0.13, 0.15, 0.82, 0.62))
    for name, cost, book in pts:
        if name == "Odoo":
            ax.plot([ODOO_CREDIT_EUR, ODOO_CREDIT_EUR_BULK], [book, book], color=ODOO, lw=5,
                    solid_capstyle="round", zorder=2)  # fmt: skip
            ax.annotate(f"Odoo IAP  {book:.0f}%\n€0.05 to 0.15 per bill",
                        (ODOO_CREDIT_EUR_BULK, book), xytext=(-4, 14), textcoords="offset points",
                        ha="center", va="bottom", fontsize=11, fontweight="bold", color=INK,
                        linespacing=1.3)  # fmt: skip
            continue
        ax.scatter(cost, book, s=110, color=LLM, edgecolor="white", lw=1.5, zorder=3)
        dx, dy, ha = PLACE[name]
        ax.annotate(f"{name} {book:.0f}%", (cost, book), xytext=(dx, dy),
                    textcoords="offset points", ha=ha, va="center", fontsize=10,
                    color=INK)  # fmt: skip

    ax.set_xscale("log")
    ax.set_xlim(0.25, 0.0035)  # inverted: cheaper to the right
    ticks = [0.005, 0.01, 0.02, 0.05, 0.1]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xticklabels([f"€{t:g}" for t in ticks])
    ax.set_xlabel("Cost per bill (cheaper →)", fontsize=9.5, color=MUTED, labelpad=8)
    ax.set_ylim(0, 105)
    ax.set_yticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100%"])
    ax.set_ylabel("Bills read without errors", fontsize=9.5, color=MUTED, labelpad=6)
    ax.tick_params(length=0, labelsize=9)
    ax.grid(color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_visible(False)

    fig.text(0.05, 0.955, "We compared Odoo IAP with LLMs.\nThis is the result.",
             fontsize=19, fontweight="bold", color=INK, va="top", linespacing=1.15)  # fmt: skip
    fig.text(0.05, 0.835, "Better is top right", fontsize=11.5, color=MUTED, va="top")
    fig.text(0.05, 0.035, "223 public test bills. 4 of 8 models shown. Odoo before supplier matching.\n"
             "github.com/pantalytics/odoo-iap-benchmark",
             fontsize=8, color=MUTED, va="bottom", linespacing=1.4)  # fmt: skip
    fig.savefig(out / "social_overview.png", dpi=200, facecolor="white", bbox_inches=None)
    fig.savefig(out / "social_overview.svg", facecolor="white", bbox_inches=None)


if __name__ == "__main__":
    main()
