from django.contrib import admin
from . import models
from jalali_date import datetime2jalali


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'get_created_at_jalali']
    list_filter = ['created_at']
    search_fields = ['title']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')
