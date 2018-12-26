from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lefigaro.spiders.lefigarospider import LefigarospiderSpider

process = CrawlerProcess(get_project_settings())
process.crawl(LefigarospiderSpider)
process.start()
