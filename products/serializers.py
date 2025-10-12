from rest_framework import serializers 
from .models import (
    Website,
    Product,
    ProductMetaData,
    PriceHistory,
    Xpath,
    Currency
)

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency 
        fields = [
            'id',
            'currency_name',
            'currency_symbol'
        ]

class WebsiteSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    class Meta:
        model = Website 
        fields = ['url','currency']

class ProductMetaDataSerializer(serializers.ModelSerializer):
    class Meta :
        model = ProductMetaData
        fields=['title','image']


class ProductSerializer(serializers.ModelSerializer):
    website = WebsiteSerializer()
    meta = ProductMetaDataSerializer()
    class Meta:
        model=Product
        fields=['id','url','created_at','website','alerts','meta'] 


class PriceHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    checked_at = serializers.DateTimeField(format="%y-%m-%d %H:%M:%S")
    class Meta:
        model=PriceHistory
        fields=['price','checked_at','product']


class XpathSerializer(serializers.ModelSerializer):
    class Meta:
        model=Xpath
        fields=['website','price_selector','title_selector','image_selector']

