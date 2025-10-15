from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


STATUS = (
    ('draft', 'پیش نویس شود'),
    ('published', 'منتشر شود'),
)


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='نامک')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


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


class Article(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='اسلاگ')
    category = models.ManyToManyField(Category, related_name='articles', verbose_name='دسته بندی')
    tag = models.ManyToManyField(Tag, related_name='articles', verbose_name='برچسب')
    description = RichTextUploadingField(verbose_name='توضیحات')
    list_banner = models.ImageField(upload_to='articles/list_banner/', help_text='برای نمایش بهتر، تصویر را با ابعاد 900x600 پیکسل بارگذاری کنید',
                                    null=True, blank=True, verbose_name='بنر لیست مقاله')
    detail_banner = models.ImageField(upload_to='articles/detail_banner/', help_text='برای نمایش بهتر، تصویر را با ابعاد 1000x600 پیکسل بارگذاری کنید',
                                      null=True, blank=True, verbose_name='بنر جزئیات مقاله')
    status = models.CharField(choices=STATUS, max_length=10, default='published', verbose_name='وضعیت')
    views = models.PositiveIntegerField(default=0, verbose_name='بازدید ها')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title
