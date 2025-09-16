from django.core.mail import send_mail
from django.conf import settings


def send_verification_email(user, code):
    subject = 'کد تایید ورود به موپلی'
    message = f'''
    کاربر گرامی {user.first_name} {user.last_name}،

    کد تایید شما برای ورود به حساب کاربری:
    {code}

    این کد به مدت 2 دقیقه معتبر است.

    با تشکر
    تیم موپلی
    '''

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
