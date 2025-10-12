from django.db import models


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
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='قیمت')
    duration_days = models.IntegerField(verbose_name='مدت به روز')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'پلن اشتراک'
        verbose_name_plural = 'پلن‌ های اشتراک'

    def __str__(self):
        return f"{self.name} - {self.price} تومان"
