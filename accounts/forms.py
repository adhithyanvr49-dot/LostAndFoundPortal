# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # This tells the form to use your CustomUser and include the phone field
        fields = UserCreationForm.Meta.fields + ('phone_number',)