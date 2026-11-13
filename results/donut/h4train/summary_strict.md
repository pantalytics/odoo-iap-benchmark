# Bill extraction benchmark: donut (strict scoring)

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 50 | 64.0 | 50.1 to 75.9 | 98.0 | 100.0 | 65.3 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 50 | 0 | 91.7 | 88.8 to 94.0 | 42.0 | 29.4 to 55.8 | 99.9 | 198/198 | 0.0045 | 10.2 |

Per field, % right:

| Field | gemini-flash |
|---|---|
| vendor_name | 98.0 |
| vendor_vat | 100.0 |
| invoice_ref | 100.0 |
| invoice_date | 65.3 |
| currency | 100.0 |
| untaxed | 100.0 |
| tax | 100.0 |
| total | 100.0 |
| iban | 62.5 |
