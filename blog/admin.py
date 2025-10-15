from django.contrib import admin
from . import models
from jalali_date import datetime2jalali


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_created_at_jalali']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'views', 'get_created_at_jalali']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')
