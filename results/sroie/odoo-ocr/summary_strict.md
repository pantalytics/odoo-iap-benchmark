# Bill extraction benchmark: sroie (strict scoring)

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| odoo-ocr-sonnet | 100 | 81.0 | 72.2 to 87.5 | 88.0 | - | 99.0 | - | - | - | 94.0 | - |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| odoo-ocr-sonnet | 100 | 0 | 93.7 | 90.3 to 95.9 | 81.0 | 72.2 to 87.5 | - | - | 0.0086 | 4.3 |

Per field, % right:

| Field | odoo-ocr-sonnet |
|---|---|
| vendor_name | 88.0 |
| invoice_date | 99.0 |
| total | 94.0 |
