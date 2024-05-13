# forms.py

from django import forms
from .models import CMSSettings

class CMSSettingsForm(forms.ModelForm):
    class Meta:
        model = CMSSettings
        fields = ['logo', 'banner', 'footer_slogan', 'about_us', 'privacy_policy', 'social_links', 'phone', 'email', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['social_links'].widget.attrs['rows'] = 5  # Adjust the number of rows in the form field
