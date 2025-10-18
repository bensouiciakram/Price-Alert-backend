import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from .serializers import ChannelSerializer, AlertSerializer, AlertMetSerializer
from .models import Channel, Alert, AlertMet

logger = logging.getLogger(__name__)


class ChannelViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class AlertViewSet(ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        alert = serializer.save(user=self.request.user)
        logger.info(f"Alert created (ID={alert.id}) by {self.request.user}")

    def perform_destroy(self, instance):
        logger.info(f"Alert deleted (ID={instance.id}) by {self.request.user}")
        super().perform_destroy(instance)


class AlertMetViewSet(ModelViewSet):
    queryset = AlertMet.objects.select_related('alert', 'alert__product').order_by('-triggered_at')
    serializer_class = AlertMetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        alert_met = serializer.save()
        logger.info(
            f"AlertMet triggered for Alert(ID={alert_met.alert.id}) "
            f"and Product={alert_met.alert.product}"
        )
