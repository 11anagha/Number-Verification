from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(forms.Form):
    """
    Form for user registration.

    Includes email, password, and password confirmation with validation.
    """

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"}),
    )

    def clean_email(self):
        """Ensure email is unique."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        """Ensure both passwords match."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class LoginForm(forms.Form):
    """
    Form for user login.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
    )



class NumberForm(forms.Form):
    """
    Form for Armstrong number verification.
    """

    number = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter a number"}),
    )
