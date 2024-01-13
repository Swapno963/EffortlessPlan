from django import forms
from .models import Tasks
class Task_form(forms.ModelForm):
    class Meta:
        model = Tasks
        # excepts = ['user']
        exclude = ['user']