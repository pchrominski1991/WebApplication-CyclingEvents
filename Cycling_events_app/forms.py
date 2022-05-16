from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput


class UserForm(forms.Form):
    username = forms.CharField(label='login')
    password = forms.CharField(widget=PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'login',
        }


