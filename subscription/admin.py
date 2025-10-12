from django.contrib import admin
from . import models
from jalali_date import datetime2jalali
from django.utils.translation import gettext_lazy as _
from django.contrib import messages


# personalized actions

def activate_plans(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, _(f"{updated} مورد با موفقیت فعال شدند."), messages.SUCCESS)
activate_plans.short_description = "فعال کردن پلن های انتخاب شده"


def deactivate_plans(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, _(f"{updated} مورد با موفقیت فعال شدند."), messages.SUCCESS)
deactivate_plans.short_description = "غیرفعال کردن پلن های انتخاب شده"


@admin.register(models.SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'duration_type', 'price', 'duration_days', 'is_active', 'get_created_at_jalali']
    list_filter = ['plan_type', 'duration_type', 'is_active', 'created_at']
    search_fields = ['name']

    fieldsets = [
        ('اطلاعات پایه', {
            'fields': ['name', 'plan_type', 'duration_type']
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
