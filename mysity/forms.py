from captcha.fields import CaptchaField
from django import forms
from .models import Contact , news
class form_table(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)


class Contactform(forms.ModelForm):
    captcha = CaptchaField()  # ✅ درست شده

    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].required = False

        # اضافه کردن استایل به فیلدها
        self.fields['name'].widget.attrs.update({
            'class': 'common-input mb-20 form-control',
            'placeholder': 'Enter your name'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'common-input mb-20 form-control',
            'placeholder': 'Enter email address'
        })
        self.fields['subject'].widget.attrs.update({
            'class': 'common-input mb-20 form-control',
            'placeholder': 'Enter subject'
        })
        self.fields['message'].widget.attrs.update({
            'class': 'common-textarea form-control',
            'placeholder': 'Enter Message',
            'rows': 5
        })
class newsform(forms.ModelForm):
    class Meta:
        model = news
        fields = '__all__'