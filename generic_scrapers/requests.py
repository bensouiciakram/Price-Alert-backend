import logging
import requests
from parsel import Selector
from generic_scrapers.base import BaseExtractor

logger = logging.getLogger(__name__)


class Extractor(BaseExtractor):
    def get_response(self) -> Selector:
        logger.debug(f"Fetching page with Requests: {self.url}")
        super().get_response()
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            logger.debug(f"Request successful (status={response.status_code}) for {self.url}")
            return Selector(text=response.text)
        except Exception as e:
            logger.exception(f"Request failed for {self.url}: {e}")
            raise
