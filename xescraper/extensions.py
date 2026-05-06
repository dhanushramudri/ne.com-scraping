from scrapy import signals
from xescraper.terminal_ui import ui


class XeUIExtension:
    """Scrapy extension that drives the terminal UI."""

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_opened,  signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed,  signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped,   signal=signals.item_scraped)
        crawler.signals.connect(ext.response_received, signal=signals.response_received)
        crawler.signals.connect(ext.spider_error,   signal=signals.spider_error)
        return ext

    def spider_opened(self, spider):
        start = getattr(spider, "start_date", "?")
        end   = getattr(spider, "end_date",   "?")
        sources = getattr(spider, "source_country", [])
        ui.stats["total_requests"] = len(sources) * max(
            1, (getattr(spider, "end_date", None) - getattr(spider, "start_date", None)).days + 1
            if hasattr(spider, "start_date") and hasattr(spider, "end_date")
            else 1
        )
        ui.log(f"Spider opened — {start} → {end} | {len(sources)} sources")
        ui.start()

    def spider_closed(self, spider, reason):
        ui.log(f"Spider closed: [bold]{reason}[/bold]")
        ui.stop()

    def response_received(self, response, request, spider):
        date   = request.meta.get("date", "")
        source = request.meta.get("source_country", "")
        ui.stats["completed_requests"] += 1
        ui.stats["current_date"]   = date
        ui.stats["current_source"] = source
        if source:
            ui.source_progress[source]["done"] += 1
        ui.log(f"[green]↓[/green] {source} / {date} — {response.status}")
        ui.update()

    def item_scraped(self, item, response, spider):
        source = (item.get("source_country") or "").upper()
        currency = (item.get("currency") or "").upper()
        ui.stats["total_rows"] += 1
        if source:
            ui.source_progress[source]["rows"] += 1
        if ui.stats["total_rows"] % 50 == 0:
            ui.log(f"[cyan]📦[/cyan] {ui.stats['total_rows']:,} rows collected")
            ui.update()

    def spider_error(self, failure, response, spider):
        ui.stats["errors"] += 1
        ui.log(f"[red]❌ Error:[/red] {str(failure.value)[:60]}")
        ui.update()