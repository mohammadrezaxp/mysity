from django import forms
from .models import login
class log_from(forms.ModelForm):
    class Meta :
        model = login
        fields = ['username', 'password']


