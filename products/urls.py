from django.urls import path,include
from rest_framework.routers import SimpleRouter 
from .views import (
    WebsiteViewSet,
    ProductViewSet,
    PriceHistoryViewSet,
    XpathViewSet
)


router = SimpleRouter()

router.register('websites',WebsiteViewSet)
router.register('products',ProductViewSet)
router.register('prices',PriceHistoryViewSet)
router.register('xpaths',XpathViewSet)

urlpatterns = [
    path('',include(router.urls))
]