#!/usr/bin/env python3
# Copyright 2026 Pantalytics B.V.
# SPDX-License-Identifier: Apache-2.0
"""Draw the paper's figures from results/<set>/r*/summary.json.

Usage:
    pip install matplotlib
    python src/figures.py results figures

Writes figures/fig1_bookable.png, fig2_fields.png and fig3_cost_time.png
(and an .svg of each). Colours: Pantalytics brand, Odoo in gold, language
models in purple; every mark carries a direct label, so colour is never the
only cue.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from aggregate import (  # noqa: E402
    CORRECTION_MINUTES,
    ODOO_CREDIT_EUR,
    ODOO_CREDIT_EUR_BULK,
    USD_EUR,
)
from bench_score import wilson  # noqa: E402

INK = "#001d21"
MUTED = "#5f6b6d"
GRID = "#e3e6e8"
ODOO = "#e8a317"
LLM = "#5b58d8"
SETS = (("donut", "Donut invoices"), ("en16931", "EN 16931 invoices"), ("sroie", "SROIE receipts"))
NAMES = {
    "odoo": "Odoo",
    "claude-opus": "Claude Opus 5.5",
    "claude-sonnet": "Claude Sonnet 5.5",
    "gpt-terra": "GPT-5.6 Terra",
    "gpt": "GPT-5.5",
    "gemini-pro": "Gemini 3.1 Pro",
    "gemini-2.5-pro": "Gemini 2.5 Pro",
    "gemini-flash": "Gemini 3.8 Flash",
    "mistral-ocr": "Mistral OCR + Medium",
}
FIELDS = (
    ("vendor_vat", "Vendor VAT number"),
    ("vendor_name", "Vendor name"),
    ("invoice_ref", "Invoice number"),
    ("invoice_date", "Invoice date"),
    ("untaxed", "Untaxed amount"),
    ("tax", "Tax amount"),
    ("total", "Total"),
)

plt.rcParams.update(
    {
        "font.family": ["Inter", "DejaVu Sans"],
        "font.size": 10,
        "text.color": INK,
        "axes.labelcolor": MUTED,
        "axes.edgecolor": GRID,
        "xtick.color": MUTED,
        "ytick.color": INK,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "figure.dpi": 200,
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
    }
)


def load(root: Path, name: str) -> list[dict]:
    return [json.loads(p.read_text()) for p in sorted((root / name).glob("r*/summary.json"))]


def mean(runs: list[dict], e: str, hit: str, n: str) -> float | None:
    vals = [r[e][hit] / r[e][n] for r in runs if e in r and r[e][n]]
    return sum(vals) / len(vals) if vals else None


def ai_cost(runs: list[dict], e: str) -> float:
    if e == "odoo":
        return ODOO_CREDIT_EUR
    eur = sum(r[e]["cost"] / r[e]["docs"] for r in runs if e in r) / len(runs)
    return eur / 0.86 * USD_EUR


def save(fig, out: Path, name: str) -> None:
    for ext in ("png", "svg"):
        fig.savefig(out / f"{name}.{ext}")
    plt.close(fig)


def fig_bookable(root: Path, out: Path) -> None:
    present = [(k, t) for k, t in SETS if load(root, k)]
    fig, axes = plt.subplots(1, len(present), figsize=(4.2 * len(present), 4.2), sharey=False)
    axes = axes if len(present) > 1 else [axes]
    for ax, (key, title) in zip(axes, present, strict=True):
        runs = load(root, key)
        rows = []
        for e in NAMES:
            m = mean(runs, e, "book", "book_n")
            if m is not None:
                n = runs[0][e]["book_n"]
                lo, hi = wilson(round(m * n), n)
                rows.append((e, m, lo, hi))
        rows.sort(key=lambda r: r[1])
        for y, (e, m, lo, hi) in enumerate(rows):
            color = ODOO if e == "odoo" else LLM
            ax.plot([100 * lo, 100 * hi], [y, y], color=color, lw=2, solid_capstyle="round")
            ax.scatter(
                100 * m, y, s=70 if e == "odoo" else 50, marker="D" if e == "odoo" else "o",
                color=color, edgecolor="white", linewidth=1.5, zorder=3,
            )  # fmt: skip
            ax.annotate(
                f"{100 * m:.0f}%", (100 * hi, y), xytext=(6, 0), textcoords="offset points",
                va="center", fontsize=9, color=INK, fontweight="bold" if e == "odoo" else None,
            )  # fmt: skip
        ax.set_yticks(range(len(rows)), [NAMES[r[0]] for r in rows])
        ax.set_xlim(-4, 112)
        ax.set_xticks([0, 25, 50, 75, 100], ["0", "25", "50", "75", "100%"])
        ax.grid(axis="x", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0)
        n = runs[0]["odoo"]["book_n"] if "odoo" in runs[0] else ""
        ax.set_title(f"{title} (n={n})", loc="left", fontsize=11, fontweight="bold")
    fig.suptitle(
        "Bills bookable without correction, with 95% interval",
        x=0.01, ha="left", fontsize=13, fontweight="bold",
    )  # fmt: skip
    fig.tight_layout()
    save(fig, out, "fig1_bookable")


def fig_fields(root: Path, out: Path) -> None:
    present = [(k, t) for k, t in SETS if load(root, k)]
    fig, axes = plt.subplots(1, len(present), figsize=(4.2 * len(present), 3.8), sharey=True)
    axes = axes if len(present) > 1 else [axes]
    labels = [label for _, label in FIELDS]
    for ax, (key, title) in zip(axes, present, strict=True):
        runs = load(root, key)
        for y, (field, _) in enumerate(FIELDS):
            llm = []
            for e in NAMES:
                if e == "odoo":
                    continue
                vals = [
                    r[e]["field"][field][0] / r[e]["field"][field][1]
                    for r in runs
                    if e in r and field in r[e]["field"] and r[e]["field"][field][1]
                ]
                if vals:
                    llm.append(sum(vals) / len(vals))
            if llm:
                ax.plot([100 * min(llm), 100 * max(llm)], [y, y], color=LLM, lw=6, alpha=0.35,
                        solid_capstyle="round")  # fmt: skip
                ax.scatter(100 * sum(llm) / len(llm), y, color=LLM, s=30, zorder=3)
            od = [
                r["odoo"]["field"][field][0] / r["odoo"]["field"][field][1]
                for r in runs
                if "odoo" in r and field in r["odoo"]["field"] and r["odoo"]["field"][field][1]
            ]
            if od:
                v = 100 * od[0]
                ax.scatter(v, y, marker="D", color=ODOO, s=60, edgecolor="white", lw=1.5, zorder=4)
                ax.annotate(f"{v:.0f}", (v, y), xytext=(0, 8), textcoords="offset points",
                            ha="center", fontsize=8, color=INK)  # fmt: skip
        ax.set_yticks(range(len(FIELDS)), labels)
        ax.set_ylim(len(FIELDS) - 0.5, -1.0)  # room above the top row for its labels
        ax.set_xlim(-4, 104)
        ax.set_xticks([0, 50, 100], ["0", "50", "100%"])
        ax.grid(axis="x", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0)
        ax.set_title(title, loc="left", fontsize=11, fontweight="bold")
    handles = [
        plt.Line2D([], [], marker="D", ls="", color=ODOO, markersize=7, label="Odoo"),
        plt.Line2D([], [], lw=6, color=LLM, alpha=0.35, label="Language models, lowest to highest"),
        plt.Line2D(
            [], [], marker="o", ls="", color=LLM, markersize=5, label="Language models, mean"
        ),
    ]
    fig.legend(
        handles=handles, loc="lower left", ncol=3, frameon=False, bbox_to_anchor=(0.01, -0.06)
    )
    fig.suptitle("Share of fields read right", x=0.01, ha="left", fontsize=13, fontweight="bold")
    fig.tight_layout()
    save(fig, out, "fig2_fields")


def fig_cost_time(root: Path, out: Path) -> None:
    """Two measures, two panels per set: AI cost and correction time, never one axis."""
    present = [(k, t) for k, t in SETS if load(root, k)]
    fig, axes = plt.subplots(
        len(present), 2, figsize=(9, 2.9 * len(present)), squeeze=False,
        gridspec_kw={"wspace": 0.08},
    )  # fmt: skip
    for row, (key, title) in enumerate(present):
        runs = load(root, key)
        rows = []
        for e in NAMES:
            m = mean(runs, e, "book", "book_n")
            if m is not None:
                hours = 100 * (1 - m) * CORRECTION_MINUTES / 60
                rows.append((e, 100 * ai_cost(runs, e), hours))
        rows.sort(key=lambda r: -r[2])
        ys = range(len(rows))
        colors = [ODOO if e == "odoo" else LLM for e, _, _ in rows]
        for col, (idx, unit, fmt) in enumerate(((1, "EUR", "{:.2f}"), (2, "h", "{:.1f}"))):
            ax = axes[row][col]
            vals = [r[idx] for r in rows]
            # Odoo's price runs from its largest (solid) to its smallest credit pack (pale)
            pale = [
                ODOO + "59" if r[0] == "odoo" and col == 0 else c
                for r, c in zip(rows, colors, strict=True)
            ]
            ax.barh(ys, vals, color=pale, height=0.62)
            if col == 0:
                bulk = [100 * ODOO_CREDIT_EUR_BULK if r[0] == "odoo" else 0 for r in rows]
                ax.barh(ys, bulk, color=ODOO, height=0.62)
            top = max(vals) or 1
            for y, v in zip(ys, vals, strict=True):
                label = fmt.format(v) + (f" {unit}" if unit == "h" else "")
                if unit == "EUR":
                    label = "EUR " + label
                    if rows[y][0] == "odoo":  # solid: largest pack, pale: smallest pack
                        label = f"EUR {100 * ODOO_CREDIT_EUR_BULK:.0f} to {v:.0f}"
                ax.annotate(label, (v, y), xytext=(4, 0), textcoords="offset points",
                            va="center", fontsize=8.5, color=INK)  # fmt: skip
            ax.set_xlim(0, top * 1.35)
            ax.set_xticks([])
            ax.spines["bottom"].set_visible(False)
            ax.tick_params(axis="y", length=0)
            ax.invert_yaxis()
            if col == 0:
                ax.set_yticks(ys, [NAMES[r[0]] for r in rows])
                ax.set_title(f"{title}: AI cost per 100 bills", loc="left", fontsize=10.5,
                             fontweight="bold")  # fmt: skip
            else:
                ax.set_yticks([])
                ax.set_title(
                    f"Correction time per 100 bills ({CORRECTION_MINUTES} min per bill)",
                    loc="left", fontsize=10.5, fontweight="bold",
                )  # fmt: skip
    fig.suptitle("What reading costs, and what correcting takes", x=0.01, ha="left",
                 fontsize=13, fontweight="bold")  # fmt: skip
    fig.tight_layout()
    save(fig, out, "fig3_cost_time")


def main() -> None:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    fig_bookable(root, out)
    fig_fields(root, out)
    fig_cost_time(root, out)
    print(f"figures in {out}")


if __name__ == "__main__":
    main()
