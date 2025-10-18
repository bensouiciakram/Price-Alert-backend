import logging
from camoufox.sync_api import Camoufox
from parsel import Selector
from .base import BaseExtractor

logger = logging.getLogger(__name__)


class Extractor(BaseExtractor):
    def get_response(self) -> Selector:
        logger.debug(f"Fetching page with Playwright: {self.url}")
        super().get_response()
        with Camoufox(headless=True, slow_mo=1000) as browser:
            page = browser.new_page()
            page.goto(self.url)
            logger.debug(f"Page loaded successfully (Playwright): {self.url}")
            return Selector(text=page.content())
