# Bill extraction benchmark: en16931 (strict scoring)

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 23 | 78.3 | 58.1 to 90.3 | 100.0 | 100.0 | 100.0 | 100.0 | 95.7 | 95.7 | 78.3 | 100.0 |
| claude-sonnet | 23 | 95.7 | 79.0 to 99.2 | 100.0 | 100.0 | 100.0 | 100.0 | 95.7 | 95.7 | 95.7 | 100.0 |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 23 | 0 | 94.7 | 91.0 to 97.0 | 60.9 | 40.8 to 77.8 | 95.3 | 53/53 | 0.0086 | 15.9 |
| claude-sonnet | 23 | 0 | 96.5 | 93.2 to 98.2 | 78.3 | 58.1 to 90.3 | 96.7 | 53/53 | 0.0150 | 3.1 |

Per field, % right:

| Field | gemini-flash | claude-sonnet |
|---|---|---|
| vendor_name | 78.3 | 78.3 |
| vendor_vat | 100.0 | 100.0 |
| invoice_ref | 100.0 | 100.0 |
| invoice_date | 100.0 | 100.0 |
| due_date | 100.0 | 100.0 |
| currency | 100.0 | 100.0 |
| untaxed | 95.7 | 95.7 |
| tax | 95.7 | 95.7 |
| total | 78.3 | 95.7 |
| iban | 100.0 | 100.0 |
| vat_treatment | 100.0 | 100.0 |
