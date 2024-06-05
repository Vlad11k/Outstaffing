from django import forms
from django.core.validators import RegexValidator

from mainsite.models import UserCVs


class SendCvForm(forms.ModelForm):
    class Meta:
        model = UserCVs
        fields = ['full_name', 'email', 'phone', 'message', 'file']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'type': 'tel', 'inputmode': 'tel'}),
            'message': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-area'}),
        }
        labels = {'file': 'Файл (pdf, docx, xls, zip, rar)'}


class SendRequest(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-request-input', 'placeholder': 'Email'}))
    phone = forms.CharField(validators=[
        RegexValidator(
            regex=r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$',
            message='Введите действительный номер',
            code="invalid_registration",
        )
    ], widget=forms.TextInput(attrs={'class': 'form-request-input', 'placeholder': 'Телефон'}))
