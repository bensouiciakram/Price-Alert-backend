import argparse
from re import sub 
import requests 
from parsel import Selector

from generic_scrapers.base import BaseExtractor 

class Extractor(BaseExtractor):
    def get_response(self) -> Selector:
        super().get_response()
        return Selector(
            text=requests.get(self.url).text
        )
