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
    product_name = serializers.CharField(source='alert.product.name', read_only=True)
    threshold_price = serializers.DecimalField(
        source='alert.threshold_price', 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )

    class Meta:
        model = AlertMet
        fields = [
            'id',
            'alert',
            'product_name',
            'threshold_price',
            'triggered_at',
        ]
