from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate
from django.contrib import messages
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation, update_session_auth_hash
import logging

logger = logging.getLogger(__name__)

class CustomUserForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control input100', 'placeholder': 'Email'}),
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control input100', 'placeholder': 'First Name'}),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control input100', 'placeholder': 'Last Name'}),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control input100', 'placeholder': 'Password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control input100', 'placeholder': 'Confirm Password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        # Your custom validation logic for email, if needed
        return email


class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control input100', 'placeholder': 'Email'}),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control input100', 'placeholder': 'Password'}),
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        del self.fields['username']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(request=self.request, email=email, password=password)
 
            if self.user_cache is None:
                messages.error(self.request, _(
                    "Please enter a correct email and password. Note that both "
                    "fields may be case-sensitive."
                ))
                raise self.get_invalid_login_error()

            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
    
class CustomUpdateUserForm(ModelForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'profile_picture')
        widgets = {
            'first_name': forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'profile_picture': forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'exampleInputFile'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'}),
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
    )

    error_messages = {
        'password_incorrect': "Your old password was entered incorrectly. Please enter it again.",
        'password_mismatch': "The two password fields didn't match.",
        'password_weak': "The new password is too weak. Please choose a stronger password.",
    }

    def add_error(self, field, error):
        if field == 'new_password2':
            field = '__all__'
        elif field == 'old_password':
            field = '__all__'
        super().add_error(field, error)


    