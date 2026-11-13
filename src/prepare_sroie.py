#!/usr/bin/env python3
# Copyright 2026 Pantalytics B.V.
# SPDX-License-Identifier: Apache-2.0
"""Turn the SROIE receipts into a bench set: real scanned till receipts.

Source: ICDAR 2019 SROIE task 3 (scanned receipts, Malaysia), as published
with labels in github.com/zzzDavid/ICDAR-2019-SROIE (data/img, data/key; 626
labelled receipts). Fraunhofer IAIS used the same copy. Labels per receipt:
company, date, address, total. Each JPEG is wrapped unchanged in a PDF, as
for Donut.

Usage:
    python src/prepare_sroie.py SROIE_REPO_DIR OUT_DIR

Writes OUT_DIR/<id>.pdf and OUT_DIR/truth.jsonl. Stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from prepare_donut import amount, jpeg_to_pdf

MONTHS = {m: i for i, m in enumerate("JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split(), 1)}


def dmy(text: str | None) -> str | None:
    """SROIE dates are day first (25/12/2018, 25-12-18, 25 DEC 2018) or ISO."""
    t = (text or "").strip().strip("()").upper()
    if m := re.fullmatch(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", t):
        return f"{m[1]}-{int(m[2]):02d}-{int(m[3]):02d}"
    m = re.fullmatch(r"(\d{1,2})[ /.-]([A-Z]{3}|\d{1,2})[ /.-](\d{2}|\d{4})", t)
    if not m:
        return None  # ambiguous or unusual label: not scored
    month = MONTHS.get(m[2]) if m[2].isalpha() else int(m[2])
    if not month or month > 12:  # a month-first label slipped in: not scored
        return None
    year = int(m[3]) + (2000 if len(m[3]) == 2 else 0)
    return f"{year}-{month:02d}-{int(m[1]):02d}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("repo", type=Path, help="a checkout of github.com/zzzDavid/ICDAR-2019-SROIE")
    ap.add_argument("out", type=Path)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    git = ["git", "-C", str(args.repo), "rev-parse", "HEAD"]
    commit = subprocess.run(git, capture_output=True, text=True).stdout.strip() or "unknown"
    rows = []
    for key in sorted((args.repo / "data" / "key").glob("*.json")):
        img = args.repo / "data" / "img" / f"{key.stem}.jpg"
        if not img.exists():
            continue
        label = json.loads(key.read_text())
        doc_id = f"sroie-{key.stem}"
        data = img.read_bytes()
        (args.out / f"{doc_id}.pdf").write_bytes(jpeg_to_pdf(data))
        rows.append(
            {
                "id": doc_id,
                "file": f"{doc_id}.pdf",
                "vendor_name": label.get("company"),
                # Date as labelled; null when the label is not a plain day-first date.
                "invoice_date": dmy(label.get("date")),
                "total": amount(label.get("total")),
                "address": label.get("address"),
                "source": f"zzzDavid/ICDAR-2019-SROIE@{commit}:data/key/{key.name}",
                "source_sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    with (args.out / "truth.jsonl").open("w") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    print(f"{len(rows)} receipts in {args.out}")


if __name__ == "__main__":
    main()
