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
