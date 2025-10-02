from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin
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