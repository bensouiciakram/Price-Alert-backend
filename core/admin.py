from django.contrib import admin
from .models import (
    User,
    DemoToken
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['username','email']


@admin.register(DemoToken)
class DemoTokenAdmin(admin.ModelAdmin):
    list_display = ['token','expire_at','is_active','created_at','user']
    