from django.urls import path,include 
from rest_framework.routers import SimpleRouter
from .views import DemoTokenViewSet


router = SimpleRouter()

router.register('tokens',DemoTokenViewSet)

urlpatterns = [
    path('',include(router.urls))
]