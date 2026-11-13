# Bill extraction benchmark: donut (strict scoring)

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 100 | 97.0 | 91.5 to 99.0 | 99.0 | 100.0 | 100.0 | 100.0 | 99.0 | 100.0 | 100.0 | 99.0 |
| claude-sonnet | 100 | 97.0 | 91.5 to 99.0 | 99.0 | 100.0 | 100.0 | 100.0 | 99.0 | 100.0 | 100.0 | 99.0 |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 100 | 0 | 96.6 | 95.2 to 97.6 | 71.0 | 61.5 to 79.0 | 99.6 | 355/355 | 0.0050 | 10.1 |
| claude-sonnet | 100 | 0 | 96.9 | 95.5 to 97.8 | 73.0 | 63.6 to 80.7 | 99.6 | 355/355 | 0.0095 | 3.5 |

Per field, % right:

| Field | gemini-flash | claude-sonnet |
|---|---|---|
| vendor_name | 98.0 | 98.0 |
| vendor_vat | 100.0 | 100.0 |
| invoice_ref | 100.0 | 100.0 |
| invoice_date | 100.0 | 100.0 |
| currency | 100.0 | 100.0 |
| untaxed | 99.0 | 99.0 |
| tax | 100.0 | 100.0 |
| total | 100.0 | 100.0 |
| iban | 72.7 | 74.7 |
