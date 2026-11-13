# Bill extraction benchmark: sroie

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| odoo-ocr-sonnet | 100 | 88.0 | 80.2 to 93.0 | 95.0 | - | 99.0 | - | - | - | 94.0 | - |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| odoo-ocr-sonnet | 100 | 0 | 96.0 | 93.1 to 97.7 | 88.0 | 80.2 to 93.0 | - | - | 0.0086 | 4.3 |

Per field, % right:

| Field | odoo-ocr-sonnet |
|---|---|
| vendor_name | 95.0 |
| invoice_date | 99.0 |
| total | 94.0 |
