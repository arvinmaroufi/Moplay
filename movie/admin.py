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


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_created_at_jalali']
    list_filter = ['created_at']
    search_fields = ['name']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')


@admin.register(models.Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ['year', 'slug', 'get_created_at_jalali']
    prepopulated_fields = {'slug': ('year',)}
    list_filter = ['created_at']
    search_fields = ['year']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_created_at_jalali']
    list_filter = ['created_at']
    search_fields = ['name']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'views', 'get_created_at_jalali']
    list_filter = ['created_at']
    search_fields = ['title']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')


@admin.register(models.Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_created_at_jalali']
    list_filter = ['created_at']
    search_fields = ['name']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')
