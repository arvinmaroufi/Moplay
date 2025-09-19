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


class Genre(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='عنوان ژانر')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='نامک')
    thumbnail = models.ImageField(upload_to='genre_thumbnails/', null=True, blank=True, verbose_name='تصویر ژانر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'ژانر'
        verbose_name_plural = 'ژانر ها'

    def __str__(self):
        return self.title


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='زبان')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='نامک')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'زبان'
        verbose_name_plural = 'زبان ها'

    def __str__(self):
        return self.name
