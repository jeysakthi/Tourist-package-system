from django import forms
from django.contrib.auth.models import User
from .models import Package


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class VendorRegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    company_name = forms.CharField()


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = [
            'title', 'description', 'price', 'duration', 'image',
            'expiry_date', 'location', 'is_top_package', 'is_budget_friendly'
        ]
