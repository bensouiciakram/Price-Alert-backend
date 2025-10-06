from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.db import transaction
from .models import Alert 
from products.models import (
    Xpath,
    PriceHistory
) 
from generic_scrapers import (
    PlaywrightExtractor,
    RequestsExtractor,
    scrape_product_metadata,
)

def set_periodic_scraping(alert_id:int):
    with transaction.atomic():
        alert = Alert.objects.get(id=alert_id)
        frequency = alert.frequency
        product_url = alert.product.url
        website = alert.product.website
        scrapy_method = website.scraping_method
        xpath = Xpath.objects.filter(website=website).first()
        if scrapy_method == 'playwright':
            extractor = PlaywrightExtractor(
                url=product_url,
                price_xpath=xpath.price_selector,
                title_xpath=xpath.title_selector,
                image_xpath=xpath.image_selector,
                price_cleanup=xpath.price_cleanup,
                title_cleanup=xpath.title_cleanup,
                image_cleanup=xpath.image_cleanup,
            )
            result = extractor.scrape_product_metadata()
        elif scrapy_method == 'scrapy':
            result = scrape_product_metadata(
                url=product_url,
                price_xpath=xpath.price_selector,
                title_xpath=xpath.title_selector,
                image_xpath=xpath.image_selector,
                price_cleanup=xpath.price_cleanup,
                title_cleanup=xpath.title_cleanup,
                image_cleanup=xpath.image_cleanup,
            )[0]
        elif scrapy_method == 'requests':
            extractor = RequestsExtractor(
                url=product_url,
                price_xpath=xpath.price_selector,
                title_xpath=xpath.title_selector,
                image_xpath=xpath.image_selector,
                price_cleanup=xpath.price_cleanup,
                title_cleanup=xpath.title_cleanup,
                image_cleanup=xpath.image_cleanup,
                )
            result = extractor.scrape_product_metadata()
        PriceHistory.objects.create(
            price=result.get('price'),
            product=alert.product
        )
