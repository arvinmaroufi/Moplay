from django import forms
from .models import Contact
from django.forms import ValidationError


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 100:
            raise ValidationError("نام نمی ‌تواند بیشتر از 100 کاراکتر باشد")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if len(email) > 200:
            raise ValidationError("ایمیل نمی‌ تواند بیشتر از 200 کاراکتر باشد")
        return email

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if len(subject) > 100:
            raise ValidationError("موضوع شما نمی ‌تواند بیشتر از 100 کاراکتر باشد")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) > 3000:
            raise ValidationError("پیام شما نمی ‌تواند بیشتر از 3000 کاراکتر باشد")
        return message
