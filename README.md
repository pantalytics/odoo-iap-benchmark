# Bill extraction benchmark: Odoo digitization against multimodal LLMs

How often does Odoo's document digitization read a vendor bill well enough
to book it, and how do current language models compare? The paper is
[paper.md](paper.md); everything needed to check or repeat it is here.

| Folder | What |
|---|---|
| `paper.md` | Research questions, hypotheses, data, method, results, discussion |
| `plan.md`, `plan-history/` | The study plan, and every version of it with commit time |
| `src/` | The code: build the test sets, run the engines, score, aggregate |
| `results/<set>/r1..r3/` | Every raw answer of every engine (`raw/`), the per-field scores (`results.csv`), the summaries (`summary.md`, `summary.json`) and the strict-scoring variant (`*_strict.*`) |
| `results/<set>/truth.jsonl` | The right answers, with source revision and SHA-256 of each source file |
| `results/<set>/aggregate.md` | Mean and range over the runs |
| `results/**/*.csv` | Flat copies of truth, answers, calls and scores; every column in [DATA.md](DATA.md) |

## Rescore without spending anything

The raw answers are in the repository, so the scores can be recomputed
from them. That needs the truth files only, no PDFs and no keys:

```bash
python3 src/bench_invoices.py results/en16931 results/en16931/r1 --engines odoo,gemini-flash,gemini-pro,gemini-2.5-pro,claude-sonnet,gpt,mistral-ocr --score-only
```

```bash
python3 src/aggregate.py results
```

The figures (needs `pip install matplotlib`):

```bash
python3 src/figures.py results figures && python3 src/fig_overview.py results figures
```

## Repeat from scratch

Python 3.12 or newer. Only `prepare_zugferd.py` needs a package (`pypdf`).

1. Build the Donut set (501 bills; the run samples 100 with seed 42):

```bash
python3 src/prepare_donut.py data/donut
```

2. Build the EN 16931 set from the ZUGFeRD corpus at the commit we used:

```bash
git clone https://github.com/ZUGFeRD/corpus data/zugferd-corpus
```

```bash
git -C data/zugferd-corpus checkout 84f8d8f68f6c3698aa3019d701a8b82db9ba0aac
```

```bash
pip install pypdf==7.0.1
```

```bash
python3 src/prepare_zugferd.py data/zugferd-corpus data/en16931
```

3. Run and score. Keys come from the environment: `OPENROUTER_API_KEY`,
   and `ODOO_IAP_TOKEN` for Odoo (an IAP account for "Document
   Digitization"; without it the free, rate-limited `integration_token`
   is used).

```bash
python3 src/bench_invoices.py data/donut out/donut/r1 --sample 100 --max-eur 15
```

```bash
python3 src/bench_invoices.py data/en16931 out/en16931/r1 --max-eur 5
```

Every answer is cached, so an interrupted run continues where it stopped
and costs nothing twice. `--strict` scores with the rules as first
written (see the paper, Deviations).

Model answers change over time even at temperature 0, and providers
update models behind the same name. Expect your numbers to land near ours,
not on them; the run-to-run range in `aggregate.md` shows how near.

## Licences

Code (`src/`): Apache-2.0, see `LICENSE`. Paper, plan and results: CC BY
4.0, see `LICENSE-CC-BY-4.0.txt`. Test data: Donut invoices under MIT
(katanaml-org/invoices-donut-data-v1); EN 16931 samples under Apache-2.0
(ZUGFeRD corpus; samples by FeRD and FNFE-MPE). The truth files are derived
from those and carry their terms.

## Who

Pantalytics B.V., Rotterdam, builds AI Pro, a module that runs language
models in Odoo. See the paper's conflict-of-interest section.
