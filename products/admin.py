from django.contrib import admin
from .models import (
    Website,
    Product,
    PriceHistory,
    Xpath
)

# Register your models here.
@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['domain']


@admin.register(PriceHistory)
class PriceAdmin(admin.ModelAdmin):
    list_display=['price','checked_at','product']
    list_select_related = ['product']


@admin.register(Xpath)
class XpathAdmin(admin.ModelAdmin):
    list_display=['website','title_selector','price_selector','image_selector']
    list_select_related=['website']