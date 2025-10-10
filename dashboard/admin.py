from django.contrib import admin
from . import models
from jalali_date import datetime2jalali
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


# personalized actions
def activate_notifications(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(
        request, _(f"{updated} اعلان با موفقیت فعال شدند."), messages.SUCCESS)
activate_notifications.short_description = "فعال کردن اعلان‌ های انتخاب شده"


def deactivate_notifications(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(
        request, _(f"{updated} اعلان با موفقیت غیرفعال شدند."), messages.SUCCESS)
deactivate_notifications.short_description = "غیرفعال کردن اعلان‌ های انتخاب شده"


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['message', 'is_for_all_users', 'is_active', 'get_created_at_jalali', 'get_expiration_date_jalali']
    list_filter = ['is_for_all_users', 'is_active', 'created_at', 'expiration_date']
    search_fields = ['message']
    filter_horizontal = ['users', 'read_by']
    fieldsets = [
        ('عمومی', {
            'fields': ['message', 'is_active']
        }),
        ('تنظیمات مخاطبان', {
            'fields': ['is_for_all_users', 'users']
        }),
        ('تنظیمات زمانی', {
            'fields': ['created_at', 'expiration_date']
        }),
        ('وضعیت خواندن', {
            'fields': ['read_by'],
            'classes': ['collapse']
        })
    ]
    readonly_fields = ['created_at']
    actions = [activate_notifications, deactivate_notifications]

    def get_queryset(self, request):
        models.Notification.delete_expired_notifications()
        return super().get_queryset(request)

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y - %H:%M:%S')

    @admin.display(description='تاریخ انقضا', ordering='expiration_date')
    def get_expiration_date_jalali(self, obj):
        return datetime2jalali(obj.expiration_date).strftime('%a، %d %b %Y - %H:%M:%S')


@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'get_created_at_jalali', 'get_updated_at_jalali']

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y - %H:%M:%S')

    @admin.display(description='تاریخ بروزرسانی', ordering='updated_at')
    def get_updated_at_jalali(self, obj):
        return datetime2jalali(obj.updated_at).strftime('%a، %d %b %Y - %H:%M:%S')
