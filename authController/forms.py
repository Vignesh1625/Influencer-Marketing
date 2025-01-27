# authController/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class LoginForm(AuthenticationForm):
    """
    Custom login form with email as the username field.
    """
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'

class RegistrationForm(UserCreationForm):
    """
    Custom registration form with role selection.
    """
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='INFLUENCER'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@domain.com'
        }),
        help_text='Required. Enter a valid email address.'
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create password'
        }),
        help_text='Your password must contain at least 8 characters.'
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Repeat password'
        }),
        help_text='Enter the same password as before, for verification.'
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email Address'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'

    def clean_email(self):
        """
        Validate that the email is not already registered.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        """
        Save the user with the selected role.
        """
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.username = self.cleaned_data['email']  # For compatibility
        if commit:
            user.save()
        return user