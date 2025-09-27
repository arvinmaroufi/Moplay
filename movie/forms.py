from django import forms
from . import models


class SocialMediaAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        social_media_fields = {
            'twitter_url': 'https://twitter.com/username',
            'instagram_url': 'https://instagram.com/username',
            'facebook_url': 'https://facebook.com/username',
        }

        for field_name, placeholder in social_media_fields.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'placeholder': placeholder,
                    'class': 'vURLField'
                })


class DirectorAdminForm(forms.ModelForm):
    class Meta:
        model = models.Director
        fields = '__all__'
        widgets = {
            'twitter_url': forms.URLInput(attrs={
                'placeholder': 'https://twitter.com/username',
                'class': 'vURLField'
            }),
            'instagram_url': forms.URLInput(attrs={
                'placeholder': 'https://instagram.com/username',
                'class': 'vURLField'
            }),
            'facebook_url': forms.URLInput(attrs={
                'placeholder': 'https://facebook.com/username',
                'class': 'vURLField'
            }),
        }
