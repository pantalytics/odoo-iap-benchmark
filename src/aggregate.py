#!/usr/bin/env python3
# Copyright 2026 Pantalytics B.V.
# SPDX-License-Identifier: Apache-2.0
"""Summarise repeated runs: mean and range per engine over r1, r2, r3.

Usage:
    python src/aggregate.py RESULTS_DIR

RESULTS_DIR holds one folder per set (donut, en16931), each with one folder
per run (r1, r2, ...) that bench_invoices.py scored. Writes
RESULTS_DIR/<set>/aggregate.md and prints it. Stdlib only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# The cost of a bill that is not bookable as read: someone corrects it. Two
# minutes at EUR 40 an hour, an assumption; the paper shows what it does.
CORRECTION_EUR = 2 / 60 * 40

METRICS = (
    ("Bookable %", "book", "book_n"),
    ("Header fields %", "hits", "n"),
    ("Line fields %", "line_hits", "line_n"),
    ("Line VAT rate %", "rate_hits", "rate_n"),
)


def main() -> None:
    root = Path(sys.argv[1])
    for set_dir in sorted(p for p in root.iterdir() if p.is_dir()):
        runs = sorted(set_dir.glob("r*/summary.json"))
        if not runs:
            continue
        data = [json.loads(r.read_text()) for r in runs]
        engines = list(data[0])
        md = [
            f"# {set_dir.name}: {len(runs)} runs\n",
            "Mean over runs, range in brackets. Odoo was run once: two runs gave "
            "byte-identical output, so the same answers are scored in every run. "
            f"Corrections: EUR {CORRECTION_EUR:.2f} for each bill that is not bookable.\n",
            "| Engine | " + " | ".join(m[0] for m in METRICS) + " | EUR per bill "
            "| EUR per bookable bill | EUR per 100 bills incl. corrections |",
            "|---" * (len(METRICS) + 4) + "|",
        ]
        for e in engines:
            cells = []
            for _, hit, n in METRICS:
                vals = [100 * d[e][hit] / d[e][n] for d in data if e in d and d[e][n]]
                if not vals:
                    cells.append("-")
                    continue
                mean = sum(vals) / len(vals)
                cells.append(f"{mean:.1f} [{min(vals):.1f} to {max(vals):.1f}]")
            cost = sum(d[e]["cost"] / d[e]["docs"] for d in data if e in d) / len(data)
            rates = [d[e]["book"] / d[e]["book_n"] for d in data if e in d and d[e]["book_n"]]
            bookable = sum(rates) / len(rates) if rates else 0.0
            per_bookable = f"{cost / bookable:.4f}" if bookable else "-"
            per_100 = 100 * cost + 100 * (1 - bookable) * CORRECTION_EUR
            md.append(
                f"| {e} | "
                + " | ".join(cells)
                + f" | {cost:.4f} | {per_bookable} | {per_100:.2f} |"
            )
        text = "\n".join(md) + "\n"
        (set_dir / "aggregate.md").write_text(text)
        print(text)


if __name__ == "__main__":
    main()
