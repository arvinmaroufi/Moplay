from django import forms
from . import models


class DirectorAdminForm(forms.ModelForm):
    class Meta:
        model = models.Director
        fields = '__all__'
        widgets = {
            'twitter_url': forms.URLInput(attrs={
                'placeholder': 'https://twitter.com/username'
            }),
            'instagram_url': forms.URLInput(attrs={
                'placeholder': 'https://instagram.com/username'
            }),
            'facebook_url': forms.URLInput(attrs={
                'placeholder': 'https://facebook.com/username'
            }),
        }
