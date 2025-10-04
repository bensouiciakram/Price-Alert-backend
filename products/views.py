from typing import List 
from django.db import transaction
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin
from rest_framework.views import APIView 
from .serializers import (
    WebsiteSerializer,
    ProductSerializer,
    PriceHistorySerializer,
    XpathSerializer
)

from .models import (
    Website,
    Product,
    PriceHistory,
    Xpath 
)
from generic_scrapers import (
    PlaywrightExtractor,
    scrape_product_metadata,
    RequestsExtractor
)


class WebsiteViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    queryset = Website.objects.all() 
    serializer_class=WebsiteSerializer


class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer


class PriceHistoryViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    queryset=PriceHistory.objects.all()
    serializer_class=PriceHistorySerializer


class XpathViewSet(UpdateModelMixin,ListModelMixin,CreateModelMixin,GenericViewSet):
    queryset = Xpath.objects.all()
    serializer_class=XpathSerializer

class ScrapeMetaData(APIView):

    def get_product_metadata(self,request) -> List[dict]:
        website = request.data.get('url')
        price_xpath = request.data.get('price_xpath')
        image_xpath = request.data.get('image_xpath')
        title_xpath = request.data.get('title_xpath')
        price_cleanup = request.data.get('price_cleanup')
        image_cleanup = request.data.get('image_cleanup')
        title_cleanup = request.data.get('title_cleanup')
        library = request.data.get('library')
        if library == 'Scrapy':
            results = scrape_product_metadata(
                url=website,
                price_xpath=price_xpath,
                title_xpath=title_xpath,
                image_xpath=image_xpath,
                price_cleanup=price_cleanup,
                title_cleanup=title_cleanup,
                image_cleanup=image_cleanup
            )
        elif library == 'Playwright':
            extractor = PlaywrightExtractor(
                url=website,
                price_xpath=price_xpath,
                title_xpath=title_xpath,
                image_xpath=image_xpath,
                price_cleanup=price_cleanup,
                title_cleanup=title_cleanup,
                image_cleanup=image_cleanup
            )
            results = extractor.scrape_product_metadata()
        elif library == 'Requests':
            extractor = RequestsExtractor(
                url=website,
                price_xpath=price_xpath,
                title_xpath=title_xpath,
                image_xpath=image_xpath,
                price_cleanup=price_cleanup,
                title_cleanup=title_cleanup,
                image_cleanup=image_cleanup
            )
            results = extractor.scrape_product_metadata()
        return results 
    
    def post(self,request):
        if Website.objects.filter(domain=request.url).exists():
            return Response({
                'message':'Scraper is already exists'
            })
        results = self.get_product_metadata(request)
        return Response(results)
    

class AddNewScraper(APIView):

    def post(self,request):
        if Website.objects.filter(url=request.data.get('url')).exists():
            return Response(
                {
                    'message':'The Scraper is already exist'
                }
            )
        with transaction.atomic():
            website = Website.objects.create(
                url=request.data.get('url'),
                scraping_method=request.data.get('scraping_method')
            )
            Xpath.objects.create(
                website=website,
                price_selector=request.data.get('price_selector'),
                image_selector=request.data.get('image_selector'),
                title_selector=request.data.get('title_selector'),
                price_cleanup=request.data.get('price_cleanup'),
                title_cleanup=request.data.get('title_cleanup'),
                image_cleanup=request.data.get('image_cleanup'),
            )
            return Response(
                {
                'message':'success'
                }
            )