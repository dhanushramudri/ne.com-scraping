# XE.com Exchange Rate Scraper (CSV/Excel Export)



Scrapes historical exchange rates from [XE.com](https://www.xe.com/) for four currency pairs — **GBP/USD, AUD/USD, CAD/USD, EUR/USD** — and saves them directly to CSV files.

Perfect for financial analysis, currency tracking, and automated data collection without database setup.

## 🌟 Features

- ✅ **Daily rates from any date range** - From 2013 to present
- ✅ **Direct CSV export** - No database required, append mode
- ✅ **Handles HTTP 403 errors** - Automatic retry with exponential backoff
- ✅ **Month-by-month batch runner** - Resume support for long runs
- ✅ **Fast & lightweight** - Pure Python with Scrapy
- ✅ **Four currency pairs** - GBP/USD, AUD/USD, EUR/USD, CAD/USD

## 📋 Requirements

- Python 3.9+
- Windows / macOS / Linux
- ~200MB disk space for 10 years of data

## 🚀 Quick Start (5 Minutes)

### Step 1: Clone Repository

```bash
git clone https://github.com/dhanushramudri/ne.com-scraping.git
cd ne.com-scraping/xe-scraper-csv






Install Deps: 

pip install -r requirements.txt


Expected output : Successfully installed scrapy-2.13.2 pandas-2.2.0 openpyxl-3.1.0 ...
 

Test Single Day

scrapy crawl xe.com -a start=2026-05-05 -a end=2026-05-05 -s LOG_LEVEL=INFO
