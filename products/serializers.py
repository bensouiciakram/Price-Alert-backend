from rest_framework import serializers 
from .models import (
    Website,
    Product,
    PriceHistory,
    Xpath
)


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website 
        fields = ['url']


class ProductSerializer(serializers.ModelSerializer):
    website = WebsiteSerializer()
    class Meta:
        model=Product
        fields=['id','url','created_at','website','alerts'] 


class PriceHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model=PriceHistory
        fields=['price','checked_at','product']


class XpathSerializer(serializers.ModelSerializer):
    class Meta:
        model=Xpath
        fields=['website','price_selector','title_selector','image_selector']


