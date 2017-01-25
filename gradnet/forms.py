from django import forms
from .models import Alumni


class AlumniSignupForm(forms.ModelForm):
    class Meta:
        model = Alumni

        fields = ['name']

