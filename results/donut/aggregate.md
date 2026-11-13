# donut: 2 runs

Mean over runs, range in brackets. Odoo was run once: two runs gave byte-identical output, so the same answers are scored in every run. AI cost: OpenRouter as billed (USD at 0.86), Odoo at EUR 0.05 to 0.15 a credit by pack size. Correction time: 2 minutes per bill that is not bookable, an assumption.

| Engine | Bookable % | Header fields % | Line fields % | Line VAT rate % | AI cost, EUR per 100 bills | Bills to correct per 100 | Correction time per 100 bills |
|---|---|---|---|---|---|---|---|
| odoo | 0.0 [0.0 to 0.0] | 51.5 [51.5 to 51.5] | 50.4 [50.4 to 50.4] | 4.2 [4.2 to 4.2] | 5.00 to 15.00 | 100 | 3.3 h |
| gemini-flash | 64.0 [64.0 to 64.0] | 95.4 [95.4 to 95.5] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 0.44 | 36 | 1.2 h |
| gemini-pro | 70.0 [69.0 to 71.0] | 96.2 [96.1 to 96.3] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 2.57 | 30 | 1.0 h |
| gemini-2.5-pro | 68.0 [66.0 to 70.0] | 95.9 [95.6 to 96.1] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 1.65 | 32 | 1.1 h |
| claude-sonnet | 97.0 [97.0 to 97.0] | 99.5 [99.5 to 99.5] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 0.92 | 3 | 0.1 h |
| gpt | 71.5 [70.0 to 73.0] | 96.1 [96.0 to 96.2] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 2.19 | 29 | 1.0 h |
| gpt-terra | 70.0 [66.0 to 74.0] | 96.0 [95.5 to 96.5] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 0.75 | 30 | 1.0 h |
| claude-opus | 97.0 [97.0 to 97.0] | 99.5 [99.5 to 99.5] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 1.89 | 3 | 0.1 h |
| mistral-ocr | 61.0 [61.0 to 61.0] | 95.0 [95.0 to 95.0] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 0.56 | 39 | 1.3 h |
