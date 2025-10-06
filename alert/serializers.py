from rest_framework import serializers 
from products.serializers import ProductSerializer
from .models import (
    Channel,
    Alert
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

