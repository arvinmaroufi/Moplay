from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    username = None
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name="شماره تلفن")
    about_me = models.TextField(max_length=300, blank=True, null=True, verbose_name="درباره من")
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True, verbose_name="عکس پروفایل")
    email = models.EmailField(max_length=100, unique=True, blank=False, verbose_name='آدرس ایمیل')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        ordering = ['date_joined']
