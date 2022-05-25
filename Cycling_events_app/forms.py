from django import forms
from django.contrib.auth import get_user_model
from django.forms import PasswordInput
import datetime
from Cycling_events_app.models import EVENT_TYPE, VOIVODESHIP_NAME, CATEGORY_NAME


User = get_user_model()


def present_or_future_date(value):
    if value < datetime.date.today():
        raise forms.ValidationError("Nie można podać daty z przeszłości!")
    return value


def only_positive_distance(value):
    if value <= 0:
        raise forms.ValidationError("Dystans musi być większy od 0")
    return value



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
    date = forms.DateField(label="Data wydarzenia", widget=forms.SelectDateWidget, validators=[present_or_future_date])
    distance = forms.FloatField(label="Długość trasy", min_value=0, validators=[only_positive_distance])
    route_description = forms.CharField(widget=forms.Textarea, label="Opis trasy")
    start = forms.CharField(max_length=128, label="Miejsce startu")
    finish = forms.CharField(max_length=128, label="Miejsce końca trasy")
    region_name = forms.ChoiceField(choices=VOIVODESHIP_NAME, label="Region")
    categories = forms.ChoiceField(choices=CATEGORY_NAME, label="Typ roweru")


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Nazwa użytkownika')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')




