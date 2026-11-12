# Reading rules in the prompt (H3, H4)

Bookable without correction, %. Baseline: mean over the runs in r*/. H3 and H4: one run each, same test samples.

| Set | Model | Baseline prompt | + hand-written rules (H3) | + learned rules (H4) | Date right, base to H3 to H4 |
|---|---|---|---|---|---|
| Donut invoices | Gemini 3.8 Flash | 64 | 97 | 64 | 65 to 100 to 65 |
| Donut invoices | Claude Sonnet 5.5 | 97 | 97 | 97 | 100 to 100 to 100 |
| EN 16931 invoices | Gemini 3.8 Flash | 100 | 100 | 83 | 100 to 100 to 100 |
| EN 16931 invoices | Claude Sonnet 5.5 | 96 | 96 | 100 | 96 to 96 to 100 |
| SROIE receipts | Gemini 3.8 Flash | 94 | 95 | 91 | 99 to 99 to 99 |
| SROIE receipts | Claude Sonnet 5.5 | 91 | 89 | 91 | 98 to 97 to 97 |
