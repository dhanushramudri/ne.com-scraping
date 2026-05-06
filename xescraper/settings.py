BOT_NAME = "xescraper"

SPIDER_MODULES = ["xescraper.spiders"]
NEWSPIDER_MODULE = "xescraper.spiders"

LOG_LEVEL = "WARNING"
LOG_ENABLED = True
LOG_FILE = "scraper.log"      

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'xescraper.pipelines_csv.CSVPipeline': 300,
}

EXTENSIONS = {
    'xescraper.extensions.XeUIExtension': 500,
}

FEED_EXPORT_ENCODING = "utf-8"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"