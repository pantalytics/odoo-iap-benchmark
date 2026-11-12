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

# AI cost: language models as billed by OpenRouter (USD, converted at
# USD_EUR); Odoo at the list price of its smallest credit pack (100 credits
# for EUR 15, iap.odoo.com, 2026-11-12), one credit per document.
USD_EUR = 0.86
ODOO_CREDIT_EUR = 0.15
# Human time is reported apart, in hours, never priced: each bill that is
# not bookable as read needs a correction, assumed to take this long.
CORRECTION_MINUTES = 2

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
            f"AI cost: OpenRouter as billed (USD at {USD_EUR}), Odoo at EUR {ODOO_CREDIT_EUR} a "
            f"credit. Correction time: {CORRECTION_MINUTES} minutes per bill that is not "
            "bookable, an assumption.\n",
            "| Engine | " + " | ".join(m[0] for m in METRICS) + " | AI cost, EUR per 100 bills "
            "| Bills to correct per 100 | Correction time per 100 bills |",
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
            if e == "odoo":
                cost = ODOO_CREDIT_EUR
            else:  # summaries hold USD as billed times 0.86, the rate bench_invoices used
                eur = sum(d[e]["cost"] / d[e]["docs"] for d in data if e in d) / len(data)
                cost = eur / 0.86 * USD_EUR
            rates = [d[e]["book"] / d[e]["book_n"] for d in data if e in d and d[e]["book_n"]]
            to_fix = 100 * (1 - sum(rates) / len(rates)) if rates else 0.0
            hours = to_fix * CORRECTION_MINUTES / 60
            md.append(
                f"| {e} | "
                + " | ".join(cells)
                + f" | {100 * cost:.2f} | {to_fix:.0f} | {hours:.1f} h |"
            )
        text = "\n".join(md) + "\n"
        (set_dir / "aggregate.md").write_text(text)
        print(text)


if __name__ == "__main__":
    main()
