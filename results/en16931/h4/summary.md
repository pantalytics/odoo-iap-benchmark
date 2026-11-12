# Bill extraction benchmark: en16931

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 23 | 82.6 | 62.9 to 93.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 82.6 | 100.0 |
| claude-sonnet | 23 | 100.0 | 85.7 to 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| gemini-flash | 23 | 0 | 98.2 | 95.5 to 99.3 | 82.6 | 62.9 to 93.0 | 98.6 | 53/53 | 0.0086 | 15.9 |
| claude-sonnet | 23 | 0 | 100.0 | 98.3 to 100.0 | 100.0 | 85.7 to 100.0 | 99.5 | 53/53 | 0.0150 | 3.1 |

Per field, % right:

| Field | gemini-flash | claude-sonnet |
|---|---|---|
| vendor_name | 100.0 | 100.0 |
| vendor_vat | 100.0 | 100.0 |
| invoice_ref | 100.0 | 100.0 |
| invoice_date | 100.0 | 100.0 |
| due_date | 100.0 | 100.0 |
| currency | 100.0 | 100.0 |
| untaxed | 100.0 | 100.0 |
| tax | 100.0 | 100.0 |
| total | 82.6 | 100.0 |
| iban | 100.0 | 100.0 |
| vat_treatment | 100.0 | 100.0 |
