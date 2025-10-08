from django.contrib import admin
from . import models
from jalali_date import datetime2jalali


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'short_subject', 'get_date_send_jalali']
    list_filter = ['date_send']
    search_fields = ['email']
    ordering = ['-date_send']

    @admin.display(description='تاریخ ارسال', ordering='date_send')
    def get_date_send_jalali(self, obj):
        return datetime2jalali(obj.date_send).strftime('%a، %d %b %Y')

    def short_subject(self, obj):
        if len(obj.subject) > 50:
            return obj.subject[:50] + '...'
        return obj.subject
    short_subject.short_description = 'موضوع'
