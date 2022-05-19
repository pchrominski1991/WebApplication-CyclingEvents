from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput

from Cycling_events_app.models import EVENT_TYPE, VOIVODESHIP_NAME, CATEGORY_NAME


class UserForm(forms.Form):
    username = forms.CharField(label='login')
    password = forms.CharField(label='hasło', widget=PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'login',
        }


class AddEventForm(forms.Form):
    event_name = forms.CharField(max_length=128, label="Podaj nazwę wydarzenia")
    event_type = forms.ChoiceField(choices=EVENT_TYPE, label="Podaj typ wydarzenia")
    limit = forms.IntegerField(label="Podaj limit miejsc")
    distance = forms.FloatField(label="Długość trasy")
    route_description = forms.CharField(widget=forms.Textarea, label="Opis trasy")
    start = forms.CharField(max_length=128, label="Miejsce startu")
    finish = forms.CharField(max_length=128, label="Miejsce końca trasy")
    region_name = forms.ChoiceField(choices=VOIVODESHIP_NAME, label="Region")
    categories = forms.ChoiceField(choices=CATEGORY_NAME, label="Typ roweru")
