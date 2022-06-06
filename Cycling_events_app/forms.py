from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import PasswordInput
import datetime
from Cycling_events_app.models import EVENT_TYPE, VOIVODESHIP_NAME, CATEGORY_NAME, Profile, Event, Bike

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


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=101)
    last_name = forms.CharField(max_length=101)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Hasło'
        self.fields['password2'].label = 'Potwierdź hasło'
        self.fields['first_name'].label = 'Imię'
        self.fields['last_name'].label = 'Nazwisko'
        self.fields['username'].label = 'Login'
        self.fields['email'].label = 'Adres e-mail'

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']



class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Adres Email',
        }
        widgets = {'email': forms.EmailInput}


class ProfileDetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'age', 'weight', 'region', 'image')
        labels = {
            'gender': 'Płeć',
            'age': 'Wiek',
            'weight': 'Waga',
            'region': 'Województwo',
            'image': 'Dodaj zdjęcie',
        }


class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('event_name', 'event_type', 'limit', 'distance', 'route_description', 'date', 'start', 'finish',
                  'region_name', 'categories')

        labels = { 'event_name':'Nazwa',
                   'event_type':'Typ',
                   'limit':'Limit miejsc',
                   'distance':'Długość trasy',
                   'route_description':'Opis Trasy',
                   'date':'Data wydarzenia',
                   'start':'Miejsce startu',
                   'finish':'Miejsce zakończenia',
                   'region_name':'Województwo',
                   'categories':'Typ roweru',
        }

        widgets = { 'date': forms.SelectDateWidget()}


class FilterEventsForm(forms.Form):
    region_name = forms.ChoiceField(choices=VOIVODESHIP_NAME, label="Region")
    event_type = forms.ChoiceField(choices=EVENT_TYPE, label="Typ wydarzenia")
    categories = forms.ChoiceField(choices=CATEGORY_NAME, label="Typ roweru")


class AddBikeForm(forms.ModelForm):
    class Meta:
        model = Bike
        fields = ('brand', 'model', 'bike_type', 'weight', 'image')
        labels = {
            'brand': 'Marka',
            'model': 'Model',
            'bike_type': 'Typ roweru',
            'weight': 'Waga',
            'image': 'Dodaj zdjęcie'
        }







