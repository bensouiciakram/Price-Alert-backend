from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from .serializers import (
    ChannelSerializer,
    AlertSerializers
)

from .models import (
    Channel,
    Alert
)


class ChannelViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    queryset=Channel.objects.all()
    serializer_class=ChannelSerializer


class AlertViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    queryset=Alert.objects.all()
    serializer_class=AlertSerializers


