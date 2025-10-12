from django.urls import path,include
from rest_framework.routers import SimpleRouter 
from .views import (
    WebsiteViewSet,
    ProductViewSet,
    PriceHistoryViewSet,
    XpathViewSet,
    CurrrencyViewSet,
    AddProduct,
    AddNewScraper
)


router = SimpleRouter()

router.register('websites',WebsiteViewSet)
router.register('products',ProductViewSet)
router.register('prices',PriceHistoryViewSet)
router.register('xpaths',XpathViewSet)
router.register('currencies',CurrrencyViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('add-product/',AddProduct.as_view()),
    path('add-scraper/',AddNewScraper.as_view())
]