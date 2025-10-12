from django.contrib import admin
from .models import (
    Channel,
    Alert,
    AlertMet 
)

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display=['name']


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display=['id','threshold','frequency','created_at','channel','product']
    list_select_related=['channel','product']


@admin.register(AlertMet)
class AlertMetAdmin(admin.ModelAdmin):
    list_display=['alert','triggered_at']
    list_select_related = ['alert']