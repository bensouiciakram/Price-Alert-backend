from django.contrib import admin
from .models import (
    Channel,
    Alert
)

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display=['name']


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display=['threshold','frequency','created_at','channel','product']
    list_select_related=['channel','product']
