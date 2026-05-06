# XE.com Exchange Rate Scraper (CSV/Excel Export)

Scrapes historical exchange rates from [XE.com](https://www.xe.com/) for four currency pairs — **GBP/USD, AUD/USD, CAD/USD, EUR/USD** — and saves them directly to CSV/Excel files.

## Features
- ✅ Daily rates from any date range
- ✅ Exports to CSV (append mode)
- ✅ Handles HTTP 403 errors with retry logic
- ✅ Month-by-month batch runner with resume support
- ✅ No database required
- ✅ Fast and lightweight

## Installation

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/xe-scraper-csv.git
cd xe-scraper-csv

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt