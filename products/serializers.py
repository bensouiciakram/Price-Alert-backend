from rest_framework import serializers 
from .models import (
    Website,
    Product,
    Price,
    Field,
    Xpath
)


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website 
        fields = ['domain']


class ProductSerializer(serializers.ModelSerializer):
    website = WebsiteSerializer()
    class Meta:
        model=Product
        fields=['url','name','created_at','website'] 


class PriceSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model=Price
        fields=['price','checked_at','product']

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model=Field
        fields=['field_name']


class XpathSerializer(serializers.ModelSerializer):
    class Meta:
        model=Xpath
        fields=['selector','website','field']