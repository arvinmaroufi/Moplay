from django import forms
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth import authenticate


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام'
        }),
        error_messages={
            'required': 'نام الزامی است'
        }
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام خانوادگی'
        }),
        error_messages={
            'required': 'نام خانوادگی الزامی است'
        }
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل'
        }),
        error_messages={
            'required': 'ایمیل الزامی است',
            'invalid': 'لطفا یک ایمیل معتبر وارد کنید'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور'
        }),
        error_messages={
            'required': 'رمز عبور الزامی است'
        }
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('این ایمیل قبلا استفاده شده است')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError('رمز عبور باید حداقل 8 کاراکتر باشد')
        if len(password) > 20:
            raise ValidationError('رمز عبور نمی‌تواند بیشتر از 20 کاراکتر باشد')
        return password


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل'
        }),
        error_messages={
            'required': 'ایمیل الزامی است',
            'invalid': 'لطفاً یک ایمیل معتبر وارد کنید'
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور'
        }),
        error_messages={
            'required': 'رمز عبور الزامی است'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError('کاربری با این ایمیل وجود ندارد')

            auth_user = authenticate(email=email, password=password)
            if not auth_user:
                raise ValidationError('رمز عبور اشتباه است')

            cleaned_data['user'] = auth_user

        return cleaned_data
