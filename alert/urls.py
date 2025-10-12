from django.urls import path,include 
from rest_framework.routers import SimpleRouter 
from .views import (
    ChannelViewSet,
    AlertViewSet,
    AlertMetViewSet
)


router = SimpleRouter()

router.register('channels',ChannelViewSet)
router.register('alerts',AlertViewSet)
router.register('alerts-met', AlertMetViewSet)

urlpatterns = [
    path('',include(router.urls))
]