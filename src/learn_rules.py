#!/usr/bin/env python3
# Copyright 2026 Pantalytics B.V.
# SPDX-License-Identifier: Apache-2.0
"""H4: write reading rules from a model's own errors on a training sample.

Reads the per-field scores of a training run (results.csv, scored by
bench_invoices.py), collects the wrong header fields of one engine, and asks
a second model to turn them into at most 10 general rules that quote no
value from the errors. The rules, the request and the raw answer are saved,
so the step can be checked.

Usage:
    python src/learn_rules.py TRAIN_RUN_DIR [TRAIN_RUN_DIR ...] --engine gemini-flash --out rules.txt

Needs OPENROUTER_API_KEY. Stdlib only.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from pathlib import Path

from bench_invoices import OPENROUTER_URL, post

TEACHER = "anthropic/claude-opus-5.5"
ASK = """A model read supplier bills and receipts and returned these fields wrong.
Each line is: field | right value | the model's value.

{errors}

Write at most 10 general reading rules that would have prevented these errors on
other bills. Do not quote any name, number, date or amount from the list above.
Answer with the rules only, one per line, each starting with "- "."""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("runs", type=Path, nargs="+", help="scored training run folders")
    ap.add_argument("--engine", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    errors = []
    for run in args.runs:
        with (run / "results.csv").open() as fh:
            for row in csv.DictReader(fh):
                if row["engine"] == args.engine and row["ok"] == "0" and "." not in row["field"]:
                    errors.append(f"{row['field']} | {row['truth'][:80]} | {row['pred'][:80]}")
    ask = ASK.format(errors="\n".join(errors) or "(none)")
    body = {"model": TEACHER, "temperature": 0, "messages": [{"role": "user", "content": ask}]}
    key = os.environ["OPENROUTER_API_KEY"]
    out = post(OPENROUTER_URL, body, {"Authorization": f"Bearer {key}"})
    rules = out["choices"][0]["message"]["content"].strip()
    args.out.write_text("Reading rules:\n" + rules + "\n")
    trace = {"teacher": TEACHER, "errors": len(errors), "request": ask, "response": out}
    args.out.with_suffix(".trace.json").write_text(json.dumps(trace, indent=1, ensure_ascii=False))
    print(f"{len(errors)} errors -> {args.out}\n{rules}")


if __name__ == "__main__":
    main()
