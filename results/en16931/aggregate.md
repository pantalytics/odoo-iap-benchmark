# en16931: 1 runs

Mean over runs, range in brackets. Odoo was run once: two runs gave byte-identical output, so the same answers are scored in every run. AI cost: OpenRouter as billed (USD at 0.86), Odoo at EUR 0.15 a credit. Correction time: 2 minutes per bill that is not bookable, an assumption.

| Engine | Bookable % | Header fields % | Line fields % | Line VAT rate % | AI cost, EUR per 100 bills | Bills to correct per 100 | Correction time per 100 bills |
|---|---|---|---|---|---|---|---|
| odoo | 8.7 [8.7 to 8.7] | 66.8 [66.8 to 66.8] | 16.5 [16.5 to 16.5] | 37.7 [37.7 to 37.7] | 15.00 | 91 | 3.0 h |
| gemini-flash | 100.0 [100.0 to 100.0] | 100.0 [100.0 to 100.0] | 98.6 [98.6 to 98.6] | 100.0 [100.0 to 100.0] | 0.50 | 0 | 0.0 h |
| gemini-pro | 100.0 [100.0 to 100.0] | 100.0 [100.0 to 100.0] | 98.6 [98.6 to 98.6] | 100.0 [100.0 to 100.0] | 2.93 | 0 | 0.0 h |
| gemini-2.5-pro | 95.7 [95.7 to 95.7] | 99.1 [99.1 to 99.1] | 99.1 [99.1 to 99.1] | 100.0 [100.0 to 100.0] | 1.72 | 4 | 0.1 h |
| claude-sonnet | 95.7 [95.7 to 95.7] | 99.1 [99.1 to 99.1] | 94.8 [94.8 to 94.8] | 98.1 [98.1 to 98.1] | 1.41 | 4 | 0.1 h |
| gpt | 100.0 [100.0 to 100.0] | 100.0 [100.0 to 100.0] | 93.9 [93.9 to 93.9] | 98.1 [98.1 to 98.1] | 2.12 | 0 | 0.0 h |
| mistral-ocr | 91.3 [91.3 to 91.3] | 97.8 [97.8 to 97.8] | 93.9 [93.9 to 93.9] | 98.1 [98.1 to 98.1] | 0.81 | 9 | 0.3 h |
