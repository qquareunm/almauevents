from django import forms
from .models import Registration, EventImage

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ["first_name", "last_name", "email", "phone_number", "comment"]

