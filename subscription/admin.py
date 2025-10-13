from django.contrib import admin
from . import models
from jalali_date import datetime2jalali
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


# personalized actions

# actions for plans
def activate_plans(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, _(f"{updated} مورد با موفقیت فعال شدند."), messages.SUCCESS)
activate_plans.short_description = "فعال کردن پلن های انتخاب شده"


def deactivate_plans(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, _(f"{updated} مورد با موفقیت فعال شدند."), messages.SUCCESS)
deactivate_plans.short_description = "غیرفعال کردن پلن های انتخاب شده"


# actions for subscriptions
def activate_subscriptions(modeladmin, request, queryset):
    updated = queryset.update(status='active')
    modeladmin.message_user(request, _(f"{updated} اشتراک با موفقیت فعال شدند."), messages.SUCCESS)
activate_subscriptions.short_description = "فعال کردن اشتراک ‌های انتخاب شده"


def expire_subscriptions(modeladmin, request, queryset):
    updated = queryset.update(status='expired')
    modeladmin.message_user(request, _(f"{updated} اشتراک با موفقیت منقضی شدند."), messages.SUCCESS)
expire_subscriptions.short_description = "منقضی کردن اشتراک‌ های انتخاب شده"


def cancel_subscriptions(modeladmin, request, queryset):
    updated = queryset.update(status='canceled')
    modeladmin.message_user(request, _(f"{updated} اشتراک با موفقیت لغو شدند."), messages.SUCCESS)
cancel_subscriptions.short_description = "لغو کردن اشتراک‌ های انتخاب شده"


@admin.register(models.SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_type', 'price', 'duration_days', 'is_active', 'get_created_at_jalali']
    list_filter = ['duration_type', 'is_active', 'created_at']
    search_fields = ['name']

    fieldsets = [
        ('اطلاعات پایه', {
            'fields': ['name', 'duration_type']
        }),
        ('قیمت و مدت', {
            'fields': ['price', 'duration_days']
        }),
        ('وضعیت', {
            'fields': ['is_active']
        }),
    ]
    actions = [activate_plans, deactivate_plans]

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%a، %d %b %Y')


@admin.register(models.UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user__email', 'plan', 'status', 'get_start_date_jalali', 'get_end_date_jalali', 'payment_amount', 'get_created_at_jalali']
    list_filter = ['user__email', 'status', 'plan', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']

    fieldsets = [
        ('اطلاعات کاربر و پلن', {
            'fields': ['user', 'plan']
        }),
        ('وضعیت و تاریخ‌ها', {
            'fields': ['status', 'start_date', 'end_date']
        }),
        ('اطلاعات پرداخت', {
            'fields': ['payment_amount', 'transaction_id']
        }),
        ('تاریخ‌های سیستم', {
            'fields': ['created_at', 'updated_at']
        }),
    ]
    actions = [activate_subscriptions, expire_subscriptions, cancel_subscriptions]

    @admin.display(description='تاریخ شروع', ordering='start_date')
    def get_start_date_jalali(self, obj):
        if obj.start_date:
            return datetime2jalali(obj.start_date).strftime('%H:%M:%S - %Y/%m/%d')
        return "-"

    @admin.display(description='تاریخ پایان', ordering='end_date')
    def get_end_date_jalali(self, obj):
        if obj.end_date:
            return datetime2jalali(obj.end_date).strftime('%H:%M:%S - %Y/%m/%d')
        return "-"

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%H:%M:%S - %Y/%m/%d')


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'amount', 'status', 'get_payment_date_jalali', 'get_created_at_jalali']
    list_filter = ['status', 'payment_date', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at']

    fieldsets = [
        ('اطلاعات پرداخت', {
            'fields': ['user', 'subscription', 'amount', 'status']
        }),
        ('تاریخ پرداخت', {
            'fields': ['payment_date']
        }),
        ('تاریخ ایجاد', {
            'fields': ['created_at']
        }),
    ]

    @admin.display(description='تاریخ پرداخت', ordering='payment_date')
    def get_payment_date_jalali(self, obj):
        if obj.payment_date:
            return datetime2jalali(obj.payment_date).strftime('%H:%M:%S - %Y/%m/%d')
        return "-"

    @admin.display(description='تاریخ ایجاد', ordering='created_at')
    def get_created_at_jalali(self, obj):
        return datetime2jalali(obj.created_at).strftime('%H:%M:%S - %Y/%m/%d')
