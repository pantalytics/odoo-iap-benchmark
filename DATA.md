# Data dictionary

Every file under `results/`, and what each column means. JSON holds the full
record; the CSV files are flat copies for spreadsheets and statistics tools,
written by `src/export_csv.py` and `src/bench_invoices.py`. CI regenerates
all of them from the raw answers and fails if one differs from what is
committed.

## Layout

```
results/
  <set>/                     donut, en16931, sroie
    truth.jsonl              the right answers, one bill per line (source of the CSVs below)
    truth_bills.csv          the same, header fields
    truth_lines.csv          the same, one row per line item
    aggregate.md             mean and range over the runs, AI cost, correction time
    r1/, r2/                 one folder per run
      raw/<engine>/<bill>.json   every answer as received (see below)
      calls.csv              one row per call: model, provider, time, cost, tokens, error
      answers_bills.csv      what each engine read, header fields
      answers_lines.csv      what each engine read, line items
      results.csv            every scored field: right value, read value, right or not
      results_strict.csv     the same under the original scoring rules (paper, section 8)
      summary.md, .json      the run's scores per engine
      summary_strict.*       the same under the original rules
```

In `r2/` and later, `raw/odoo` is a link to `r1/raw/odoo`: Odoo's answers were
identical across runs (paper, section 4.5), so they are stored once.

## Bills: `truth_bills.csv`, `answers_bills.csv`

| Column | Meaning |
|---|---|
| `id` / `bill` | Bill id: `donut-<split>-<row>`, `zugferd-<n>` (EN 16931), `sroie-<n>` |
| `engine` | `odoo` or a model key (see `src/bench_invoices.py`, `ENGINES`) |
| `vendor_name` | Seller's name. Donut's truth carries the address after the name |
| `vendor_vat` | Seller's VAT number or tax id as printed |
| `invoice_ref` | The bill's own number |
| `invoice_date`, `due_date` | ISO dates (truth); as read (answers) |
| `currency` | ISO 4217 code (truth); as read, sometimes a sign such as `$` |
| `untaxed`, `tax`, `total` | Amounts. EN 16931 credit notes are positive in the truth, negative on the page |
| `iban` | Seller's IBAN. Donut truth IBANs failing the checksum are not scored |
| `vat_treatment` | EN 16931 VAT category of the bill (S, Z, E, AE, K, G, O); Odoo does not return it |
| `vendor_country`, `buyer_*` | Truth only. The buyer is sent to Odoo as its own company |
| `source`, `source_sha256` | Truth only. Dataset and revision (or repository commit and path) of the source file, and its SHA-256 |

An empty cell means absent: not on the bill (truth) or not returned (answer).
An absent truth is not scored.

## Lines: `truth_lines.csv`, `answers_lines.csv`

| Column | Meaning |
|---|---|
| `line` | Position on the bill, from 1. Lines are scored by position |
| `description`, `quantity`, `unit_price` | As printed |
| `tax_rate` | VAT rate in percent |
| `net` | Line amount before tax |
| `vat_category` | EN 16931 category of the line (EN 16931 truth only) |

## Calls: `calls.csv`

| Column | Meaning |
|---|---|
| `model` | The model that answered, as OpenRouter reports it; `odoo-extract-api` for Odoo |
| `provider` | Who served it on OpenRouter (for example Google, Anthropic, Azure) |
| `status`, `error` | `ok`, or `error` with the message. Errors were retried; what is left failed |
| `seconds` | Wall-clock time of the call, Odoo's queue polling included |
| `cost_usd` | Cost as billed by OpenRouter; for Odoo the credit price assumed at run time (the paper uses the list price, EUR 0.15) |
| `prompt_tokens`, `completion_tokens`, `reasoning_tokens` | As reported by OpenRouter |

## Scores: `results.csv`, `results_strict.csv`

| Column | Meaning |
|---|---|
| `doc` | Bill id |
| `engine` | Engine key |
| `field` | Header field, or `line<n>.<field>` for line items |
| `truth`, `pred` | Right value and read value |
| `ok` | 1 when they match under the rules of `src/bench_score.py`, else 0 |

The bookable outcome, the VAT summary per rate and the summaries are
computed from the raw answers by `src/bench_score.py`; see the paper,
section 4.5.

## Raw answers: `raw/<engine>/<bill>.json`

| Key | Meaning |
|---|---|
| `pred` | The answer, normalised to the fields above |
| `raw` | The response as received: OpenRouter's full chat completion, or Odoo's result with every candidate and its position on the page (the OCR text is dropped to save space) |
| `cost_usd`, `seconds` | As in `calls.csv` |
| `error` | Present only when the call failed |
