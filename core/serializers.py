from rest_framework import serializers
from .models import DemoToken

class DemoTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoToken 
        fields=['token','expire_at','is_active','created_at','user']