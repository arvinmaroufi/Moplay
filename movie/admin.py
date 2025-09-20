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


@admin.register(models.Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_created_at_jalali']
    list_filter = ['created_at']
    search_fields = ['name']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')


class MovieCommentInline(admin.TabularInline):
    model = models.MovieComment
    extra = 0
    readonly_fields = ['created_at']


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'dubbed_or_subtitle', 'subscription_status', 'status', 'views', 'get_created_at_jalali']
    list_filter = ['status', 'dubbed_or_subtitle', 'subscription_status', 'created_at', 'genre', 'country']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['genre', 'tags', 'language', 'actors', 'similar_movies', 'country', 'director']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [MovieCommentInline]
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'description', 'vertical_banner', 'horizontal_banner')
        }),
        ('دسته‌بندی و برچسب‌ها', {
            'fields': ('genre', 'tags', 'language', 'country')
        }),
        ('افراد مرتبط', {
            'fields': ('actors', 'director', 'similar_movies')
        }),
        ('مشخصات فنی', {
            'fields': ('duration', 'release_date', 'score', 'age_range')
        }),
        ('لینک‌های رسانه', {
            'fields': ('trailer', 'subtitle_url', 'quality_480p', 'quality_720p', 'quality_1080p')
        }),
        ('تنظیمات نمایش', {
            'fields': ('dubbed_or_subtitle', 'subscription_status', 'is_recommended', 'status')
        }),
        ('آمار و تاریخ‌ها', {
            'fields': ('views', 'created_at', 'updated_at')
        }),
    )

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')


class SeriesCommentInline(admin.TabularInline):
    model = models.SeriesComment
    extra = 0
    readonly_fields = ['created_at']


class ChapterSeriesInline(admin.TabularInline):
    model = models.ChapterSeries
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


@admin.register(models.Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'dubbed_or_subtitle', 'subscription_status', 'status', 'views', 'chapter_count', 'get_created_at_jalali']
    list_filter = ['status', 'dubbed_or_subtitle', 'subscription_status', 'created_at', 'genre', 'country']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['genre', 'tags', 'language', 'actors', 'similar_series', 'country', 'director']
    readonly_fields = ['views', 'created_at', 'updated_at']
    inlines = [ChapterSeriesInline, SeriesCommentInline]
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'slug', 'description', 'vertical_banner', 'horizontal_banner')
        }),
        ('دسته‌بندی و برچسب‌ها', {
            'fields': ('genre', 'tags', 'language', 'country')
        }),
        ('افراد مرتبط', {
            'fields': ('actors', 'director', 'similar_series')
        }),
        ('مشخصات فنی', {
            'fields': ('duration', 'chapter_count', 'release_date', 'score', 'age_range')
        }),
        ('لینک‌های رسانه', {
            'fields': ('trailer', 'subtitle_url')
        }),
        ('تنظیمات نمایش', {
            'fields': ('dubbed_or_subtitle', 'subscription_status', 'is_recommended', 'status')
        }),
        ('آمار و تاریخ‌ها', {
            'fields': ('views', 'created_at', 'updated_at')
        }),
    )

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')


class VideoSeriesInline(admin.TabularInline):
    model = models.VideoSeries
    extra = 0


@admin.register(models.ChapterSeries)
class ChapterSeriesAdmin(admin.ModelAdmin):
    list_display = ['series', 'title', 'order', 'created_at']
    list_filter = ['series', 'created_at']
    search_fields = ['title', 'series__title']
    inlines = [VideoSeriesInline]


@admin.register(models.VideoSeries)
class VideoSeriesAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'order', 'get_subtitle', 'get_series_name']
    list_filter = ['chapter__series']
    search_fields = ['chapter__title', 'chapter__series__title']

    def get_series_name(self, obj):
        return obj.chapter.series.title
    get_series_name.short_description = 'سریال'
    get_series_name.admin_order_field = 'chapter__series__title'

    def get_subtitle(self, obj):
        return "دارد" if obj.subtitle else "ندارد"
    get_subtitle.short_description = 'زیرنویس'


@admin.register(models.MovieComment)
class MovieCommentAdmin(admin.ModelAdmin):
    list_display = ['movie', 'author', 'status', 'get_created_at_jalali']
    list_filter = ['status', 'created_at', 'movie']
    search_fields = ['movie__title']
    readonly_fields = ['created_at']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')
