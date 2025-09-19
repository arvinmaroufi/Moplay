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


class Year(models.Model):
    year = models.CharField(max_length=4, unique=True, verbose_name='سال')
    slug = models.SlugField(max_length=4, unique=True, verbose_name='نامک')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'سال'
        verbose_name_plural = 'سال ها'

    def __str__(self):
        return self.year


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='نام کشور')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='نامک')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'کشور'
        verbose_name_plural = 'کشور ها'

    def __str__(self):
        return self.name


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='عنوان برچسب')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='نامک')
    views = models.PositiveIntegerField(default=0, verbose_name='بازدید ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها'

    def __str__(self):
        return self.title


class Director(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='اسم کارگردان')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='نامک')
    bio = models.TextField(blank=True, null=True, verbose_name='بیوگرافی')
    photo = models.ImageField(upload_to='directors_photos/', null=True, blank=True, verbose_name='عکس کارگردان')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'کارگردان'
        verbose_name_plural = 'کارگردانان'

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='اسم بازیگر')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='نامک')
    bio = models.TextField(blank=True, null=True, verbose_name='بیوگرافی')
    photo = models.ImageField(upload_to='actors_photos/', null=True, blank=True, verbose_name='عکس بازیگر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'بازیگر'
        verbose_name_plural = 'بازیگران'

    def __str__(self):
        return self.name
