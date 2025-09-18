from django import forms
from django.core.exceptions import ValidationError


class ProfileEditForm(forms.Form):
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
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره تماس'
        })
    )
    about_me = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'درباره من',
            'rows': 4
        })
    )
    profile_photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'profile-file-input',
            'accept': 'image/*'
        })
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if not phone.startswith('09'):
                raise ValidationError("شماره تلفن باید با 09 شروع شود")
            if len(phone) != 11:
                raise ValidationError("شماره تلفن باید 11 رقم باشد")
        return phone


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور فعلی'
        }),
        error_messages={
            'required': 'رمز عبور فعلی الزامی است'
        }
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'رمز عبور جدید'
        }),
        error_messages={
            'required': 'رمز عبور جدید الزامی است'
        }
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'تکرار رمز عبور جدید'
        }),
        error_messages={
            'required': 'تکرار رمز عبور جدید الزامی است'
        }
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise ValidationError('رمز عبور فعلی صحیح نیست')
        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if len(new_password) < 8:
            raise ValidationError('رمز عبور باید حداقل 8 کاراکتر باشد')
        if len(new_password) > 20:
            raise ValidationError('رمز عبور نمی‌تواند بیشتر از 20 کاراکتر باشد')

        if self.user.check_password(new_password):
            raise ValidationError('رمز عبور جدید نمی ‌تواند با رمز عبور فعلی یکسان باشد')

        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError('رمز عبور جدید و تکرار آن مطابقت ندارند')

        return cleaned_data
    