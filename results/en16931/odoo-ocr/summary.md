# Bill extraction benchmark: en16931

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| odoo-ocr-sonnet | 23 | 100.0 | 85.7 to 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| odoo-ocr-sonnet | 23 | 0 | 100.0 | 98.3 to 100.0 | 100.0 | 85.7 to 100.0 | 98.1 | 53/53 | 0.0085 | 2.9 |

Per field, % right:

| Field | odoo-ocr-sonnet |
|---|---|
| vendor_name | 100.0 |
| vendor_vat | 100.0 |
| invoice_ref | 100.0 |
| invoice_date | 100.0 |
| due_date | 100.0 |
| currency | 100.0 |
| untaxed | 100.0 |
| tax | 100.0 |
| total | 100.0 |
| iban | 100.0 |
| vat_treatment | 100.0 |
