from django.urls import path,include
from rest_framework.routers import SimpleRouter 
from .views import (
    WebsiteViewSet,
    ProductViewSet,
    PriceViewSet,
    FieldViewSet,
    XpathViewSet
)


router = SimpleRouter()

router.register('websites',WebsiteViewSet)
router.register('products',ProductViewSet)
router.register('prices',PriceViewSet)
router.register('fields',FieldViewSet)
router.register('xpaths',XpathViewSet)

urlpatterns = [
    path('',include(router.urls))
]