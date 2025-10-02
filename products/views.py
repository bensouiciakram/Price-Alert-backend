from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from .serializers import (
    WebsiteSerializer,
    ProductSerializer,
    PriceSerializer,
    FieldSerializer,
    XpathSerializer
)

from .models import (
    Website,
    Product,
    Price,
    Field,
    Xpath 
)

class WebsiteViewSet(ModelViewSet):
    queryset = Website.objects.all() 
    serializer_class=WebsiteSerializer


class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer


class PriceViewSet(ModelViewSet):
    queryset=Price.objects.all()
    serializer_class=PriceSerializer


class FieldViewSet(ModelViewSet):
    queryset=Field.objects.all()
    serializer_class = FieldSerializer


class XpathViewSet(ModelViewSet):
    queryset = Xpath.objects.all()
    serializer_class=XpathSerializer