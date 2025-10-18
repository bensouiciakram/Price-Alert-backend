import os
import logging
from typing import List
from urllib.parse import urlparse
from django.db import transaction
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
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
from alert.models import Alert, Channel
from generic_scrapers import PlaywrightExtractor, RequestsExtractor

logger = logging.getLogger(__name__)


class WebsiteViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer

    def create(self, request, *args, **kwargs):
        logger.info("Received request to create new website entry.")
        return super().create(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        logger.info(f"Deleting product ID {product.id}, URL: {product.url}")
        return super().destroy(request, *args, **kwargs)


class PriceHistoryViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = PriceHistory.objects.all()
    serializer_class = PriceHistorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='latest_price')
    def latest_price(self, request):
        product_id = request.data.get('product_id')
        logger.debug(f"Fetching latest price for product ID {product_id}")
        price_object = PriceHistory.objects.filter(product=product_id).first()

        if not price_object:
            logger.warning(f"No price history found for product ID {product_id}")
            return Response(
                {'message': 'No price history found'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({
            'product_id': product_id,
            'last_price': price_object.price,
            'checked_at': price_object.checked_at.strftime("%y-%m-%d %H:%M:%S")
        }, status=status.HTTP_200_OK)


class XpathViewSet(UpdateModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Xpath.objects.all()
    serializer_class = XpathSerializer
    permission_classes = [IsAuthenticated]


class CurrrencyViewSet(ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class AddProduct(APIView):
    permission_classes = [IsAuthenticated]

    def get_website_url(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def get_product_metadata(
        self,
        website: str,
        price_xpath: str,
        image_xpath: str,
        title_xpath: str,
        price_cleanup: str,
        image_cleanup: str,
        title_cleanup: str,
        library: str
    ) -> dict:
        logger.debug(f"Extracting product metadata from {website} using {library}.")
        try:
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
            else:
                logger.error(f"Unknown library '{library}' used for extraction.")
                return {}
            return extractor.scrape_product_metadata()
        except Exception as e:
            logger.exception(f"Failed to extract metadata for {website}: {e}")
            return {}

    def post(self, request):
        user = request.user.username
        logger.info(f"[User: {user}] Requested to add a new product.")

        product_url = request.data.get('product_url')
        website_url = self.get_website_url(product_url)

        website_qs = Website.objects.filter(url=website_url)
        if not website_qs.exists():
            logger.warning(f"Website {website_url} not supported.")
            return Response({'message': 'Website is not supported'}, status=status.HTTP_400_BAD_REQUEST)

        website = website_qs.first()

        if Product.objects.filter(url=product_url).exists():
            logger.info(f"Product already exists for URL {product_url}")
            return Response({'message': 'Product is already added'}, status=status.HTTP_200_OK)

        xpath = Xpath.objects.filter(website=website).first()
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

        if not result:
            logger.error(f"Failed to retrieve metadata for {product_url}")
            return Response({'message': 'Failed to fetch product data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            with transaction.atomic():
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
                PriceHistory.objects.create(
                    price=result.get('price'),
                    product=product
                )
                logger.info(f"Successfully added new product: {product_url}")
                return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(f"Transaction failed while adding product {product_url}: {e}")
            return Response({'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddNewScraper(APIView):
    def post(self, request):
        logger.info("Received request to register new scraper.")
        if Website.objects.filter(url=request.data.get('url')).exists():
            logger.warning(f"Scraper already exists for URL {request.data.get('url')}")
            return Response({'message': 'The Scraper already exists'}, status=status.HTTP_200_OK)

        data = request.data
        try:
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
                logger.info(f"Successfully registered new scraper for {website.url}")
                return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(f"Failed to create scraper for {data.get('url')}: {e}")
            return Response({'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
