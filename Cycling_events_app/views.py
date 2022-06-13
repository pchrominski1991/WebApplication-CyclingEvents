from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserForm, AddEventForm, RegisterForm, UserDetailsForm,\
    ProfileDetailsForm, EditEventForm, FilterEventsForm, AddBikeForm
from .models import Event, Category, Region, Profile, Bike

User = get_user_model()


class LoginView(View):
    """
    Display view to log in user.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests: to display log in form.
        """
        form = UserForm()
        context = {
            'form': form
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: to authenticate user.
        """
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(
                    request,
                    f'Pomyślnie zalogowano użytkownika {user.username}'
                )
                return redirect('/main_page/')
            else:
                form.add_error(None, 'Niepoprawny login lub hasło!')

        context = {
            'form': form
        }

        return render(request, 'login.html', context)


class LogoutView(View):
    """
    View to log out user from app.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests: to log out user from app.
        """
        logout(request)
        messages.success(request, "Wylogowano się poprawnie.")
        return redirect('login')


class MainView(View):
    """
    View to display main page.
    """
    def get(self, request):
        """
        Handle GET requests: to display main page..
        """
        return render(request=request, template_name='main_page.html')


class EventsView(View):
    """
    View display events.
    """
    def get(self, request):
        """
        Handle get request:
        to display all added events sorted by event_name
        """
        form = FilterEventsForm()
        events = Event.objects.order_by('event_name')
        return render(request=request, template_name='events.html', context={
            "events": events,
            "form": form,
        })

    def post(self, request):
        """
        Handle POST requests:
        to filter events through: event_type, region name, categories.
        """
        form = FilterEventsForm(request.POST)
        if form.is_valid():
            event_type = form.cleaned_data['event_type']
            region_name = form.cleaned_data['region_name']
            categories = form.cleaned_data['categories']
            events = Event.objects.filter(region_name=region_name)\
                .filter(categories=categories)\
                .filter(event_type=event_type)
            return render(request, 'events.html', {"form": form,
                                                   "events": events,
                                                   })


class AddEventView(LoginRequiredMixin, View):
    """
    Display view to add new event.
    """
    def get(self, request):
        """
        Handle GET requests: to display add event form.
        """
        form = AddEventForm()
        return render(request, 'add_event.html', {"form": form})

    def post(self, request):
        """
        Create new event object with the passed
        POST variables.
        """
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
            messages.success(
                request,
                f'Dodałeś wydarzenie {event.event_name} do bazy.'
            )
            return redirect('/events/')
        return render(request, 'add_event.html', {"form": form})


class RegisterView(View):
    """
    Display view to register user in app.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests: to display add event form.
        """
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
        """
        Create new user with the passed
        POST variables.
        """
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Konto zostało pomyślnie zarejestrowane. Możesz się zalogować!'
            )
            return redirect('login')
        else:
            messages.error(
                request,
                "Rejestracja nie powiodła się. Wypełnij poprawnie formularz."
            )
        context = {
            'form': form
        }
        return render(request, 'register.html', context)


class ProfileView(View):
    """
    Display view with user profile.
    """
    def get(self, request):
        """
        Handle GET requests: to display user profile.
        """
        user = request.user
        profiles = Profile.objects.get(user_id=user.id)
        bike = profiles.bike
        return render(request=request, template_name='profile.html', context={
            "profiles": profiles,
            "bike": bike
        })


class EditProfileView(View):
    """
    Display view to edit user profile.
    """
    def get(self, request):
        """
        Handle GET requests: to display edit user profile.
        """
        user_form = UserDetailsForm(instance=request.user)
        profile_form = ProfileDetailsForm(instance=request.user.profile)
        return render(request, 'edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request):
        """
        Handle POST requests: to update user profile.
        """
        user_form = UserDetailsForm(request.POST, instance=request.user)
        profile_form = ProfileDetailsForm(request.POST or None,
                                          request.FILES or None,
                                          instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(self.request, 'Zmieniono dane użytkownika.')
            return HttpResponseRedirect(self.request.path_info)
        else:
            profile_form = ProfileDetailsForm(instance=request.user.profile)
        return render(request, 'profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })


class EventView(View):
    """
    Display view single event.
    """
    def get(self, request, id):
        """
        Handle GET requests:
        to display event details with the limit of available places.
        """
        event = Event.objects.get(id=id)
        user = User.objects.get(id=event.event_creator_id)
        participants = event.event_participant.count()
        avb = int(event.limit) - int(participants)
        return render(
               request=request,
               template_name='event_details.html',
               context={
                "event": event,
                "user": user,
                "avb": avb,
               })


class EditEventView(LoginRequiredMixin, View):
    """
    Display view to edit event.
    """
    def get(self, request, id):
        """
        Handle GET requests: to display edited event.
        """
        event = Event.objects.get(id=id)
        if request.user.id == event.event_creator_id:
            form = EditEventForm(instance=event)
            return render(request, 'edit_event.html', {"form": form})
        else:
            return redirect(f'/event_details/{id}/')

    def post(self, request, id):
        """
        Handle POST requests: to update event.
        """
        event = Event.objects.get(id=id)
        form = EditEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Pomyślnie zmieniono informacje o wydarzeniu."
            )
            return redirect(f'/event_details/{id}/')
        return render(request, 'edit_event.html', {"form": form})


class MyEventsView(LoginRequiredMixin, View):
    """
    Display view with user events.
    """
    def get(self, request):
        """
        Handle GET requests: to display user events.
        """
        user = request.user
        profile = Profile.objects.get(user_id=user.id)
        event_creator = Event.objects.filter(
            event_creator_id=user.id).order_by('event_name')
        my_event = Event.objects.filter(
            event_participant=profile).order_by('event_name')
        return render(
            request=request,
            template_name='my_events.html',
            context={"event_creator": event_creator,
                     "my_event": my_event
                     })


class EventSignupView(LoginRequiredMixin, View):
    """
    View to sign up for the event
    """
    def get(self, request, id):
        """
        Handle GET requests: to sign up for the events,
        with checking that the limit is not exceeded
        and that the user is not already signed up.
        """
        event = Event.objects.get(id=id)
        participants = event.event_participant.all()
        if (int(event.limit) - int(participants.count())) > 0:
            if request.user.profile not in participants:
                event.event_participant.add(request.user.profile)
                messages.success(
                    request,
                    f'Pomyślnie zapisałeś się na {event.event_name}.'
                )
                return redirect("my-events")
            else:
                messages.error(request, "Jesteś już zapisany na to wydarzenie")
                return redirect('events')
        else:
            messages.error(
                request,
                "Limit miejsc na to wydarzenie został wyczerpany"
            )
            return redirect('events')


class EventResignationView(View):
    """
    View used to cancel the event
    """
    def get(self, request, id):
        """
        Handle GET requests: to cancel participation in event.
        """
        user = request.user
        event = Event.objects.get(id=id)
        event.event_participant.remove(user.profile)
        messages.success(
            request,
            f'Zrezygnowałeś z udziału w wydarzeniu {event.event_name}.'
        )
        return redirect("my-events")


class ParticipantsView(View):
    """
    Display view with the list of participants.
    """
    def get(self, request, id):
        event = Event.objects.get(id=id)
        participants = event.event_participant.all()
        return render(request, "participants.html",
                      context={"participants": participants})


class AddBikeView(View):
    """
    Display view to add new bike.
    """
    def get(self, request):
        """
        Handle GET requests: to display add bike form.
        """
        form = AddBikeForm()
        return render(request, 'add_bike.html', {"form": form})

    def post(self, request):
        """
        Create new announcement object with the passed
        POST variables.
        """
        form = AddBikeForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            brand = form.cleaned_data['brand']
            model = form.cleaned_data['model']
            bike_type = form.cleaned_data['bike_type']
            weight = form.cleaned_data['weight']
            image = form.cleaned_data['image']
            bike = Bike.objects.create(brand=brand,
                                       model=model,
                                       bike_type=bike_type,
                                       weight=weight,
                                       image=image)
            bike.save()
            user = request.user
            user.profile.bike = bike
            user.save()
            messages.success(request, 'Dodałeś rower do bazy')
            return redirect('/profile/')
        return render(request, 'add_bike.html', {"form": form})


class BikeDetailsView(View):
    """
    Display view single bike.
    """
    def get(self, request, id):
        bike = Bike.objects.get(id=id)
        return render(request, "bike.html", context={"bike": bike})


class EditBikeView(View):
    """
    Display view to edit event.
    """
    def get(self, request, id):
        """
        Handle GET requests: to display edited bike.
        """
        bike = Bike.objects.get(id=id)
        form = AddBikeForm(instance=bike)
        return render(request, 'add_bike.html', {"form": form})

    def post(self, request, id):
        """
        Handle POST requests: to update event.
        """
        bike = Bike.objects.get(id=id)
        form = AddBikeForm(request.POST or None,
                           request.FILES or None,
                           instance=bike)
        if form.is_valid():
            form.save()
            bike.save()
            messages.success(request, 'Zmieniłeś dane roweru')
            return redirect(f'/bike_details/{id}/')
        return render(request, 'add_bike.html', {"form": form})


class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')
