from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserForm, AddEventForm, RegisterForm
from .models import Event, Category, Region
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        context = {
            'form': form
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/main_page/')
            else:
                form.add_error(None, 'Niepoprawny login lub hasło!')

        context = {
            'form': form
        }

        return render(request, 'login.html', context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class MainView(View):
    def get(self, request):
        return render(request=request, template_name='main_page.html')

class EventsView(View):
    def get(self, request):
        events = Event.objects.order_by('event_name')
        return render(request=request, template_name='events.html',context={
            "events": events
        })


class AddEventView(View):
    def get(self, request):
        form = AddEventForm()
        return render(request, 'add_event.html', {"form": form})

    def post(self, request):
        form = AddEventForm(request.POST)
        if form.is_valid():
            event_name = form.cleaned_data['event_name']
            event_type = form.cleaned_data['event_type']
            date = form.cleaned_data['date']
            limit = form.cleaned_data['limit']
            route_description = form.cleaned_data['route_description']
            start = form.cleaned_data['start']
            distance = form.cleaned_data['distance']
            finish = form.cleaned_data['finish']
            region_name = form.cleaned_data['region_name']
            categories = form.cleaned_data['categories']
            category = Category.objects.get(category_name=categories)
            region = Region.objects.get(voivodeship_name=region_name)
            event = Event.objects.create(event_name=event_name,
                                         event_type=event_type,
                                         date=date,
                                         limit=limit,
                                         route_description=route_description,
                                         distance=distance,
                                         start=start,
                                         finish=finish,
                                         event_creator=request.user,
                                         )
            event.region_name = region
            event.categories = category
            event.save()
            return redirect('/events/')
        return render(request, 'add_event.html', {"form": form})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main')
        return render(request, 'register.html', {'form': form})