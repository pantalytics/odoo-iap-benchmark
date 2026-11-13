# Bill extraction benchmark: donut

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| odoo-ocr-sonnet | 100 | 94.0 | 87.5 to 97.2 | 99.0 | 100.0 | 97.0 | 100.0 | 99.0 | 100.0 | 100.0 | 99.0 |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| odoo-ocr-sonnet | 100 | 0 | 98.6 | 97.6 to 99.2 | 89.0 | 81.4 to 93.7 | 99.7 | 355/355 | 0.0075 | 3.2 |

Per field, % right:

| Field | odoo-ocr-sonnet |
|---|---|
| vendor_name | 98.0 |
| vendor_vat | 100.0 |
| invoice_ref | 100.0 |
| invoice_date | 97.0 |
| currency | 100.0 |
| untaxed | 99.0 |
| tax | 100.0 |
| total | 100.0 |
| iban | 92.0 |
