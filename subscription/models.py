from django.db import models
from accounts.models import User
from django.utils import timezone
import uuid


class SubscriptionPlan(models.Model):
    PLAN_TYPES = [
        ('basic', 'پایه'),
        ('standard', 'نقره‌ای'),
        ('premium', 'طلایی'),
        ('advanced', 'الماسی'),
    ]

    DURATION_TYPES = [
        ('one_month', 'یک ماهه'),
        ('three_months', 'سه ماهه'),
        ('six_months', 'شش ماهه'),
        ('one_year', 'یک ساله'),
    ]

    name = models.CharField(max_length=100, verbose_name='نام پلن')
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES, verbose_name='نوع پلن')
    duration_type = models.CharField(max_length=20, choices=DURATION_TYPES, verbose_name='نوع مدت')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    duration_days = models.IntegerField(verbose_name='مدت به روز')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'پلن اشتراک'
        verbose_name_plural = 'پلن‌ های اشتراک'

    def __str__(self):
        return f"{self.name} - {self.price} تومان"


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('expired', 'منقضی شده'),
        ('canceled', 'لغو شده'),
        ('pending', 'در انتظار پرداخت'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, verbose_name='پلن')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ پایان')
    payment_amount = models.PositiveIntegerField(verbose_name='مبلغ پرداختی')
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='شناسه تراکنش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'اشتراک کاربر'
        verbose_name_plural = 'اشتراک‌ های کاربران'

    def __str__(self):
        return self.user.email

    def is_active(self):
        if self.status == 'active' and self.end_date and self.end_date > timezone.now():
            return True
        return False

    def save(self, *args, **kwargs):
        if self.status == 'active' and self.end_date and self.end_date <= timezone.now():
            self.status = 'expired'

        if self.status == 'active' and not self.start_date:
            self.start_date = timezone.now()
            if self.plan.duration_days:
                self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration_days)

        super().save(*args, **kwargs)
