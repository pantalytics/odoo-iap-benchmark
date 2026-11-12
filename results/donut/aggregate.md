# donut: 1 runs

Mean over runs, range in brackets. Odoo was run once: two runs gave byte-identical output, so the same answers are scored in every run. AI cost: OpenRouter as billed (USD at 0.86), Odoo at EUR 0.15 a credit. Correction time: 2 minutes per bill that is not bookable, an assumption.

| Engine | Bookable % | Header fields % | Line fields % | Line VAT rate % | AI cost, EUR per 100 bills | Bills to correct per 100 | Correction time per 100 bills |
|---|---|---|---|---|---|---|---|
| odoo | 0.0 [0.0 to 0.0] | 51.5 [51.5 to 51.5] | 50.4 [50.4 to 50.4] | 4.2 [4.2 to 4.2] | 15.00 | 100 | 3.3 h |
| gemini-flash | 64.0 [64.0 to 64.0] | 95.5 [95.5 to 95.5] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 0.44 | 36 | 1.2 h |
| gemini-pro | 69.0 [69.0 to 69.0] | 96.1 [96.1 to 96.1] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 2.55 | 31 | 1.0 h |
| gemini-2.5-pro | 70.0 [70.0 to 70.0] | 96.1 [96.1 to 96.1] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 1.66 | 30 | 1.0 h |
| claude-sonnet | 97.0 [97.0 to 97.0] | 99.5 [99.5 to 99.5] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 0.92 | 3 | 0.1 h |
| gpt | 73.0 [73.0 to 73.0] | 96.2 [96.2 to 96.2] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 2.19 | 27 | 0.9 h |
| mistral-ocr | 61.0 [61.0 to 61.0] | 95.0 [95.0 to 95.0] | 99.7 [99.7 to 99.7] | 100.0 [100.0 to 100.0] | 0.56 | 39 | 1.3 h |
