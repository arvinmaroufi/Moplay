from django.db import models
from accounts.models import User
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q


class Notification(models.Model):
    message = models.TextField(verbose_name='پیام')
    is_for_all_users = models.BooleanField(default=False, help_text='با فعال‌سازی، اعلان به همه کاربران ارسال می‌شود', verbose_name='برای همه کاربران')
    users = models.ManyToManyField(User, blank=True, related_name='notifications', help_text='لیست کاربرانی که این اعلان را دریافت می‌کنند', verbose_name='کاربران هدف')
    read_by = models.ManyToManyField(User, blank=True, related_name='read_notifications', verbose_name='خوانده شده توسط')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    expiration_date = models.DateTimeField(null=True, blank=True, help_text='تاریخی که پس از آن اعلان به صورت خودکار حذف خواهد شد', verbose_name='تاریخ انقضا')

    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'اعلان‌ ها'
        ordering = ['-created_at']

    def __str__(self):
        return self.message

    @classmethod
    def delete_expired_notifications(cls):
        now = timezone.now()
        cls.objects.filter(models.Q(expiration_date__isnull=False) & models.Q(expiration_date__lt=now)).delete()

    @classmethod
    def _get_base_queryset_for_user(cls, user):
        now = timezone.now()
        if user.is_staff or user.is_superuser:
            return cls.objects.filter(
                is_active=True,
                users=user
            ).filter(
                Q(expiration_date__isnull=True) | Q(expiration_date__gte=now)
            )
        else:
            return cls.objects.filter(
                is_active=True
            ).filter(
                Q(is_for_all_users=True) | Q(users=user)
            ).filter(
                Q(expiration_date__isnull=True) | Q(expiration_date__gte=now)
            )

    @classmethod
    def get_active_notifications_for_user(cls, user):
        return cls._get_base_queryset_for_user(user).distinct().order_by('-created_at')

    @classmethod
    def get_recent_notifications_count(cls, user):
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        return cls._get_base_queryset_for_user(user).filter(
            created_at__gte=twenty_four_hours_ago
        ).exclude(
            read_by=user
        ).distinct().count()

    def mark_as_read(self, user):
        self.read_by.add(user)

    def is_read_by_user(self, user):
        return self.read_by.filter(id=user.id).exists()


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet', verbose_name='کاربر')
    balance = models.DecimalField(max_digits=16, decimal_places=0, default=0, verbose_name='موجودی (تومان)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول‌ها'

    def __str__(self):
        return f"کیف پول {self.user.email} - موجودی: {self.balance} تومان"

    def deposit(self, amount):
        self.balance += amount
        self.save()
        return self.balance

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

    def get_balance(self):
        return self.balance
