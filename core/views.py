from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from .serializers import DemoTokenSerializer
from .models import DemoToken

# Create your views here.

class DemoTokenViewSet(RetrieveModelMixin,GenericViewSet):
    queryset = DemoToken.objects.all()
    serializer_class = DemoTokenSerializer

    
