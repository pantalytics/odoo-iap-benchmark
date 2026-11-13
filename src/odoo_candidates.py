#!/usr/bin/env python3
# Copyright 2026 Pantalytics B.V.
# SPDX-License-Identifier: Apache-2.0
"""Where Odoo loses a field: did it see the right value, and then pick another?

Usage:
    python src/odoo_candidates.py results

Odoo's answer lists, per field, the candidates it found on the page and the
one it selected. Per field and set this counts how often the selected value
is right, and how often the right value was among the candidates at all.
Writes results/odoo_candidates.md. Free: it reads the cached answers only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from bench_score import same

FEATURES = (  # Odoo feature -> our field
    ("supplier", "vendor_name"),
    ("VAT_Number", "vendor_vat"),
    ("invoice_id", "invoice_ref"),
    ("date", "invoice_date"),
    ("subtotal", "untaxed"),
    ("total_tax_amount", "tax"),
    ("total", "total"),
)
SETS = (("donut", "Donut"), ("en16931", "EN 16931"), ("sroie", "SROIE"))


def main() -> None:
    root = Path(sys.argv[1])
    md = [
        "# Odoo: right value selected, and right value among its candidates\n",
        "Per field, % of bills where the truth has a value. Selected: what Odoo "
        "returned as its answer. Among candidates: the right value was in Odoo's own "
        "candidate list, so its OCR saw it.\n",
        "| Set | Field | Bills | Selected right % | Among candidates % |",
        "|---|---|---|---|---|",
    ]
    for key, title in SETS:
        truth = {}
        for line in (root / key / "truth.jsonl").open():
            d = json.loads(line)
            truth[d["id"]] = d
        answers = sorted((root / key / "r1" / "raw" / "odoo").glob("*.json"))
        for feature, field in FEATURES:
            n = sel = cand = 0
            for f in answers:
                t = truth[f.stem].get(field)
                raw = json.loads(f.read_text()).get("raw") or {}
                if t in (None, "") or feature not in raw and field != "vendor_vat":
                    continue
                entry = raw.get(feature) or {}
                values = [c.get("content") for c in entry.get("candidates") or []]
                chosen = (entry.get("selected_value") or {}).get("content")
                n += 1
                sel += same(field, t, chosen)
                cand += any(same(field, t, v) for v in values + [chosen])
            if n:
                md.append(
                    f"| {title} | {field} | {n} | {100 * sel / n:.0f} | {100 * cand / n:.0f} |"
                )
    text = "\n".join(md) + "\n"
    (root / "odoo_candidates.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
