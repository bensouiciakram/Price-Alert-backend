import argparse
from re import sub 
from camoufox.sync_api import Camoufox
from parsel import Selector 
from .base import BaseExtractor

class Extractor(BaseExtractor):

    def get_response(self) -> Selector :
        super().get_response()
        with Camoufox(headless=True,slow_mo=1000) as browser:
            page = browser.new_page()
            page.goto(self.url)
            # page.wait_for_selector(self.title_xpath)
            return Selector(text=page.content())

