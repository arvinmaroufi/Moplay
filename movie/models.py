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


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='عنوان فیلم')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='نامک')
    genre = models.ManyToManyField(Genre, related_name='movies_genre', verbose_name='ژانر')
    tags = models.ManyToManyField(Tag, related_name='movies_tag', null=True, blank=True, verbose_name='برچسب')
    language = models.ManyToManyField(Language, related_name='movies_language', verbose_name='زبان فیلم')
    description = models.TextField(verbose_name='خلاصه داستان')
    vertical_banner = models.ImageField(upload_to='movies/movie_vertical_banner/', help_text='برای نمایش بهتر، تصویر را با ابعاد 800x1050 پیکسل بارگذاری کنید',
                                        null=True, blank=True, verbose_name='بنر عمودی فیلم')
    horizontal_banner = models.ImageField(upload_to='movies/movie_horizontal_banner/', help_text='برای نمایش بهتر، تصویر را با ابعاد 3320x1280 پیکسل بارگذاری کنید',
                                          null=True, blank=True, verbose_name='بنر افقی فیلم')
    actors = models.ManyToManyField(Actor, related_name='movies_actor', verbose_name='بازیگران')
    similar_movies = models.ManyToManyField('self', blank=True, null=True, related_name='similar', verbose_name='فیلم های مشابه')
    country = models.ManyToManyField(Country, related_name='movie_country', verbose_name='کشور سازنده')
    director = models.ManyToManyField(Director, related_name='movies_director', verbose_name='کارگردانان')
    duration = models.CharField(max_length=5, verbose_name='مدت زمان فیلم (لطفا مدت زمان را به دقیقه وارد کنید)')
    release_date = models.ForeignKey(Year, related_name='movie_year', on_delete=models.CASCADE, verbose_name='تاریخ انتشار')
    score = models.CharField(max_length=10, default='0.0/10', verbose_name='امتیاز')
    age_range = models.CharField(max_length=20, default='بالای 14 سال', verbose_name='رنج سنی')
    views = models.PositiveIntegerField(default=0, verbose_name='بازدید ها')
    trailer = models.URLField(max_length=500, verbose_name='لینک تریلر فیلم')
    subtitle_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='لینک زیرنویس فیلم')
    quality_480p = models.URLField(max_length=500, blank=True, null=True, verbose_name='لینک کیفیت 480p')
    quality_720p = models.URLField(max_length=500, blank=True, null=True, verbose_name='لینک کیفیت 720p')
    quality_1080p = models.URLField(max_length=500, blank=True, null=True, verbose_name='لینک کیفیت 1080p')
    dubbed_or_subtitle = models.CharField(choices=DUBBED_OR_SUBTITLE_CHOICES, max_length=10, default='dubbed', verbose_name='وضعیت دوبله یا زیرنویس')
    subscription_status = models.CharField(choices=SUBSCRIPTION_STATUS_CHOICES, max_length=12, default='subscription', verbose_name='وضعیت اشتراکی')
    is_recommended = models.BooleanField(default=False, verbose_name='آیا فیلم، پیشنهادی است؟')
    status = models.CharField(choices=STATUS, max_length=10, default='published', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم ها'

    def __str__(self):
        return self.title
