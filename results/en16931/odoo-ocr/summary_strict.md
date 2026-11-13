# Bill extraction benchmark: en16931 (strict scoring)

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| odoo-ocr-sonnet | 23 | 95.7 | 79.0 to 99.2 | 100.0 | 100.0 | 100.0 | 100.0 | 95.7 | 95.7 | 95.7 | 100.0 |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| odoo-ocr-sonnet | 23 | 0 | 96.1 | 92.7 to 97.9 | 73.9 | 53.5 to 87.5 | 93.9 | 53/53 | 0.0085 | 2.9 |

Per field, % right:

| Field | odoo-ocr-sonnet |
|---|---|
| vendor_name | 73.9 |
| vendor_vat | 100.0 |
| invoice_ref | 100.0 |
| invoice_date | 100.0 |
| due_date | 100.0 |
| currency | 100.0 |
| untaxed | 95.7 |
| tax | 95.7 |
| total | 95.7 |
| iban | 100.0 |
| vat_treatment | 100.0 |
