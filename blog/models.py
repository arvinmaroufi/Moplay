from django.db import models


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
