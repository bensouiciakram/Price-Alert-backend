from django.contrib import admin
from .models import (
    Website,
    Product,
    ProductMetaData,
    PriceHistory,
    Xpath
)

# Register your models here.
@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['url','scraping_method']


@admin.register(PriceHistory)
class PriceAdmin(admin.ModelAdmin):
    list_display=['price','checked_at','product']
    list_select_related = ['product']


@admin.register(Xpath)
class XpathAdmin(admin.ModelAdmin):
    list_display=['website','title_selector','price_selector','image_selector']
    list_select_related=['website']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['url','created_at',]


@admin.register(ProductMetaData)
class ProductMedaDataAdmin(admin.ModelAdmin):
    list_display =['title','image']