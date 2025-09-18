from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from jalali_date import datetime2jalali


# personalized actions
def activate_users(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(
        request, _(f"{updated} کاربر با موفقیت فعال شدند."), messages.SUCCESS)
activate_users.short_description = "فعال کردن کاربران انتخاب شده"


def deactivate_users(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(
        request, _(f"{updated} کاربر با موفقیت غیرفعال شدند."), messages.SUCCESS)
deactivate_users.short_description = "غیرفعال کردن کاربران انتخاب شده"


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('عمومی', {'fields': ('email', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'phone', 'about_me', 'profile_photo')}),
        ('اجازه ها', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('تاریخ های مهم', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        ('عمومی', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
        ('اطلاعات شخصی', {
            'fields': ('first_name', 'last_name', 'phone', 'profile_photo')
        }),
        ('اجازه ها', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    list_display = ['email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_active', 'get_date_joined_jalali']
    search_fields = ['email', 'phone', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    ordering = ['date_joined']
    actions = [activate_users, deactivate_users]

    @admin.display(description='تاریخ پیوستن', ordering='date_joined')
    def get_date_joined_jalali(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%a، %d %b %Y')
