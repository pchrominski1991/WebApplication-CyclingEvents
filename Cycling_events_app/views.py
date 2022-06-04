from collections import Counter
from itertools import count

from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserForm, AddEventForm, RegisterForm, UserDetailsForm, ProfileDetailsForm, EditEventForm, \
    FilterEventsForm
from .models import Event, Category, Region, Profile
from django.utils.translation import gettext as _



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
        messages.info(request, "Wylogowano się poprawnie.")
        return redirect('login')


class MainView(View):
    def get(self, request):
        return render(request=request, template_name='main_page.html')


class EventsView(View):
    def get(self, request):
        form = FilterEventsForm()
        events = Event.objects.order_by('event_name')
        return render(request=request, template_name='events.html', context={
            "events": events,
            "form": form,
        })

    def post(self, request):
        form = FilterEventsForm(request.POST)
        if form.is_valid():
            event_type = form.cleaned_data['event_type']
            region_name = form.cleaned_data['region_name']
            categories = form.cleaned_data['categories']
            events = Event.objects.filter(region_name=region_name).filter(categories=categories).filter(event_type=event_type)
            return render(request, 'events.html', {"form": form,
                                                   "events": events,
                                                   })


class AddEventView(LoginRequiredMixin, View):
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
            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')


class ProfileView(View):
    def get(self, request):
        user = request.user
        profiles = Profile.objects.get(user_id=user.id)
        return render(request=request, template_name='profile.html',context={
            "profiles": profiles
        })


class EditProfileView(View):
    def get(self, request):
        user_form = UserDetailsForm(instance=request.user)
        profile_form = ProfileDetailsForm(instance=request.user.profile)
        return render(request, 'edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        user_form = UserDetailsForm(request.POST, instance=request.user)
        profile_form = ProfileDetailsForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(self.request, 'zmieniono dane użytkownika')
            return HttpResponseRedirect(self.request.path_info)
        else:
            profile_form = ProfileDetailsForm(instance=request.user.profile)
        return render(request, 'profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })


class EventView(View):
    def get(self, request, id):
        event = Event.objects.get(id=id)
        user = User.objects.get(id=event.event_creator_id)
        participants = event.event_participant.count()
        avb = int(event.limit) - int(participants)
        return render(request=request, template_name='event_details.html', context={
            "event": event,
            "user": user,
            "avb": avb,
        })


class EditEventView(LoginRequiredMixin,View):
    def get(self, request, id):
        event = Event.objects.get(id=id)
        if request.user.id == event.event_creator_id:
            form = EditEventForm(instance=event)
            return render(request, 'edit_event.html', {"form": form})
        else:
            return redirect(f'/event_details/{id}/')

    def post(self, request, id):
        event = Event.objects.get(id=id)
        form = EditEventForm(request.POST, instance=event)
        if form.is_valid():
            return redirect(f'/event_details/{id}/')
        return render(request, 'edit_event.html', {"form": form})




class MyEventsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user_id=user.id)
        event_creator = Event.objects.filter(event_creator_id=user.id).order_by('event_name')
        my_event = Event.objects.filter(event_participant=profile).order_by('event_name')
        return render(request=request, template_name='my_events.html', context={"event_creator": event_creator,
                                                                                "my_event": my_event,
                                                                                })


class EventSignupView(LoginRequiredMixin, View):
    def get(self, request, id):
        user = request.user
        event = Event.objects.get(id=id)
        event.event_participant.add(request.user.profile)
        return redirect("my-events")


class EventResignationView(View):
    def get(self, request, id):
        user = request.user
        event = Event.objects.get(id=id)
        event.event_participant.remove(user.profile)
        return redirect("my-events")


class ParticipantsView(View):
    def get(self, request, id):
        event = Event.objects.get(id=id)
        participants = event.event_participant.all()
        return render(request, "participants.html", context={"participants": participants})