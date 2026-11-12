# How well does Odoo read a vendor bill? A reproducible comparison of Odoo's document digitization with six multimodal language models

Pantalytics B.V., Rotterdam. Working paper, version 1, November 2026.

Code, data manifests and every raw answer are in this repository
([README](README.md)): github.com/pantalytics/odoo-iap-benchmark.

## Abstract

<!-- RESULTS:ABSTRACT -->

## 1. Introduction

Odoo, an open-source ERP used by small and mid-sized companies, can read
vendor bills: a PDF is sent to Odoo's Extract API, and the fields of a
draft bill are filled in. The service costs one IAP credit per document.
Odoo publishes no accuracy figure for it, and we found no independent
measurement. Accuracy claims that circulate online come from vendors of
competing products and come without a method.

Meanwhile general-purpose multimodal language models (LLMs) read documents
directly from the page image. Berghaus et al. (2025) compared eight such
models on three public invoice sets and found that sending the page image
to the model beats extracting the text first and giving the model the text,
by 10 to 40 percentage points.

Odoo's service is built the second way: according to Odoo's IAP privacy
policy the document is converted to text by Google Cloud Vision, after
which Odoo's own model extracts the fields. That makes the comparison
interesting beyond Odoo: it is a production OCR-then-extract pipeline
against current image-in models.

What matters to the people who use it is not character accuracy but
whether the bill can be booked as read. We therefore define the main
outcome from an accountant's point of view (section 4.4).

### Research questions

- **RQ1.** How often does Odoo's document digitization return a vendor bill
  that can be booked without correction?
- **RQ2.** How do current multimodal LLMs compare on the same bills, in
  accuracy, cost and time?
- **RQ3.** Does putting a dedicated OCR step in front of an LLM (Mistral OCR,
  then Mistral Medium) lose accuracy against giving the LLM the page?
- **RQ4.** How often are the VAT rate per line, the VAT summary and the VAT
  category read correctly?

## 2. Hypotheses

The study plan was written before any data was collected and kept under
version control. Every version of it is published in `plan-history/`, named
by commit time and hash, so the commit hashes below show when each
statement was made.

- **H1** (stated in commit `61632b1`, 2026-11-12 13:49 UTC, before any
  Odoo answer existed): image-in LLMs extract bill fields more accurately
  than Odoo's digitization, because Odoo puts an OCR step first.
- **H2** (commit `61632b1`): the OCR-first LLM pipeline is less accurate
  than image-in LLMs on these born-digital documents; OCR earns its place on
  bad scans only.
- RQ1 and RQ4 had no directional hypothesis; they are descriptive.

## 3. Related work

- **Berghaus et al. (2025)**, Fraunhofer IAIS: eight multimodal models,
  three public sets (Donut synthetic invoices, SROIE receipts, inv-cdip
  scanned invoices), exact-match field accuracy. Gemini 2.5 Pro scored
  96.5% on the Donut invoices. We reuse their Donut set to anchor our
  harness against theirs.
- **Text-recognition benchmarks** (OlmOCRBench, OmniDocBench) score how well
  text and layout are recognised, not whether a field holds the right
  value. Mistral reports 85.2 and 93.1 on them for OCR 4.
- **Key-information-extraction sets**: SROIE and CORD are till receipts;
  DocILE (Šimsa et al., 2023) holds 6,680 English business documents from
  US sources, with hidden test labels; inv-cdip (Gao et al., 2022) holds 350
  scanned US invoices from the 1980s and 1990s. None of them labels the VAT
  treatment of a bill.
- **Vendor leaderboards** (Nanonets IDP) are run by a vendor on its own
  task definitions.

We found no public benchmark that scores European VAT treatment. That gap
shaped the choice of data below.

## 4. Data and method

### 4.1 Test sets

Only public, standard sets were used, so that results can be compared and
repeated. Two hold vendor bills, one holds till receipts.

**Donut invoices.** `katanaml-org/invoices-donut-data-v1` on Hugging Face,
revision `d2cde298e79c94fb05bc320999deb4b7889b0464`, MIT licence. 501
synthetic English invoices with US addresses, rendered at 2481 × 3508
pixels, with structured ground truth (header, line items, summary). This is
the "clean invoices" set of Berghaus et al. Each JPEG was wrapped unchanged
in a one-page A4 PDF, so that every engine received the same file type.
For cost reasons we drew a fixed random sample of 100 bills
(`random.Random(42).sample`). The sample has 366 lines; 355 carry a VAT
rate (all 10%), 11 carry none. Currency is printed as "$" on 96 bills and
missing on 4.

**EN 16931 sample invoices.** The official Factur-X/ZUGFeRD sample invoices
published by FeRD (Germany) and FNFE-MPE (France) for the European
e-invoicing standard EN 16931, as collected in the ZUGFeRD corpus
(github.com/ZUGFeRD/corpus, commit
`84f8d8f68f6c3698aa3019d701a8b82db9ba0aac`, Apache-2.0). Each PDF carries
its invoice as CII XML, which gives exact ground truth, including the VAT
rate and EN 16931 VAT category per line and the VAT summary per rate.
Selection, applied in this order:

1. all PDFs in the corpus (151);
2. excluded: folders `fail/` (deliberately broken files) and
   `ZUGFeRDv1/` (format version without VAT detail);
3. excluded: PDFs without embedded CII XML, or without any VAT category;
4. excluded: duplicates, defined as the same invoice number and seller name
   (the same FeRD sample appears in several folders and versions).

That leaves 23 invoices with 53 lines: 18 from German sellers, 4 French,
1 British. VAT categories: 17 standard rate (S), 3 exempt (E), 2
intra-community supply (K), 1 export (G); 9 carry two VAT rates (7/19% or
5.5/20%); 2 are credit notes. No sample uses reverse charge (AE). The XML
was removed from each PDF before any engine saw it (only the pages were
copied to a new PDF), so that no engine could read the answer from the
attachment.

**SROIE receipts.** The ICDAR 2019 SROIE task 3 receipts: real scanned
till receipts from shops and restaurants in Malaysia, with four labelled
fields (company, date, address, total), in the copy published with labels
at github.com/zzzDavid/ICDAR-2019-SROIE (commit
`27be4271b251c256f695acbade9a801bffe85994`, 626 labelled receipts, MIT
licence on the repository). Berghaus et al. used the same copy. Each JPEG was
wrapped in a PDF as for Donut, and a fixed random sample of 100 was drawn
(seed 42). Dates are labelled day first in several formats; labels that are not a
plain day-first or ISO date would be left unscored (none in the sample). SROIE has no
VAT labels and no currency label; for receipts "bookable" means vendor
name, date and total right. SROIE was added after the first results, at the
research owner's request for real-world documents (section 8).

For all three sets, `truth.jsonl` records for every bill the source (dataset
and revision, or corpus commit and path) and the SHA-256 of the source
file.

### 4.2 Sets considered and not used

| Set | Reason |
|---|---|
| inv-cdip (scanned invoices of Berghaus et al.) | The UCSF Industry Documents Library refused automated download; also US documents without VAT |
| DocILE | English US documents, test labels not public |
| CORD | Phone photos of Indonesian receipts, but no store name and no date labelled |
| A synthetic EU VAT set of our own (150 bills, nine VAT scenarios) | Built, then discarded: a set we generate ourselves is not a standard and invites the suspicion of being tuned to a result |

### 4.3 Engines

| Engine | Model | Route |
|---|---|---|
| Odoo | Odoo Extract API, invoice route, API version 123 | `extract.api.odoo.com`, called directly with an IAP account token |
| Gemini 3.8 Flash | `google/gemini-3.8-flash` | OpenRouter, PDF passed natively |
| Gemini 3.1 Pro | `google/gemini-3.1-pro-preview` | same |
| Gemini 2.5 Pro | `google/gemini-2.5-pro` | same; the best model of Berghaus et al., as anchor |
| Claude Sonnet 5.5 | `anthropic/claude-sonnet-5.5` | same |
| GPT-5.5 | `openai/gpt-5.5` | same |
| Mistral OCR → Mistral Medium 3.5 | `mistralai/mistral-medium-3-5` | OpenRouter `file-parser` plugin with engine `mistral-ocr`: the page goes through Mistral OCR, the model gets its text |

All LLMs received the same one-paragraph prompt and the same JSON schema
(`src/bench_invoices.py`, `PROMPT` and `SCHEMA`), at temperature 0, with
structured output enforced. The prompt says the document is a bill
received from a supplier, asks for ISO dates and plain numbers, and asks
for null where a value is absent. The schema asks for the header fields,
the lines (description, quantity, unit price, VAT rate, net amount), the
VAT summary (rate, base, tax per rate) and the EN 16931 VAT category.

Odoo received what an Odoo database sends: `perspective: client` (the
bill was received) and the buyer's company name, VAT number and country as
`user_infos`, taken per bill from the ground truth, since a database always
knows its own company. Odoo's API returns no VAT category: in Odoo the
category follows from the vendor's fiscal position in the database, so that
field is not held against Odoo.

Model ids were checked against OpenRouter's model list on 2026-11-12, the
day all runs took place. Costs per call are OpenRouter's reported cost.
Odoo's cost is the price of one IAP credit, about EUR 0.13 at the pack size
used (an assumption; Odoo bills credits in packs). Seconds are wall-clock
time per bill, including Odoo's polling at 5-second intervals.

### 4.4 Outcomes

**Primary outcome: bookable without correction.** A bill counts as
bookable when every field an accountant needs to post it is right:

- the vendor: its VAT number when the bill has one, else its name;
- invoice number, invoice date, currency;
- untaxed amount, tax amount, total;
- the VAT summary: the base amount per VAT rate. Truth is the printed VAT
  table (EN 16931) or, where a bill has none, the sum of line amounts per
  rate (Donut). A prediction's summary is its VAT table if it gave one,
  else the sum of its line amounts per rate. One line per VAT rate is as
  bookable as many: Odoo itself offers that option.

Due date, IBAN and line descriptions serve payment and reading, not
booking, and are reported separately. A field whose truth is absent is not
scored.

**Secondary outcomes:** accuracy per field, all header fields together,
line fields (description, quantity, unit price, VAT rate) matched by
position, VAT rate per line, VAT category, cost and time per bill.

**Matching rules.** Amounts and quantities match within 0.005, compared by
absolute value. Dates are compared as ISO dates. VAT numbers are compared
without separators and without a leading country code. Codes (invoice
number, IBAN, currency) are compared upper-case without separators; a
currency sign counts as its ISO code. Names count when one contains the
other (after lower-casing and removing punctuation) or when their
similarity ratio is at least 0.9, and the prediction is at least 4
characters. Truth IBANs that fail the ISO 13616 checksum are not scored
(section 6.3).

**Statistics.** Proportions carry a 95% Wilson score interval. For field
accuracy the interval treats fields as independent, which they are not
within a bill; it is a lower bound on the uncertainty. Each LLM was run
three times on every bill; we report the mean and the range. Odoo was run
twice on all 123 bills, once without and once with the buyer hints, and
returned byte-identical answers both times, so one run is scored for all
three.

## 5. Results

Numbers below are from run 1 of 3. Square brackets give the 95% Wilson
interval of the bookable rate. "Line VAT rate" is the share of lines whose
VAT rate is right, matched by position; "VAT summary" the share of bills
whose base amount per VAT rate is right. When runs 2 and 3 are in, the
tables give the mean, with the range over runs in round brackets
(`results/<set>/aggregate.md`).

### 5.1 Donut invoices (100 bills)

| Engine | Bookable % | Header fields % | Line VAT rate % | VAT summary % | EUR / bill | s / bill |
|---|---|---|---|---|---|---|
| Odoo digitization | 0.0 [0 to 4] | 51.5 | 4.2 | 6.2 | 0.129 | 8 |
| Claude Sonnet 5.5 | 97.0 [92 to 99] | 99.5 | 100.0 | 99.0 | 0.009 | 4 |
| Gemini 3.1 Pro | 69.0 [59 to 77] | 96.1 | 100.0 | 99.0 | 0.026 | 21 |
| GPT-5.5 | 73.0 [64 to 81] | 96.2 | 100.0 | 99.0 | 0.022 | 9 |
| Gemini 2.5 Pro | 70.0 [60 to 78] | 96.1 | 100.0 | 99.0 | 0.017 | 16 |
| Gemini 3.8 Flash | 64.0 [54 to 73] | 95.5 | 100.0 | 99.0 | 0.004 | 10 |
| Mistral OCR → Mistral Medium 3.5 | 61.0 [51 to 70] | 95.0 | 100.0 | 99.0 | 0.006 | 4 |

Per field, % right:

| Field | Odoo | Claude | Gem 3.1 Pro | GPT-5.5 | Gem 2.5 Pro | Gem Flash | Mistral |
|---|---|---|---|---|---|---|---|
| vendor_name | 0 | 98 | 98 | 98 | 98 | 98 | 98 |
| vendor_vat | 2 | 100 | 100 | 100 | 100 | 100 | 95 |
| invoice_ref | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| invoice_date | 69 | 100 | 70 | 75 | 73 | 65 | 66 |
| currency | 100 | 100 | 100 | 100 | 98 | 100 | 100 |
| untaxed | 6 | 99 | 99 | 99 | 99 | 99 | 99 |
| tax | 6 | 100 | 100 | 100 | 100 | 100 | 100 |
| total | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| iban | 92 | 99 | 99 | 93 | 97 | 99 | 99 |

### 5.2 EN 16931 sample invoices (23 bills)

| Engine | Bookable % | Header fields % | Line VAT rate % | VAT summary % | EUR / bill | s / bill |
|---|---|---|---|---|---|---|
| Odoo digitization | 8.7 [2 to 27] | 66.8 | 37.7 | 95.7 | 0.129 | 7 |
| Claude Sonnet 5.5 | 95.7 [79 to 99] | 99.1 | 98.1 | 100.0 | 0.014 | 3 |
| Gemini 3.1 Pro | 100.0 [86 to 100] | 100.0 | 100.0 | 100.0 | 0.029 | 25 |
| GPT-5.5 | 100.0 [86 to 100] | 100.0 | 98.1 | 100.0 | 0.021 | 7 |
| Gemini 2.5 Pro | 95.7 [79 to 99] | 99.1 | 100.0 | 100.0 | 0.017 | 17 |
| Gemini 3.8 Flash | 100.0 [86 to 100] | 100.0 | 100.0 | 100.0 | 0.005 | 10 |
| Mistral OCR → Mistral Medium 3.5 | 91.3 [73 to 98] | 97.8 | 98.1 | 100.0 | 0.008 | 4 |

Per field, % right:

| Field | Odoo | Claude | Gem 3.1 Pro | GPT-5.5 | Gem 2.5 Pro | Gem Flash | Mistral |
|---|---|---|---|---|---|---|---|
| vendor_name | 9 | 100 | 100 | 100 | 100 | 100 | 100 |
| vendor_vat | 27 | 100 | 100 | 100 | 100 | 100 | 100 |
| invoice_ref | 52 | 100 | 100 | 100 | 100 | 100 | 100 |
| invoice_date | 52 | 96 | 100 | 100 | 96 | 100 | 96 |
| currency | 96 | 100 | 100 | 100 | 100 | 100 | 100 |
| untaxed | 96 | 100 | 100 | 100 | 100 | 100 | 100 |
| tax | 96 | 100 | 100 | 100 | 100 | 100 | 100 |
| total | 100 | 100 | 100 | 100 | 100 | 100 | 96 |
| due_date | 83 | 92 | 100 | 100 | 92 | 100 | 92 |
| iban | 57 | 100 | 100 | 100 | 100 | 100 | 71 |
| vat_treatment | - | 100 | 100 | 100 | 100 | 100 | 100 |

VAT category (EN 16931 code per bill) was right on 23 of 23 bills for every
language model. Odoo's API does not return it.

### 5.3 SROIE receipts (100 receipts)

<!-- RESULTS:SROIE -->

### 5.4 Under the original scoring rules

The same answers scored with the rules as first written (`--strict`, see
section 8). The ranking does not change; the language models lose 2 to 4
points on header fields, mostly on vendor names that carry a legal form,
Odoo loses 1 to 4.

**Donut**

| Engine | Bookable % | Header fields % | Line VAT rate % | VAT summary % | EUR / bill | s / bill |
|---|---|---|---|---|---|---|
| Odoo digitization | 0.0 [0 to 4] | 50.1 | 4.2 | 6.2 | 0.129 | 8 |
| Claude Sonnet 5.5 | 97.0 [92 to 99] | 96.9 | 100.0 | 99.0 | 0.009 | 4 |
| Gemini 3.1 Pro | 69.0 [59 to 77] | 93.5 | 100.0 | 99.0 | 0.026 | 21 |
| GPT-5.5 | 73.0 [64 to 81] | 93.6 | 100.0 | 99.0 | 0.022 | 9 |
| Gemini 2.5 Pro | 70.0 [60 to 78] | 93.5 | 100.0 | 99.0 | 0.017 | 16 |
| Gemini 3.8 Flash | 64.0 [54 to 73] | 92.9 | 100.0 | 99.0 | 0.004 | 10 |
| Mistral OCR → Mistral Medium 3.5 | 61.0 [51 to 70] | 92.5 | 100.0 | 99.0 | 0.006 | 4 |

**EN 16931**

| Engine | Bookable % | Header fields % | Line VAT rate % | VAT summary % | EUR / bill | s / bill |
|---|---|---|---|---|---|---|
| Odoo digitization | 8.7 [2 to 27] | 62.9 | 37.7 | 95.7 | 0.129 | 7 |
| Claude Sonnet 5.5 | 91.3 [73 to 98] | 95.6 | 98.1 | 100.0 | 0.014 | 3 |
| Gemini 3.1 Pro | 95.7 [79 to 99] | 96.5 | 100.0 | 100.0 | 0.029 | 25 |
| GPT-5.5 | 95.7 [79 to 99] | 96.5 | 98.1 | 100.0 | 0.021 | 7 |
| Gemini 2.5 Pro | 91.3 [73 to 98] | 95.6 | 100.0 | 100.0 | 0.017 | 17 |
| Gemini 3.8 Flash | 95.7 [79 to 99] | 96.1 | 100.0 | 100.0 | 0.005 | 10 |
| Mistral OCR → Mistral Medium 3.5 | 82.6 [63 to 93] | 93.9 | 98.1 | 100.0 | 0.008 | 4 |

### 5.5 Hypotheses

- **H1 supported.** Every language model produced more bookable bills than
  Odoo on both invoice sets, by a margin far outside the intervals: 0% for
  Odoo against 61 to 97% on Donut, 9% against 91 to 100% on EN 16931.
- **H2 weakly supported.** The OCR-first pipeline (Mistral OCR, then
  Mistral Medium) had the lowest bookable rate of the language models on
  both invoice sets (61% and 91%), but its intervals overlap those of most
  image-in models; only Claude Sonnet 5.5 is clearly ahead on Donut.


## 6. Discussion

### 6.1 Where Odoo goes wrong

- **Vendor.** Odoo's raw read named the vendor correctly on 0 of 100
  Donut bills and 2 of 23 EN 16931 bills. It often returns a heading as
  the vendor ("Invoice no", "Beispiel"). It found the vendor's VAT number on
  2% and 27% of the bills.
- **Invoice number and date.** On the EN 16931 bills, half the numbers and
  dates were wrong: Odoo returned another number on the page (a customer or
  order number) and another date (the delivery date).
- **Untaxed amount and tax.** On 93 of 99 Donut bills Odoo returned the total
  as the untaxed amount and 0 as the tax: it did not read the VAT column.
  On the EN 16931 bills it got both right on 22 of 23.
- **Lines.** Odoo returns one line per VAT rate, not the article lines (1.4
  lines per bill against 2.3 printed). Matched line by line that scores
  low; as a VAT summary it is right on 22 of 23 EN 16931 bills. Odoo itself
  offers "one line per tax" as a booking option, so for the accountant this
  is not a defect; the lost article detail is.

Totals and currency Odoo reads reliably (96 to 100%).

### 6.2 Where the language models go wrong

Almost every language-model error on Donut is a date. Donut prints US dates,
month first (09/10/2015). Claude Sonnet 5.5 read all 100 correctly; the
others read 25 to 35 of them day first. That alone makes the gap between
Claude (97% bookable) and the rest (61 to 73%). The same happened on the one
French EN 16931 sample that prints a US date. On European bills, where day
first is the norm, this costs little; telling the model the vendor's country
would likely remove most of it.

Apart from dates the models differ little on these clean documents: vendor,
VAT number, invoice number, amounts and VAT summary are at 98 to 100% for
all of them.

### 6.3 VAT

Every language model read the VAT rate of practically every line (98 to
100%), the VAT summary of every bill, and the EN 16931 VAT category of all
23 bills, including the mixed-rate, exempt, intra-community and export
cases. The set is small and has no reverse-charge bill, so this shows that
the models can read VAT, not how often they will on a company's real mix.

### 6.4 Cost and time

Per bill a language model cost EUR 0.004 (Gemini 3.8 Flash) to EUR 0.03
(Gemini 3.1 Pro); Odoo about EUR 0.13. Claude Sonnet 5.5 and the Mistral
pipeline answered in 3 to 4 seconds, Gemini 3.1 Pro in about 20. Odoo took 7
to 8 seconds, mostly waiting on its queue.

AI cost and human time are reported apart. AI cost is what was billed:
OpenRouter's reported cost per call for the language models, and the list
price of Odoo's smallest credit pack (100 credits for EUR 15) for Odoo.
Human time is the number of bills that are not bookable as read, times an
assumed two minutes to correct one (`results/<set>/aggregate.md`):

| Per 100 bills, run 1 | AI cost, Donut | To correct, Donut | AI cost, EN 16931 | To correct, EN 16931 |
|---|---|---|---|---|
| Odoo | EUR 15.00 | 100 bills, 3.3 h | EUR 15.00 | 91 bills, 3.0 h |
| Claude Sonnet 5.5 | EUR 0.92 | 3 bills, 0.1 h | EUR 1.41 | 4 bills, 0.1 h |
| Gemini 3.8 Flash | EUR 0.44 | 36 bills, 1.2 h | EUR 0.50 | 0 bills |
| GPT-5.5 | EUR 2.19 | 27 bills, 0.9 h | EUR 2.12 | 0 bills |
| Gemini 3.1 Pro | EUR 2.55 | 31 bills, 1.0 h | EUR 2.93 | 0 bills |
| Gemini 2.5 Pro | EUR 1.66 | 30 bills, 1.0 h | EUR 1.72 | 4 bills, 0.1 h |
| Mistral OCR → Medium | EUR 0.56 | 39 bills, 1.3 h | EUR 0.81 | 9 bills, 0.3 h |

The AI cost differs by a few euros per 100 bills; the time spent correcting
differs by hours. Unless an hour of correcting is worth less than a few
euros, the engine that is right most often is also the cheapest in total.
Between engines that are equally right, the AI cost decides (on EN 16931:
Gemini 3.8 Flash).

### 6.5 What this means for an Odoo user

Read raw, Odoo's digitization gives a draft that needs correcting on nearly
every bill in these sets, mostly the vendor, the number and the date, and on
US-style bills the tax. Inside a database the vendor lookup will recover part
of the vendor errors (section 7), but not the numbers, dates and taxes. A
current language model gets most of these bills right as read, at a quarter
of the price per call or less, and it saves hours of correcting per hundred
bills. Which model to pick depends on the
bills: on these sets Claude Sonnet 5.5 was the safest choice (best on the US
dates, at EUR 0.01 a bill), Gemini 3.8 Flash the cheapest where dates are
unambiguous. A follow-up on real Dutch vendor bills will tell for those.


### 6.3 The ground truth has errors too

In 25 of the 100 Donut bills of our sample, the IBAN in the ground truth
fails its own checksum ("GB82D)FU82ZI3146210425"): the labels were partly
produced by OCR. Every model read these IBANs as printed, and was marked
wrong. Berghaus et al. name IBAN as the hardest field on this set; part of
that difficulty is in the labels. We exclude such truths from scoring.

## 7. Limitations

- **Raw read, not the booked bill.** We scored what Odoo's Extract API
  returns. Inside a database Odoo also searches the vendor in the partner
  list (by VAT number, name, bank account) and applies the vendor's fiscal
  position and default taxes. The bill an accountant finally sees can be
  better than the raw read, or worse where defaults override a correct
  read. A follow-up study books real bills in a real database.
- **Mostly clean documents.** Both invoice sets are generated PDFs. The SROIE
  receipts are real scans, but flatbed scans of Malaysian till receipts, not
  phone photos of European bills. H2 is tested on clean invoices and on these
  scans only.
- **Small VAT set.** The EN 16931 set has 23 bills, mostly German, and no
  reverse-charge sample. Its VAT results show capability, not a rate that
  carries to a company's real mix of bills.
- **US conventions in Donut.** Donut prints US dates (month first), which
  European readers, human or model, misread when the day is 12 or less.
  This affects the date field and so the bookable rate.
- **Model drift.** Hosted models change behind the same name, and
  temperature 0 does not make their output deterministic. The run-to-run
  range shows the second; nothing here guards against the first.
- **Possible caching at Odoo.** Odoo's two runs were identical to the byte.
  The service may cache results per file, in which case our two runs are
  not independent evidence of determinism.
- **Scoring rules revised after a first look.** See section 8. Results under
  the original rules are published alongside (`*_strict.*`).

## 8. Deviations from the plan

| Planned (plan commit) | Done | Why |
|---|---|---|
| Fraunhofer's scanned set inv-cdip (`a889638`) | Not used | Automated download refused by the source library |
| A synthetic EU VAT set of our own (`ffa4567`) | Built, then removed (`32a3c5f`) | Not a standard set; decided by the research owner before any result on it |
| Primary outcome: header-field accuracy | Primary outcome: bookable without correction | Header-field accuracy does not answer the practical question; changed at the research owner's request after the first results, before the repeated runs |
| One run per engine | Three runs per LLM on the invoice sets, one on SROIE | To measure run-to-run variation; SROIE got one run within the budget |
| Two test sets | SROIE receipts added | Requested by the research owner after the first results, for real scanned documents |
| (not planned) | An exploratory run of all engines with an earlier schema (no VAT summary, no line amount) is not reported | It preceded the final schema; its numbers were within a few points of run 1 and led to the scoring revisions below |
| Scoring rules as first written | Four rules revised after inspecting the first LLM answers: (1) names match by containment, not prefix ("Au bon moulin" against "Au bon moulin SARL"); (2) amounts by absolute value (credit notes print negative amounts where the XML holds positive ones); (3) truth IBANs failing their checksum not scored; (4) the VAT summary added to the schema, since line amounts computed as quantity × price miss discounts | Each revision corrects a scoring error that marked a right answer wrong for every engine alike. The original rules remain available (`--strict`) and their results are published |

## 9. Reproducibility

All code is in `src/`, all raw answers of all engines in `results/`, with
the truth files and their source hashes. Scores can be recomputed from the
raw answers at no cost; the full study can be repeated with an OpenRouter
key and an Odoo IAP account (README). Runs took place on 2026-11-12 with
Python 3.13.18 and pypdf 7.0.1. Total cost: <!-- RESULTS:COST -->.

## 10. Conflict of interest

Pantalytics sells AI Pro, a module that runs language models inside Odoo,
and so has an interest in language models doing well against Odoo's own
service. To keep that interest from steering the result we used only
public data, wrote the hypotheses down before collecting it, publish every
raw answer and the scoring under the original rules, and give the code to
anyone who wants to check it.

## References

- Berghaus, D., Berger, A., Hillebrand, L., Cvejoski, K., Sifa, R. (2025).
  Multi-Modal Vision vs. Text-Based Parsing: Benchmarking LLM Strategies for
  Invoice Processing. arXiv:2509.04469.
- Kim, G. et al. (2022). OCR-free Document Understanding Transformer.
  ECCV 2022.
- Šimsa, Š. et al. (2023). DocILE Benchmark for Document Information
  Localization and Extraction. ICDAR 2023. arXiv:2302.05658.
- Gao, M. et al. (2022). Field Extraction from Forms with Unlabeled Data
  (inv-cdip). github.com/salesforce/inv-cdip.
- CEN (2017). EN 16931-1: Electronic invoicing, semantic data model.
- Odoo S.A. Extract API, Odoo 19.0 documentation; In-App Purchase privacy
  policy, iap.odoo.com/privacy (consulted 2026-11-12).
- Mistral AI (2026). Mistral OCR 4 announcement, as reported by VentureBeat,
  2026-06-24.
