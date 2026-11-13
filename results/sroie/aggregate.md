# sroie: 1 runs

Mean over runs, range in brackets. Odoo was run once: two runs gave byte-identical output, so the same answers are scored in every run. AI cost: OpenRouter as billed (USD at 0.86), Odoo at EUR 0.05 to 0.15 a credit by pack size. Correction time: 2 minutes per bill that is not bookable, an assumption.

| Engine | Bookable % | Header fields % | Line fields % | Line VAT rate % | AI cost, EUR per 100 bills | Bills to correct per 100 | Correction time per 100 bills |
|---|---|---|---|---|---|---|---|
| odoo | 8.0 [8.0 to 8.0] | 48.0 [48.0 to 48.0] | - | - | 5.00 to 15.00 | 92 | 3.1 h |
| gemini-flash | 94.0 [94.0 to 94.0] | 97.3 [97.3 to 97.3] | - | - | 0.64 | 6 | 0.2 h |
| gemini-pro | 90.0 [90.0 to 90.0] | 96.0 [96.0 to 96.0] | - | - | 3.03 | 10 | 0.3 h |
| gemini-2.5-pro | 90.0 [90.0 to 90.0] | 96.0 [96.0 to 96.0] | - | - | 2.22 | 10 | 0.3 h |
| claude-sonnet | 91.0 [91.0 to 91.0] | 96.3 [96.3 to 96.3] | - | - | 0.86 | 9 | 0.3 h |
| gpt | 91.0 [91.0 to 91.0] | 96.3 [96.3 to 96.3] | - | - | 2.37 | 9 | 0.3 h |
| gpt-terra | 84.0 [84.0 to 84.0] | 94.0 [94.0 to 94.0] | - | - | 1.26 | 16 | 0.5 h |
| claude-opus | 90.0 [90.0 to 90.0] | 96.0 [96.0 to 96.0] | - | - | 1.92 | 10 | 0.3 h |
| mistral-ocr | 88.0 [88.0 to 88.0] | 95.0 [95.0 to 95.0] | - | - | 0.45 | 12 | 0.4 h |
