"""Cycling_events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Cycling_events_app.views import LoginView, MainView, EventsView, AddEventView, LogoutView, RegisterView, \
    ProfileView, EditProfileView, EventView, EditEventView, MyEventsView, EventResignationView, \
    EventSignupView, ParticipantsView, AddBikeView, BikeDetailsView, EditBikeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(), name='login'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('main_page/', MainView.as_view(), name='main'),
    path('events/', EventsView.as_view(), name='events'),
    path('add_event/', AddEventView.as_view(), name='add-events'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit-profile'),
    path('event_details/<str:id>/', EventView.as_view(), name='event-details'),
    path('event_signup/<str:id>/', EventSignupView.as_view(), name='event-signup'),
    path('edit_event/<str:id>/', EditEventView.as_view(), name='edit-event'),
    path('my_events', MyEventsView.as_view(), name='my-events'),
    path('event_resignation/<str:id>/', EventResignationView.as_view(), name='event-signup'),
    path('participants/<str:id>/', ParticipantsView.as_view(), name='participants'),
    path('add_bike/', AddBikeView.as_view(), name='add-bike'),
    path('bike_details/<str:id>/', BikeDetailsView.as_view(), name='bike_details'),
    path('edit_bike/<str:id>/', EditBikeView.as_view(), name='bike_details'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
