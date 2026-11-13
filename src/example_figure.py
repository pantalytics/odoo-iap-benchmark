#!/usr/bin/env python3
# Copyright 2026 Pantalytics B.V.
# SPDX-License-Identifier: Apache-2.0
"""Figure 4: three bills, what is printed, and what Odoo and a model read.

Usage:
    pip install matplotlib pillow
    python src/example_figure.py results DATA_ROOT figures

DATA_ROOT holds the prepared sets (donut/, en16931/) with their PDFs; the
answers come from results/<set>/r1/raw. Needs pdftoppm (poppler-utils).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

import bench_score  # noqa: E402
from figures import INK, LLM, MUTED, NAMES, ODOO, save  # noqa: E402

GOOD = "#1f7a4d"
BAD = "#b42318"

# (set, bill, page crop as fractions (left, top, right, bottom), caption, fields, model)
EXAMPLES = (
    ("donut", "donut-train-003", (0.0, 0.0, 1.0, 0.62),
     "Donut: Odoo takes a heading as the vendor and misses the VAT",
     ("vendor_name", "untaxed", "tax", "total"), "claude-sonnet"),
    ("en16931", "zugferd-000", (0.0, 0.0, 1.0, 0.45),
     "EN 16931: Odoo picks the wrong number and date",
     ("vendor_name", "invoice_ref", "invoice_date", "total"), "gemini-flash"),
    ("donut", "donut-train-012", (0.0, 0.0, 1.0, 0.30),
     "Donut: a US date that most models read day first",
     ("invoice_date",), "gemini-flash"),
)  # fmt: skip
LABELS = {
    "vendor_name": "Vendor",
    "untaxed": "Untaxed",
    "tax": "Tax",
    "total": "Total",
    "invoice_ref": "Invoice number",
    "invoice_date": "Invoice date",
}


def page(pdf: Path, crop: tuple[float, float, float, float]) -> Image.Image:
    with tempfile.TemporaryDirectory() as tmp:
        stem = Path(tmp) / "page"
        subprocess.run(
            ["pdftoppm", "-r", "110", "-png", "-singlefile", str(pdf), str(stem)],
            capture_output=True, check=True,
        )  # fmt: skip
        img = Image.open(stem.with_suffix(".png"))
        img.load()
    w, h = img.size
    left, top, right, bottom = crop
    return img.crop((int(left * w), int(top * h), int(right * w), int(bottom * h)))


def short(value, field: str = "") -> str:
    text = "(empty)" if value in (None, "") else str(value)
    if field == "vendor_name":  # Donut's truth carries the address after the name
        text = re.split(r"\s\d", text, maxsplit=1)[0]
    return text if len(text) <= 20 else text[:18] + "..."


def main() -> None:
    results, data, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    fig = plt.figure(figsize=(11, 3.2 * len(EXAMPLES)))
    grid = fig.add_gridspec(len(EXAMPLES), 2, width_ratios=[1.05, 1], hspace=0.35, wspace=0.05)
    for row, (set_name, bill, crop, caption, fields, model) in enumerate(EXAMPLES):
        truth = next(
            json.loads(line)
            for line in (results / set_name / "truth.jsonl").open()
            if json.loads(line)["id"] == bill
        )
        raw = results / set_name / "r1" / "raw"
        odoo = json.loads((raw / "odoo" / f"{bill}.json").read_text())["pred"]
        llm = json.loads((raw / model / f"{bill}.json").read_text())["pred"]
        ax = fig.add_subplot(grid[row, 0])
        ax.imshow(page(data / set_name / f"{bill}.pdf", crop))
        ax.set_axis_off()
        ax.set_title(caption, loc="left", fontsize=10.5, fontweight="bold", color=INK)
        tx = fig.add_subplot(grid[row, 1])
        tx.set_axis_off()
        cols = (("Printed", None), ("Odoo", ODOO), (NAMES[model], LLM))
        xs = (0.0, 0.40, 0.72)
        for x, (head, color) in zip(xs, cols, strict=True):
            tx.text(x, 1.0, head, fontsize=9.5, fontweight="bold", color=color or MUTED,
                    transform=tx.transAxes, va="top")  # fmt: skip
        for i, f in enumerate(fields):
            y = 0.74 - i * 0.18
            tx.text(0.0, y + 0.07, LABELS[f], fontsize=8, color=MUTED, transform=tx.transAxes)
            tx.text(xs[0], y, short(truth.get(f), f), fontsize=9, color=INK, transform=tx.transAxes)
            for x, pred in ((xs[1], odoo), (xs[2], llm)):
                ok = bench_score.same(f, truth.get(f), pred.get(f))
                mark = "✓ " if ok else "✗ "
                tx.text(x, y, mark + short(pred.get(f), f), fontsize=9, transform=tx.transAxes,
                        color=GOOD if ok else BAD)  # fmt: skip
    fig.suptitle("Three bills: what is printed, and what was read", x=0.01, ha="left",
                 fontsize=13, fontweight="bold", color=INK)  # fmt: skip
    out.mkdir(parents=True, exist_ok=True)
    save(fig, out, "fig4_examples")
    print(f"figure in {out}")


if __name__ == "__main__":
    main()
