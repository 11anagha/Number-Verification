from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ["password1", "password2"]:
            self.fields[fieldname].help_text = None
        self.fields["email"].help_text = None


    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email
