import re

data = """
'scrapy.spidermiddlewares.referer.RefererMiddleware',

'scrapy.spidermiddlewares.urllength.UrlLengthMiddleware',

'scrapy.spidermiddlewares.depth.DepthMiddleware']

2020-05-08 14:31:25 [scrapy.middleware] INFO: Enabled item pipelines:

['parsers.pipelines.YandexOrganizationPipeline']

2020-05-08 14:31:25 [scrapy.core.engine] INFO: Spider opened

2020-05-08 14:31:25 [scrapy.extensions.logstats] INFO: Crawled 0 pages (at 0 pages/min), scraped 0 items (at 0 items/min)

2020-05-08 14:31:25 [scrapy.extensions.telnet] INFO: Telnet console listening on 127.0.0.1:6023

2020-05-08 14:31:25 [yandex_organization] INFO: QUERY <<Алейск: Землеустройство, Кадастр>>

2020-05-08 14:31:25 [yandex_organization] INFO: YandexOrganizationSpider | Начали парсинг Алейск: Землеустройство, Кадастр initial_depth=0

2020-05-08 14:31:25 [yandex_organization] INFO: ProxyTorMiddleware | process_request | Request url | https://yandex.ru/maps/api/search?add_type=direct&ajax=1&client_usecase=suggest&csrfToken=&lang=ru_RU&ll=82.787762%2C52.5062585&origin=maps-
"""

RAW_QUERY_INFO = 'QUERY <<(.*?)>>'

query_raw = data[0:4096]
print(RAW_QUERY_INFO)
match = re.findall(RAW_QUERY_INFO, query_raw, re.DOTALL)
print(match)
if match:
    print(match[0].strip())