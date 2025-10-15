from django.contrib import admin
from . import models
from jalali_date import datetime2jalali
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


# personalized actions

def make_article_published(modeladmin, request, queryset):
    updated = queryset.update(status='published')
    modeladmin.message_user(request, _(f"{updated} مقاله با موفقیت منتشر شدند."), messages.SUCCESS)
make_article_published.short_description = "منتشر کردن مقالات انتخاب شده"


def make_article_draft(modeladmin, request, queryset):
    updated = queryset.update(status='draft')
    modeladmin.message_user(request, _(f"{updated} مقاله با موفقیت پیش نویس شدند."), messages.SUCCESS)
make_article_draft.short_description = "پیش نویس کردن مقالات انتخاب شده"


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


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['short_title', 'status', 'views', 'get_created_at_jalali', 'get_updated_at_jalali']
    list_filter = ['status', 'created_at', 'updated_at', 'category']
    search_fields = ['title']
    filter_horizontal = ['category', 'tag']
    readonly_fields = ['created_at', 'updated_at', 'get_created_at_jalali', 'get_updated_at_jalali']
    actions = [make_article_published, make_article_draft]
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'description')
        }),
        ('دسته‌بندی و برچسب‌ها', {
            'fields': ('category', 'tag')
        }),
        ('بنرها', {
            'fields': ('list_banner', 'detail_banner'),
        }),
        ('تنظیمات نمایش', {
            'fields': ('status',)
        }),
        ('آمار و تاریخ‌ها', {
            'fields': ('views', 'created_at', 'updated_at', 'get_created_at_jalali', 'get_updated_at_jalali')
        }),
    )

    def short_title(self, obj):
        if len(obj.title) > 30:
            return obj.title[:30] + '...'
        return obj.title

    short_title.short_description = 'عنوان مقاله'
    
    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')

    @admin.display(description='تاریخ به‌روزرسانی', ordering='updated_at')
    def get_updated_at_jalali(self, obj):
        return datetime2jalali(obj.updated_at).strftime('%a، %d %b %Y')
