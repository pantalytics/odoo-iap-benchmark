# Bill extraction benchmark: donut

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 100 | 64.0 | 54.2 to 72.7 | 99.0 | 100.0 | 65.0 | 100.0 | 99.0 | 100.0 | 100.0 | 99.0 |
| claude-sonnet | 100 | 97.0 | 91.5 to 99.0 | 99.0 | 100.0 | 100.0 | 100.0 | 99.0 | 100.0 | 100.0 | 99.0 |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 100 | 0 | 95.5 | 93.9 to 96.7 | 64.0 | 54.2 to 72.7 | 99.7 | 355/355 | 0.0054 | 9.7 |
| claude-sonnet | 100 | 0 | 99.5 | 98.8 to 99.8 | 96.0 | 90.2 to 98.4 | 99.7 | 355/355 | 0.0102 | 3.6 |

Per field, % right:

| Field | gemini-flash | claude-sonnet |
|---|---|---|
| vendor_name | 98.0 | 98.0 |
| vendor_vat | 100.0 | 100.0 |
| invoice_ref | 100.0 | 100.0 |
| invoice_date | 65.0 | 100.0 |
| currency | 100.0 | 100.0 |
| untaxed | 99.0 | 99.0 |
| tax | 100.0 | 100.0 |
| total | 100.0 | 100.0 |
| iban | 98.7 | 98.7 |
