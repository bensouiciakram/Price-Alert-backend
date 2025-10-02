from django.urls import path,include 
from rest_framework.routers import SimpleRouter 
from .views import (
    ChannelViewSet,
    AlertViewSet
)


router = SimpleRouter()

router.register('channels',ChannelViewSet)
router.register('alerts',AlertViewSet)

urlpatterns = [
    path('',include(router.urls))
]