from django import forms
from main.models import Subscriber, Package, TVPackage, Equipment, Additional
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class TVPackageChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    package = forms.ModelChoiceField(queryset=Package.objects.all())
    tv_package = TVPackageChoiceField(queryset=TVPackage.objects.all(), label='TV тариф')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторити Пароль')
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={'data-theme': 'light'},  # Можете настроить внешний вид капчи
        )
    )
    class Meta:
        model = Subscriber
        fields = ['name', 'email', 'phone', 'address', 'package', 'tv_package', 'password']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['package'].empty_label = None
        self.fields['tv_package'].empty_label = None



class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={'data-theme': 'light'},  # Можете настроить внешний вид капчи
        )
    )

class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount')