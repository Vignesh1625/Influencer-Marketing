# influencers/forms.py
from django import forms
from .models import InfluencerInfo, InfluencerSocialMedia

class InfluencerAdditionalForm(forms.Form):
    full_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Bio'
        })
    )
    base_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'step': '0.01',
            'class': 'form-control',
            'placeholder': 'Base Amount'
        })
    )
    gender = forms.ChoiceField(
        choices=InfluencerInfo.GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    location = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Location'
        })
    )
    instagram_handle = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Instagram Handle'
        })
    )
    instagram_followers = forms.IntegerField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Instagram Followers'
        })
    )
    youtube_channel = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'YouTube Channel'
        })
    )
    youtube_subscribers = forms.IntegerField(
        min_value=0,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'YouTube Subscribers'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        instagram_handle = cleaned_data.get('instagram_handle')
        instagram_followers = cleaned_data.get('instagram_followers')
        youtube_channel = cleaned_data.get('youtube_channel')
        youtube_subscribers = cleaned_data.get('youtube_subscribers')

        if instagram_handle and not instagram_followers:
            raise forms.ValidationError("Please provide Instagram followers count")
        if youtube_channel and not youtube_subscribers:
            raise forms.ValidationError("Please provide YouTube subscribers count")

        return cleaned_data
