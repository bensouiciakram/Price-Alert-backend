from django.contrib import admin
from .models import (
    Website,
    Product,
    Price,
    Field,
    Xpath
)

# Register your models here.
@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['domain']


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display=['price','checked_at','product']
    list_select_related = ['product']


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display=['field_name']


@admin.register(Xpath)
class XpathAdmin(admin.ModelAdmin):
    list_display=['selector','website','field']
    list_select_related=['website','field']