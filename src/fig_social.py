#!/usr/bin/env python3
# Copyright 2026 Pantalytics B.V.
# SPDX-License-Identifier: Apache-2.0
"""Social figure: one message, readable on a phone. For LinkedIn and the Odoo forum.

Usage:
    python src/fig_social.py results figures

Same numbers as figure 0 (mean bookable share of the three sets, AI cost per
document), drawn as sorted bars with the conclusion in the title. 4:5 portrait,
1080 x 1350 px. Writes figures/social_bookable.png and .svg.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

from aggregate import ODOO_CREDIT_EUR, ODOO_CREDIT_EUR_BULK
from fig_overview import points
from figures import GRID, INK, LLM, MUTED, ODOO

plt.rcParams.update({"font.family": ["Inter", "Helvetica Neue", "DejaVu Sans"],
                     "savefig.bbox": "standard"})  # fixed 1080 x 1350, no tight crop


def main() -> None:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    pts = [p for p in points(root) if not p[0].endswith("rules")]  # one arm per model
    models = sorted((p for p in pts if p[0] != "Odoo"), key=lambda p: p[2])
    odoo = next(p for p in pts if p[0] == "Odoo")
    rows = [odoo, *models]  # bottom to top: Odoo last in reading order

    fig = plt.figure(figsize=(5.4, 6.75), dpi=200)
    ax = fig.add_axes((0.37, 0.12, 0.35, 0.66))
    for i, (name, cost, book) in enumerate(rows):
        is_odoo = name == "Odoo"
        y = i + (0.6 if not is_odoo else 0)  # a gap between Odoo and the models
        ax.barh(y, book, height=0.68, color=ODOO if is_odoo else LLM)
        ax.text(book + 2, y, f"{book:.0f}%", va="center", fontsize=11,
                fontweight="bold", color=INK)  # fmt: skip
        ax.text(-3, y, name, va="center", ha="right", fontsize=10.5, color=INK,
                fontweight="bold" if is_odoo else "normal")  # fmt: skip
        price = (f"€{ODOO_CREDIT_EUR_BULK:.2f} to {ODOO_CREDIT_EUR:.2f}" if is_odoo
                 else f"€{cost:.3f}")  # fmt: skip
        ax.text(1.2, y, price, va="center", ha="left", fontsize=10, color=INK if is_odoo
                else MUTED, fontweight="bold" if is_odoo else "normal",
                transform=ax.get_yaxis_transform())  # fmt: skip
    top = len(rows) - 1 + 0.6
    ax.text(1.2, top + 0.8, "Cost\nper bill", ha="left", va="bottom", fontsize=9,
            color=MUTED, transform=ax.get_yaxis_transform())  # fmt: skip
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, top + 0.6)
    ax.set_xticks([0, 50, 100], ["0", "50", "100%"])
    ax.set_yticks([])
    ax.tick_params(length=0, labelsize=9)
    ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_visible(False)

    fig.text(0.05, 0.955, "We compared Odoo IAP with LLMs.\nThis is the result.",
             fontsize=19, fontweight="bold", color=INK, va="top", linespacing=1.15)  # fmt: skip
    fig.text(0.05, 0.835, "Bills you can book without fixing anything",
             fontsize=11.5, color=MUTED, va="top")  # fmt: skip
    fig.text(0.05, 0.035, "223 public test bills. Odoo before it matches suppliers to your contacts.\n"
             "github.com/pantalytics/odoo-iap-benchmark",
             fontsize=8, color=MUTED, va="bottom", linespacing=1.4)  # fmt: skip
    fig.savefig(out / "social_bookable.png", dpi=200, facecolor="white", bbox_inches=None)
    fig.savefig(out / "social_bookable.svg", facecolor="white", bbox_inches=None)


if __name__ == "__main__":
    main()
