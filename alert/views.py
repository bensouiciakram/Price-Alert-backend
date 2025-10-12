from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin
from .serializers import (
    ChannelSerializer,
    AlertSerializer,
    AlertMetSerializer
)

from .models import (
    Channel,
    Alert,
    AlertMet
)


class ChannelViewSet(ListModelMixin,CreateModelMixin,GenericViewSet):
    queryset=Channel.objects.all()
    serializer_class=ChannelSerializer


class AlertViewSet(ModelViewSet):
    queryset=Alert.objects.all()
    serializer_class=AlertSerializer


class AlertMetViewSet(ModelViewSet):
    queryset = AlertMet.objects.select_related('alert', 'alert__product').order_by('-triggered_at').all()
    serializer_class = AlertMetSerializer
    # permission_classes = [permissions.IsAuthenticated]