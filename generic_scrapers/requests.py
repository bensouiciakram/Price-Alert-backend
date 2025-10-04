import argparse
from re import sub 
import requests 
from parsel import Selector 

class Extractor:
    def __init__(self, url, price_xpath, title_xpath, image_xpath,
                 price_cleanup=None, title_cleanup=None, image_cleanup=None, **kwargs):
        self.url = url
        self.price_xpath = price_xpath
        self.title_xpath = title_xpath
        self.image_xpath = image_xpath
        self.price_cleanup = price_cleanup
        self.title_cleanup = title_cleanup
        self.image_cleanup = image_cleanup

    def scrape_product_metadata(self) -> dict :
        response = requests.get(self.url)
        page_selector = Selector(text=response.text)
        price = page_selector.xpath(self.price_xpath).get()
        title = page_selector.xpath(self.title_xpath).get()
        image = page_selector.xpath(self.image_xpath).get()

        return {
            "price": sub(self.price_cleanup, "", price) if self.price_cleanup else price,
            "title": sub(self.title_cleanup, "", title) if self.title_cleanup else title,
            "image": sub(self.image_cleanup, "", image) if self.image_cleanup else image,
        }

