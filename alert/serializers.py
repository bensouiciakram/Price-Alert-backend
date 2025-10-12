from decimal import Decimal
from rest_framework import serializers 
from products.serializers import ProductSerializer
from .models import (
    Channel,
    Alert,
    AlertMet
)

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Channel 
        fields = ['name']


class AlertSerializer(serializers.ModelSerializer):
    channel = ChannelSerializer()
    product = ProductSerializer()
    class Meta:
        model=Alert
        fields =['id','threshold','frequency','created_at','channel','product'] 

class AlertMetSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(source='get_product_name', read_only=True)
    website_url = serializers.SerializerMethodField(source='get_website_url',read_only=True)
    product_id = serializers.SerializerMethodField(source='get_product_id',read_only=True)
    threshold_price = serializers.SerializerMethodField(
        source='get_threshold_price', 
        read_only=True
    )
    new_price = serializers.SerializerMethodField(source='get_last_price',read_only=True)
    triggered_at = serializers.DateTimeField(format="%y-%m-%d %H:%M:%S")

    class Meta:
        model = AlertMet
        fields = [
            'id',
            'product_id',
            'product_name',
            'threshold_price',
            'triggered_at',
            'website_url',
            'new_price'
        ]

    def get_new_price(self,alert_met) -> Decimal :
        return alert_met\
                    .alert\
                    .product\
                    .prices\
                    .first()\
                    .price
    

    def get_product_name(self,alert_met) -> str:
        return alert_met\
                    .alert\
                    .product\
                    .meta\
                    .title 
    

    def get_website_url(self,alert_met) -> str:
        return alert_met\
                    .alert\
                    .product\
                    .website\
                    .url 
    

    def get_product_id(self,alert_met) -> int :
        return alert_met\
                    .alert\
                    .product\
                    .id 
    

    def get_threshold_price(self,alert_met) -> Decimal:
        return alert_met\
                    .alert\
                    .threshold 