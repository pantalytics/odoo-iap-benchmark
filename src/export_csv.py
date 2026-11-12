#!/usr/bin/env python3
# Copyright 2026 Pantalytics B.V.
# SPDX-License-Identifier: Apache-2.0
"""Flatten the truth files and the raw answers into CSV, for anyone without Python.

Usage:
    python src/export_csv.py results

Writes, per set: truth_bills.csv, truth_lines.csv; per run: calls.csv,
answers_bills.csv and answers_lines.csv. results.csv (the per-field scores)
is written by bench_invoices.py. Columns are described in DATA.md. Stdlib only.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from bench_score import FIELDS

BILL_COLS = ["id", *FIELDS, "vendor_country", "buyer_name", "buyer_vat", "buyer_country"]
LINE_COLS = ["description", "quantity", "unit_price", "tax_rate", "net", "vat_category"]
CALL_COLS = [
    "bill", "engine", "model", "provider", "status", "error", "seconds", "cost_usd",
    "prompt_tokens", "completion_tokens", "reasoning_tokens",
]  # fmt: skip


def write(path: Path, header: list[str], rows: list[list]) -> None:
    with path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def cell(v):
    return "" if v is None else v


def export_set(set_dir: Path) -> None:
    truths = [json.loads(line) for line in (set_dir / "truth.jsonl").open()]
    write(
        set_dir / "truth_bills.csv",
        [*BILL_COLS, "source", "source_sha256"],
        [[cell(t.get(c)) for c in [*BILL_COLS, "source", "source_sha256"]] for t in truths],
    )
    write(
        set_dir / "truth_lines.csv",
        ["id", "line", *LINE_COLS],
        [
            [t["id"], i + 1, *[cell(line.get(c)) for c in LINE_COLS]]
            for t in truths
            for i, line in enumerate(t.get("lines") or [])
        ],
    )
    for run in sorted(set_dir.glob("r*/raw")):
        calls, bills, lines = [], [], []
        for engine_dir in sorted(run.iterdir()):
            engine = engine_dir.name
            for f in sorted(engine_dir.glob("*.json")):
                entry = json.loads(f.read_text())
                raw = entry.get("raw") or {}
                usage = raw.get("usage") or {}
                details = usage.get("completion_tokens_details") or {}
                calls.append(
                    [
                        f.stem, engine, raw.get("model", "odoo-extract-api" if engine == "odoo" else ""),
                        raw.get("provider", ""), "error" if "error" in entry else "ok",
                        entry.get("error", ""), entry.get("seconds", ""), entry.get("cost_usd", ""),
                        usage.get("prompt_tokens", ""), usage.get("completion_tokens", ""),
                        details.get("reasoning_tokens", ""),
                    ]
                )  # fmt: skip
                pred = entry.get("pred") or {}
                bills.append([f.stem, engine, *[cell(pred.get(c)) for c in FIELDS]])
                for i, line in enumerate(pred.get("lines") or []):
                    lines.append([f.stem, engine, i + 1, *[cell(line.get(c)) for c in LINE_COLS]])
        write(run.parent / "calls.csv", CALL_COLS, calls)
        write(run.parent / "answers_bills.csv", ["bill", "engine", *FIELDS], bills)
        write(run.parent / "answers_lines.csv", ["bill", "engine", "line", *LINE_COLS], lines)


def main() -> None:
    root = Path(sys.argv[1])
    for set_dir in sorted(p for p in root.iterdir() if (p / "truth.jsonl").exists()):
        export_set(set_dir)
    print(f"CSV written under {root}")


if __name__ == "__main__":
    main()
