from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import DemoTokenSerializer
from .models import DemoToken

# Create your views here.

class DemoTokenViewSet(ModelViewSet):
    queryset = DemoToken.objects.all()
    serializer_class = DemoTokenSerializer

    
