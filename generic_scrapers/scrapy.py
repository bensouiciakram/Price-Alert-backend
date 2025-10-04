import argparse
from re import sub
from typing import List 
import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess


class GenericSpider(scrapy.Spider):
    name = "generic"

    def __init__(self, url, price_xpath, title_xpath, image_xpath,
                 price_cleanup=None, title_cleanup=None, image_cleanup=None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [url]
        self.price_xpath = price_xpath
        self.title_xpath = title_xpath
        self.image_xpath = image_xpath
        self.price_cleanup = price_cleanup
        self.title_cleanup = title_cleanup
        self.image_cleanup = image_cleanup

    def parse(self, response):
        price = response.xpath(self.price_xpath).get()
        title = response.xpath(self.title_xpath).get()
        image = response.xpath(self.image_xpath).get()

        item = {
            "price": sub(self.price_cleanup, "", price) if self.price_cleanup else price,
            "title": sub(self.title_cleanup, "", title) if self.title_cleanup else title,
            "image": sub(self.image_cleanup, "", image) if self.image_cleanup else image,
        }
        self.results.append(item)
        yield item 


def scrape_product_metadata(**kwargs) -> List[dict]:
    results = []
    process = CrawlerProcess(settings={"LOG_ENABLED": False})
    process.crawl(GenericSpider, results=results, **kwargs)
    process.start()
    return results