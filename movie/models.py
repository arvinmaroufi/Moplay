from django.db import models


STATUS = (
    ("draft", "پیش نویس شود"),
    ("published", "منتشر شود"),
)

DUBBED_OR_SUBTITLE_CHOICES = (
    ('dubbed', 'دوبله فارسی'),
    ('subtitled', 'زیرنویس فارسی'),
)

SUBSCRIPTION_STATUS_CHOICES = (
    ('free', 'رایگان'),
    ('subscription', 'اشتراکی'),
)
