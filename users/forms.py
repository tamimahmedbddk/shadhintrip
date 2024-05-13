from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm

# Ensure you're getting the custom user model
User = get_user_model()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta(UserCreationForm.Meta):
        # Assuming 'CustomUser' is your custom user model and it's in the 'users' app
        model = User
        # Make sure 'email' is included instead of 'username' and in the correct order
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',)

        # Update error_messages for the fields accordingly
        error_messages = {
            'email': {
                'unique': "A user with that email already exists. Please choose a different one.",
                'required': 'Email is required.',
                'invalid': 'This email is invalid. Please enter a valid email address.'
            },
            'password1': {
                'required': 'Password is required.',
                'password_too_short': 'This password is too short. It must contain at least 8 characters.',
                'password_too_common': 'This password is too common.',
                'password_entirely_numeric': 'This password is entirely numeric.'
            },
            'password2': {
                'required': 'Confirming your password is required.',
                'password_mismatch': "The passwords didn’t match. Please confirm your password again.",
            },
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Updating placeholders
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No account found with this email address.")
        return email

