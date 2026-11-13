# Bill extraction benchmark: sroie

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 100 | 91.0 | 83.8 to 95.2 | 95.0 | - | 99.0 | - | - | - | 95.0 | - |
| claude-sonnet | 100 | 91.0 | 83.8 to 95.2 | 96.0 | - | 97.0 | - | - | - | 96.0 | - |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 100 | 0 | 96.3 | 93.6 to 97.9 | 91.0 | 83.8 to 95.2 | - | - | 0.0081 | 16.5 |
| claude-sonnet | 100 | 0 | 96.3 | 93.6 to 97.9 | 91.0 | 83.8 to 95.2 | - | - | 0.0095 | 3.4 |

Per field, % right:

| Field | gemini-flash | claude-sonnet |
|---|---|---|
| vendor_name | 95.0 | 96.0 |
| invoice_date | 99.0 | 97.0 |
| total | 95.0 | 96.0 |
