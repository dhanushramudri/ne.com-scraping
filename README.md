
````markdown
# XE.com Exchange Rate Scraper

Scrapes historical exchange rates from XE.com and exports to CSV.

- 160+ currencies per request (fiat, crypto, metals)
- 27 source currencies
- Date range support with month-by-month batch runner
- Resume support if interrupted

## Requirements

- Windows
- Python 3.9+
- ~1GB disk space per year of data

## Installation

```bash
git clone https://github.com/dhanushramudri/ne.com-scraping.git
cd ne.com-scraping

pip install -r requirements.txt
````

## Usage

**Single day:**

```bash
scrapy crawl xe.com -a start=2026-05-05 -a end=2026-05-05
```

**Date range:**

```bash
scrapy crawl xe.com -a start=2026-04-01 -a end=2026-04-31
```

**Large range with resume (recommended for multi-month):**

```bash
python run_batches.py --start 2020-01-01 --end 2026-05-06 --retries 2
```

## Output

File: `xe_rates_output.csv`

```
date,source_country,currency,currency_name,rate,inverse_rate
2026-05-05,GBP,USD,US Dollar,1.3575479295226776,0.7366222423922861
2026-05-05,GBP,EUR,Euro,1.1595313076786709,0.862417421054335
2026-05-05,GBP,JPY,Japanese Yen,214.05505348099095,0.00467169535938475
```

## Test Commands

**Verify single day works:**

```bash
scrapy crawl xe.com -a start=2026-05-05 -a end=2026-05-05 -s LOG_LEVEL=INFO
```

**Verify output file was created:**

```bash
dir xe_rates_output.csv
```


## Batch Runner Options

```bash
python run_batches.py \
  --start 2020-01-01 \
  --end 2026-05-06 \
  --sleep-min 5 \
  --sleep-max 15 \
  --retries 3 \
  --resume-file months_done.txt
```





## Troubleshooting

**`scrapy: command not found`** — ensure Python and dependencies are installed and added to PATH.

**HTTP 403 errors** — use `run_batches.py` with `--retries 3` instead of running the spider directly.

**No rows found** — run with `LOG_LEVEL=DEBUG` and check if XE.com table structure changed.

**Data goes back to:** April 2013

