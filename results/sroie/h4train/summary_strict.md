# Bill extraction benchmark: sroie (strict scoring)

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 50 | 96.0 | 86.5 to 98.9 | 98.0 | - | 95.9 | - | - | - | 98.0 | - |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 50 | 1 | 97.3 | 93.3 to 99.0 | 96.0 | 86.5 to 98.9 | - | - | 0.0072 | 18.1 |

Per field, % right:

| Field | gemini-flash |
|---|---|
| vendor_name | 98.0 |
| invoice_date | 95.9 |
| total | 98.0 |
