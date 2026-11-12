# Bill extraction benchmark: sroie

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| odoo | 100 | 8.0 | 4.1 to 15.0 | 20.0 | - | 69.0 | - | - | - | 55.0 | - |
| gemini-flash | 100 | 94.0 | 87.5 to 97.2 | 96.0 | - | 99.0 | - | - | - | 97.0 | - |
| gemini-pro | 100 | 90.0 | 82.6 to 94.5 | 96.0 | - | 99.0 | - | - | - | 93.0 | - |
| gemini-2.5-pro | 100 | 90.0 | 82.6 to 94.5 | 96.0 | - | 99.0 | - | - | - | 93.0 | - |
| claude-sonnet | 100 | 91.0 | 83.8 to 95.2 | 97.0 | - | 98.0 | - | - | - | 94.0 | - |
| gpt | 100 | 91.0 | 83.8 to 95.2 | 94.0 | - | 98.0 | - | - | - | 97.0 | - |
| gpt-terra | 100 | 84.0 | 75.6 to 89.9 | 90.0 | - | 99.0 | - | - | - | 93.0 | - |
| claude-opus | 100 | 90.0 | 82.6 to 94.5 | 97.0 | - | 99.0 | - | - | - | 92.0 | - |
| mistral-ocr | 100 | 88.0 | 80.2 to 93.0 | 94.0 | - | 97.0 | - | - | - | 94.0 | - |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| odoo | 100 | 0 | 48.0 | 42.4 to 53.6 | 8.0 | 4.1 to 15.0 | - | - | 0.1290 | 8.1 |
| gemini-flash | 100 | 0 | 97.3 | 94.8 to 98.6 | 94.0 | 87.5 to 97.2 | - | - | 0.0064 | 15.0 |
| gemini-pro | 100 | 0 | 96.0 | 93.1 to 97.7 | 90.0 | 82.6 to 94.5 | - | - | 0.0303 | 26.1 |
| gemini-2.5-pro | 100 | 0 | 96.0 | 93.1 to 97.7 | 90.0 | 82.6 to 94.5 | - | - | 0.0222 | 21.0 |
| claude-sonnet | 100 | 0 | 96.3 | 93.6 to 97.9 | 91.0 | 83.8 to 95.2 | - | - | 0.0086 | 3.5 |
| gpt | 100 | 0 | 96.3 | 93.6 to 97.9 | 91.0 | 83.8 to 95.2 | - | - | 0.0237 | 11.0 |
| gpt-terra | 100 | 0 | 94.0 | 90.7 to 96.2 | 84.0 | 75.6 to 89.9 | - | - | 0.0126 | 7.2 |
| claude-opus | 100 | 0 | 96.0 | 93.1 to 97.7 | 90.0 | 82.6 to 94.5 | - | - | 0.0192 | 6.9 |
| mistral-ocr | 100 | 0 | 95.0 | 91.9 to 96.9 | 88.0 | 80.2 to 93.0 | - | - | 0.0045 | 4.0 |

Per field, % right:

| Field | odoo | gemini-flash | gemini-pro | gemini-2.5-pro | claude-sonnet | gpt | gpt-terra | claude-opus | mistral-ocr |
|---|---|---|---|---|---|---|---|---|---|
| vendor_name | 20.0 | 96.0 | 96.0 | 96.0 | 97.0 | 94.0 | 90.0 | 97.0 | 94.0 |
| invoice_date | 69.0 | 99.0 | 99.0 | 99.0 | 98.0 | 98.0 | 99.0 | 99.0 | 97.0 |
| total | 55.0 | 97.0 | 93.0 | 93.0 | 94.0 | 97.0 | 93.0 | 92.0 | 94.0 |
