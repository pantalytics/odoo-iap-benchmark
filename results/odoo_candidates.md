# Odoo: right value selected, and right value among its candidates

Per field, % of bills where the truth has a value. Selected: what Odoo returned as its answer. Among candidates: the right value was in Odoo's own candidate list, so its OCR saw it.

| Set | Field | Bills | Selected right % | Among candidates % |
|---|---|---|---|---|
| Donut | vendor_name | 100 | 0 | 99 |
| Donut | vendor_vat | 99 | 2 | 3 |
| Donut | invoice_ref | 100 | 100 | 100 |
| Donut | invoice_date | 100 | 69 | 69 |
| Donut | untaxed | 100 | 6 | 100 |
| Donut | tax | 99 | 6 | 100 |
| Donut | total | 99 | 100 | 100 |
| EN 16931 | vendor_name | 23 | 9 | 65 |
| EN 16931 | vendor_vat | 22 | 27 | 45 |
| EN 16931 | invoice_ref | 23 | 52 | 100 |
| EN 16931 | invoice_date | 23 | 52 | 100 |
| EN 16931 | untaxed | 23 | 96 | 100 |
| EN 16931 | tax | 23 | 96 | 100 |
| EN 16931 | total | 23 | 100 | 100 |
| SROIE | vendor_name | 100 | 20 | 97 |
| SROIE | invoice_date | 99 | 70 | 72 |
| SROIE | total | 100 | 55 | 94 |
