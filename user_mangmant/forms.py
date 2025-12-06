from django import forms
from .models import Sign_Up
class Singup_from(forms.ModelForm):
    class Meta :
        model = Sign_Up
        fields = ['first_name','last_name','email','phon_number',' birthday','password']


