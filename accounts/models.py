from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
import random
from django.utils import timezone
from datetime import timedelta


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


class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        time_elapsed = timezone.now() - self.created_at
        return not self.is_used and time_elapsed < timedelta(minutes=2)

    def mark_as_used(self):
        self.delete()

    @classmethod
    def generate_code(cls, user):
        cls.objects.filter(user=user).delete()
        code = str(random.randint(10000, 99999))
        return cls.objects.create(user=user, code=code)

    @classmethod
    def cleanup_expired_codes(cls):
        expired_time = timezone.now() - timedelta(minutes=2)
        cls.objects.filter(created_at__lt=expired_time).delete()

    def save(self, *args, **kwargs):
        self.cleanup_expired_codes()
        super().save(*args, **kwargs)
