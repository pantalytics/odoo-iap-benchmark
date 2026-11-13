#!/usr/bin/env python3
# Copyright 2026 Pantalytics B.V.
# SPDX-License-Identifier: Apache-2.0
"""H3 and H4: baseline prompt against hand-written and learned reading rules.

Usage:
    python src/compare_prompts.py results [figures]

Reads results/<set>/r*/summary.json (baseline, mean over runs), h3/ and h4/,
writes results/prompting.md and, with a figures folder, fig5_prompting.png.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SETS = (("donut", "Donut invoices"), ("en16931", "EN 16931 invoices"), ("sroie", "SROIE receipts"))
MODELS = (("gemini-flash", "Gemini 3.8 Flash"), ("claude-sonnet", "Claude Sonnet 5.5"))
ARMS = (
    ("base", "Baseline prompt"),
    ("h3", "+ hand-written rules (H3)"),
    ("h4", "+ learned rules (H4)"),
)


def rate(summaries: list[dict], engine: str, hit: str = "book", n: str = "book_n") -> float | None:
    vals = [s[engine][hit] / s[engine][n] for s in summaries if engine in s and s[engine][n]]
    return 100 * sum(vals) / len(vals) if vals else None


def collect(root: Path) -> dict:
    out = {}
    for key, _ in SETS:
        base = [json.loads(p.read_text()) for p in sorted((root / key).glob("r*/summary.json"))]
        arms = {"base": base}
        for arm in ("h3", "h4"):
            p = root / key / arm / "summary.json"
            arms[arm] = [json.loads(p.read_text())] if p.exists() else []
        out[key] = arms
    return out


def table(data: dict) -> str:
    md = [
        "# Reading rules in the prompt (H3, H4)\n",
        "Bookable without correction, %. Baseline: mean over the runs in r*/. "
        "H3 and H4: one run each, same test samples.\n",
        "| Set | Model | "
        + " | ".join(label for _, label in ARMS)
        + " | Date right, base to H3 to H4 |",
        "|---" * (len(ARMS) + 3) + "|",
    ]
    for key, title in SETS:
        for engine, name in MODELS:
            cells = []
            dates = []
            for arm, _ in ARMS:
                r = rate(data[key][arm], engine)
                cells.append(f"{r:.0f}" if r is not None else "-")
                d = [
                    s[engine]["field"]["invoice_date"]
                    for s in data[key][arm]
                    if engine in s and "invoice_date" in s[engine]["field"]
                ]
                dates.append(
                    f"{100 * sum(h for h, _ in d) / sum(n for _, n in d):.0f}" if d else "-"
                )
            md.append(f"| {title} | {name} | " + " | ".join(cells) + f" | {' to '.join(dates)} |")
    return "\n".join(md) + "\n"


def figure(data: dict, out: Path) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    from figures import GRID, INK, save

    colors = {"base": "#8a9396", "h3": "#5b58d8", "h4": "#0f8f6a"}
    markers = {"base": "o", "h3": "s", "h4": "^"}
    present = [(k, t) for k, t in SETS if data[k]["h3"] or data[k]["h4"]]
    fig, axes = plt.subplots(1, len(present), figsize=(4.2 * len(present), 3.2), sharey=True)
    axes = axes if len(present) > 1 else [axes]
    for ax, (key, title) in zip(axes, present, strict=True):
        for y, (engine, _) in enumerate(MODELS):
            pts = [(arm, rate(data[key][arm], engine)) for arm, _ in ARMS]
            offsets = {"base": -0.22, "h3": 0.0, "h4": 0.22}  # dodge, so no marker hides another
            for arm, v in pts:
                if v is not None:
                    yy = y + offsets[arm]
                    ax.scatter(v, yy, color=colors[arm], marker=markers[arm], s=60,
                               edgecolor="white", lw=1.2, zorder=3)  # fmt: skip
                    ax.annotate(f"{v:.0f}", (v, yy), xytext=(-8, 0), textcoords="offset points",
                                ha="right", va="center", fontsize=8, color=INK)  # fmt: skip
        ax.set_yticks(range(len(MODELS)), [name for _, name in MODELS])
        ax.set_ylim(-0.6, len(MODELS) - 0.4)
        ax.set_xlim(40, 104)
        ax.set_xticks([50, 75, 100], ["50", "75", "100%"])
        ax.grid(axis="x", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0)
        ax.set_title(title, loc="left", fontsize=11, fontweight="bold", color=INK)
    handles = [
        plt.Line2D([], [], marker=markers[a], ls="", color=colors[a], markersize=8, label=label)
        for a, label in ARMS
    ]
    fig.legend(
        handles=handles, loc="lower left", ncol=3, frameon=False, bbox_to_anchor=(0.01, -0.12)
    )
    fig.suptitle("Bookable without correction: does telling the model how to read help?",
                 x=0.01, ha="left", fontsize=13, fontweight="bold", color=INK)  # fmt: skip
    fig.tight_layout()
    save(fig, out, "fig5_prompting")


def main() -> None:
    root = Path(sys.argv[1])
    data = collect(root)
    text = table(data)
    (root / "prompting.md").write_text(text)
    print(text)
    if len(sys.argv) > 2:
        figure(data, Path(sys.argv[2]))


if __name__ == "__main__":
    main()
