from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    ChannelSerializer,
    AlertSerializers
)

from .models import (
    Channel,
    Alert
)


class ChannelViewSet(ModelViewSet):
    queryset=Channel.objects.all()
    serializer_class=ChannelSerializer


class AlertViewSet(ModelViewSet):
    queryset=Alert.objects.all()
    serializer_class=AlertSerializers


