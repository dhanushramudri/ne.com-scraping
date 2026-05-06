import scrapy

class XeRawItem(scrapy.Item):
    date = scrapy.Field()
    currency = scrapy.Field()         # Target currency (ANY currency - fiat, crypto, metals)
    currency_name = scrapy.Field()    # Full name from table
    rate = scrapy.Field()             # source → target rate
    inverse_rate = scrapy.Field()     # target → source rate
    source_country = scrapy.Field()   # Source currency (GBP, AUD, EUR, USD, etc.)