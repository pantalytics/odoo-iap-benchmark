# Bill extraction benchmark: sroie (strict scoring)

## Bookable without correction

A bill counts when vendor, number, date, currency, untaxed, tax, total and the net amount per VAT rate are all right.

| Engine | Bills | Bookable % | 95% CI | vendor | invoice_ref | invoice_date | currency | untaxed | tax | total | vat_breakdown |
|---|---|---|---|---|---|---|---|---|---|---|---|
| odoo | 100 | 10.0 | 5.5 to 17.4 | 22.0 | - | 69.0 | - | - | - | 55.0 | - |
| gemini-flash | 100 | 93.0 | 86.3 to 96.6 | 95.0 | - | 99.0 | - | - | - | 97.0 | - |
| gemini-pro | 100 | 84.0 | 75.6 to 89.9 | 90.0 | - | 99.0 | - | - | - | 93.0 | - |
| gemini-2.5-pro | 100 | 90.0 | 82.6 to 94.5 | 96.0 | - | 99.0 | - | - | - | 93.0 | - |
| claude-sonnet | 100 | 90.0 | 82.6 to 94.5 | 95.0 | - | 98.0 | - | - | - | 94.0 | - |
| gpt | 100 | 90.0 | 82.6 to 94.5 | 93.0 | - | 98.0 | - | - | - | 97.0 | - |
| gpt-terra | 100 | 83.0 | 74.5 to 89.1 | 89.0 | - | 99.0 | - | - | - | 93.0 | - |
| claude-opus | 100 | 90.0 | 82.6 to 94.5 | 97.0 | - | 99.0 | - | - | - | 92.0 | - |
| mistral-ocr | 100 | 85.0 | 76.7 to 90.7 | 91.0 | - | 97.0 | - | - | - | 94.0 | - |

## All fields

| Engine | Bills | Errors | Header fields right % | 95% CI | Bills fully right % | 95% CI | Line fields right % | Line VAT rate right | EUR per bill | Seconds per bill |
|---|---|---|---|---|---|---|---|---|---|---|
| odoo | 100 | 0 | 48.7 | 43.1 to 54.3 | 10.0 | 5.5 to 17.4 | - | - | 0.1290 | 8.1 |
| gemini-flash | 100 | 0 | 97.0 | 94.4 to 98.4 | 93.0 | 86.3 to 96.6 | - | - | 0.0064 | 15.0 |
| gemini-pro | 100 | 0 | 94.0 | 90.7 to 96.2 | 84.0 | 75.6 to 89.9 | - | - | 0.0303 | 26.1 |
| gemini-2.5-pro | 100 | 0 | 96.0 | 93.1 to 97.7 | 90.0 | 82.6 to 94.5 | - | - | 0.0222 | 21.0 |
| claude-sonnet | 100 | 0 | 95.7 | 92.7 to 97.5 | 90.0 | 82.6 to 94.5 | - | - | 0.0086 | 3.5 |
| gpt | 100 | 0 | 96.0 | 93.1 to 97.7 | 90.0 | 82.6 to 94.5 | - | - | 0.0237 | 11.0 |
| gpt-terra | 100 | 0 | 93.7 | 90.3 to 95.9 | 83.0 | 74.5 to 89.1 | - | - | 0.0126 | 7.2 |
| claude-opus | 100 | 0 | 96.0 | 93.1 to 97.7 | 90.0 | 82.6 to 94.5 | - | - | 0.0192 | 6.9 |
| mistral-ocr | 100 | 0 | 94.0 | 90.7 to 96.2 | 85.0 | 76.7 to 90.7 | - | - | 0.0045 | 4.0 |

Per field, % right:

| Field | odoo | gemini-flash | gemini-pro | gemini-2.5-pro | claude-sonnet | gpt | gpt-terra | claude-opus | mistral-ocr |
|---|---|---|---|---|---|---|---|---|---|
| vendor_name | 22.0 | 95.0 | 90.0 | 96.0 | 95.0 | 93.0 | 89.0 | 97.0 | 91.0 |
| invoice_date | 69.0 | 99.0 | 99.0 | 99.0 | 98.0 | 98.0 | 99.0 | 99.0 | 97.0 |
| total | 55.0 | 97.0 | 93.0 | 93.0 | 94.0 | 97.0 | 93.0 | 92.0 | 94.0 |
