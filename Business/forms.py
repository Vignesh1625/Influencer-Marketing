# Business/forms.py
from django import forms
from .models import BusinessClient

class BusinessClientForm(forms.ModelForm):
    """
    Form for creating or updating a BusinessClient instance.
    Includes validation for phone number and full name.
    """
    class Meta:
        model = BusinessClient
        fields = ['full_name', 'gender', 'phone', 'location', 'address', 'company_name']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
        }

    def clean_phone(self):
        """
        Validate that the phone number contains only digits.
        """
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone

    def clean_full_name(self):
        """
        Validate that the full name is at least 3 characters long.
        """
        full_name = self.cleaned_data.get('full_name')
        if len(full_name) < 3:
            raise forms.ValidationError("Full name must be at least 3 characters long.")
        return full_name