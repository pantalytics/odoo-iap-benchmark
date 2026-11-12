# Bill extraction benchmark: sroie

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 100 | 95.0 | 88.8 to 97.8 | 97.0 | - | 99.0 | - | - | - | 97.0 | - |
| claude-sonnet | 100 | 89.0 | 81.4 to 93.7 | 97.0 | - | 97.0 | - | - | - | 93.0 | - |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 100 | 0 | 97.7 | 95.3 to 98.9 | 95.0 | 88.8 to 97.8 | - | - | 0.0086 | 18.3 |
| claude-sonnet | 100 | 0 | 95.7 | 92.7 to 97.5 | 89.0 | 81.4 to 93.7 | - | - | 0.0087 | 3.4 |

Per field, % right:

| Field | gemini-flash | claude-sonnet |
|---|---|---|
| vendor_name | 97.0 | 97.0 |
| invoice_date | 99.0 | 97.0 |
| total | 97.0 | 93.0 |
