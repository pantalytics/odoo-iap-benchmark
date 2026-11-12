# en16931: 1 runs

Mean over runs, range in brackets. Odoo was run once: two runs gave byte-identical output, so the same answers are scored in every run. Corrections: EUR 1.33 for each bill that is not bookable.

| Engine | Bookable % | Header fields % | Line fields % | Line VAT rate % | EUR per bill | EUR per bookable bill | EUR per 100 bills incl. corrections |
|---|---|---|---|---|---|---|---|
| odoo | 8.7 [8.7 to 8.7] | 66.8 [66.8 to 66.8] | 16.5 [16.5 to 16.5] | 37.7 [37.7 to 37.7] | 0.1290 | 1.4835 | 134.64 |
| gemini-flash | 100.0 [100.0 to 100.0] | 100.0 [100.0 to 100.0] | 98.6 [98.6 to 98.6] | 100.0 [100.0 to 100.0] | 0.0050 | 0.0050 | 0.50 |
| gemini-pro | 100.0 [100.0 to 100.0] | 100.0 [100.0 to 100.0] | 98.6 [98.6 to 98.6] | 100.0 [100.0 to 100.0] | 0.0293 | 0.0293 | 2.93 |
| gemini-2.5-pro | 95.7 [95.7 to 95.7] | 99.1 [99.1 to 99.1] | 99.1 [99.1 to 99.1] | 100.0 [100.0 to 100.0] | 0.0172 | 0.0179 | 7.51 |
| claude-sonnet | 95.7 [95.7 to 95.7] | 99.1 [99.1 to 99.1] | 94.8 [94.8 to 94.8] | 98.1 [98.1 to 98.1] | 0.0141 | 0.0147 | 7.20 |
| gpt | 100.0 [100.0 to 100.0] | 100.0 [100.0 to 100.0] | 93.9 [93.9 to 93.9] | 98.1 [98.1 to 98.1] | 0.0212 | 0.0212 | 2.12 |
| mistral-ocr | 91.3 [91.3 to 91.3] | 97.8 [97.8 to 97.8] | 93.9 [93.9 to 93.9] | 98.1 [98.1 to 98.1] | 0.0081 | 0.0089 | 12.40 |
