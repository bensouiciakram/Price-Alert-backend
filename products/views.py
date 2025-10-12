import os 
from typing import List 
from urllib.parse import urlparse 
from django.db import transaction
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import status 
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin
from rest_framework.views import APIView 
from .serializers import (
    CurrencySerializer,
    WebsiteSerializer,
    ProductSerializer,
    PriceHistorySerializer,
    XpathSerializer
)

from .models import (
    Currency,
    Website,
    Product,
    ProductMetaData,
    PriceHistory,
    Xpath 
)
from alert.models import (
    Alert,
    Channel
)
from generic_scrapers import (
    PlaywrightExtractor,
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

    @action(detail=False, methods=['post'], url_path='latest_price')
    def latest_price(self, request):
        product_id = request.data.get('product_id')
        price_object = PriceHistory.objects.filter(product=product_id).first()

        return Response({
            'product_id':product_id,
            'last_price':price_object.price,
            'checked_at':price_object.checked_at.strftime("%y-%m-%d %H:%M:%S")
        }, status=status.HTTP_200_OK)


class XpathViewSet(UpdateModelMixin,ListModelMixin,CreateModelMixin,GenericViewSet):
    queryset = Xpath.objects.all()
    serializer_class=XpathSerializer

class CurrrencyViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class AddProduct(APIView):

    def get_website_url(self,url:str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def get_product_metadata(
            self,
            website:str,
            price_xpath:str,
            image_xpath:str,
            title_xpath:str,
            price_cleanup:str,
            image_cleanup:str,
            title_cleanup:str,
            library:str
        ) -> dict:
        if library == 'playwright':
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
        elif library == 'requests':
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

        website_qs:Website = Website.objects.filter(url=self.get_website_url(request.data.get('product_url')))
        if not website_qs.exists():
            return Response(
                {
                    'message':'Website is not supported'
                }
            )
        website = website_qs.first()
        product_url = request.data.get('product_url')
        product_sq = Product.objects.filter(url=product_url)
        if product_sq.exists():
            return Response(
                {
                    'message':'Product is already added'
                }
            )
        product = product_sq.first()
        xpath = Xpath.objects.filter(website=website).first()
        with transaction.atomic():
            result = self.get_product_metadata(
                website=product_url,
                price_xpath=xpath.price_selector,
                image_xpath=xpath.image_selector,
                title_xpath=xpath.title_selector,
                price_cleanup=xpath.price_cleanup,
                title_cleanup=xpath.title_cleanup,
                image_cleanup=xpath.image_cleanup,
                library=website.scraping_method
            )
            product_metadata = ProductMetaData.objects.create(
                title=result.get('title'),
                image=result.get('image'),
            )
            product = Product.objects.create(
                url=product_url,
                website=website,
                meta=product_metadata
            )
            channel = Channel.objects.filter(name=request.data.get('channel')).first()
            Alert.objects.create(
                threshold=request.data.get('threshold'),
                frequency=request.data.get('frequency'),
                channel=channel,
                product=product
            )
            price_history = PriceHistory.objects.create(
                price=result.get('price'),
                product=product
            )
            return Response(
                {
                    'message':'success'
                }
            )

    

class AddNewScraper(APIView):
    def post(self,request):
        if Website.objects.filter(url=request.data.get('url')).exists():
            return Response(
                {
                    'message':'The Scraper is already exist'
                }
            )
        data = request.data 
        with transaction.atomic():
            website = Website.objects.create(
                url=data.get('url'),
                scraping_method=data.get('scraping_method'),
                currency_id=data.get('currency')
            )
            Xpath.objects.create(
                website=website,
                price_selector=data.get('price_selector'),
                image_selector=data.get('image_selector'),
                title_selector=data.get('title_selector'),
                price_cleanup=data.get('price_cleanup'),
                title_cleanup=data.get('title_cleanup'),
                image_cleanup=data.get('image_cleanup'),
            )
            return Response(
                {
                'message':'success'
                }
            )
        

