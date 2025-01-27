from django import forms
from .models import BusinessClient

class BusinessClientForm(forms.ModelForm):
    class Meta:
        model = BusinessClient
        fields = ['full_name', 'company_name', 'phone', 'location', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'full_name': 'Full Name',
            'company_name': 'Company Name',
            'phone': 'Phone Number',
            'location': 'Location',
            'address': 'Address',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number must only contain digits.")
        return phone

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name) < 3:
            raise forms.ValidationError("Full name must have at least 3 characters.")
        return full_name
