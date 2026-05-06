import csv
import os
import re
from datetime import datetime

def _to_float(s):
    """Safe string->float for values like '1,234.5678' or '1 234.5678'."""
    if s is None:
        return None
    txt = str(s).strip()
    if not txt:
        return None
    # Remove commas/spaces; keep dot
    txt = re.sub(r"[,\s]", "", txt)
    try:
        return float(txt)
    except Exception:
        return None

class CSVPipeline:
    def __init__(self):
        self.csv_file = 'xe_rates_output.csv'
        self.file_handle = None
        self.writer = None
        self.file_exists = os.path.exists(self.csv_file)

    def open_spider(self, spider):
        """Open CSV file and write header if new file."""
        self.file_handle = open(self.csv_file, 'a', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(
            self.file_handle,
            fieldnames=['date', 'source_country', 'currency', 'currency_name', 'rate', 'inverse_rate']
        )
        
        # Write header only if file is new
        if not self.file_exists:
            self.writer.writeheader()
        
        spider.logger.info(f"CSV Pipeline opened: {self.csv_file}")

    def close_spider(self, spider):
        """Close CSV file."""
        if self.file_handle:
            self.file_handle.close()
        spider.logger.info(f"CSV Pipeline closed. Data saved to: {self.csv_file}")

    def process_item(self, item, spider):
        """Write item to CSV file."""
        currency = (item.get("currency") or "").upper()
        if not currency:
            spider.logger.debug(f"Skipping row with no currency: {item}")
            return item

        source = (item.get("source_country") or "").upper()
        date = item.get("date")
        rate = _to_float(item.get("rate"))
        inv = _to_float(item.get("inverse_rate"))
        currency_name = item.get("currency_name", "")

        try:
            self.writer.writerow({
                'date': date,
                'source_country': source,
                'currency': currency,
                'currency_name': currency_name,
                'rate': rate,
                'inverse_rate': inv
            })
            self.file_handle.flush()
            spider.logger.info(f"✅ Written to CSV: {source}/{currency} on {date}, rate={rate}")
        except Exception as e:
            spider.logger.error(f"❌ Error writing to CSV: {e}")

        return item