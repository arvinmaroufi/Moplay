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


class DirectorAdminForm(SocialMediaAdminForm):
    class Meta:
        model = models.Director
        fields = '__all__'
