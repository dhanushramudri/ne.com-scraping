import scrapy
import datetime as dt
from xescraper.items import XeRawItem

def daterange_days(start: dt.date, end: dt.date):
    """Yield YYYY-MM-DD strings for each day (inclusive) between start and end."""
    curr = start
    one = dt.timedelta(days=1)
    while curr <= end:
        yield curr.isoformat()
        curr += one

class XeSpider(scrapy.Spider):
    name = "xe.com"
    allowed_domains = ["xe.com"]

    # Only these sources; no 'USD' as a source
    source_country = ["GBP", "AUD", "EUR", "CAD"]

    # Let Scrapy pass -a start=... -a end=... into __init__
    def __init__(self, start=None, end=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default if not provided (you can adjust)
        default_start = dt.date(2013, 4, 1)
        default_end   = dt.date(2013, 4, 30)

        if start:
            y, m, d = map(int, start.split("-"))
            self.start_date = dt.date(y, m, d)
        else:
            self.start_date = default_start

        if end:
            y, m, d = map(int, end.split("-"))
            self.end_date = dt.date(y, m, d)
        else:
            self.end_date = default_end

        if self.end_date < self.start_date:
            raise ValueError(f"end ({self.end_date}) is before start ({self.start_date})")

    def start_requests(self):
        for source in self.source_country:
            for day in daterange_days(self.start_date, self.end_date):
                url = f"https://www.xe.com/currencytables/?from={source}&date={day}"
                yield scrapy.Request(
                    url,
                    callback=self.parse,
                    meta={"date": day, "source_country": source},
                    dont_filter=True,
                )

    def parse(self, response):
        date = response.meta["date"]
        source_country = response.meta["source_country"]

        # Grab the data table rows
        rows = response.css("div#table-section table tbody tr")
        if not rows:
            self.logger.error(f"No rows found in {response.url}")
            return

        # Only the USD row
        for row in rows:
            currency = (row.css("th[scope='row'] a::text").get() or "").strip()
            if currency != "USD":
                continue

            currency_name = (row.css("td:nth-child(2)::text").get() or "").strip()
            rate = (row.css("td:nth-child(3)::text").get() or "").strip()
            inverse_rate = (row.css("td:nth-child(4)::text").get() or "").strip()

            self.logger.info(
                f"Extracted [{source_country}/USD] {date}: {currency_name}, rate={rate}, inverse={inverse_rate}"
            )

            item = XeRawItem()
            item["currency"] = "USD"
            item["currency_name"] = currency_name
            item["rate"] = rate                # source -> USD
            item["inverse_rate"] = inverse_rate  # USD -> source
            item["date"] = date
            item["source_country"] = source_country

            if item["currency"] and item["rate"]:
                yield item