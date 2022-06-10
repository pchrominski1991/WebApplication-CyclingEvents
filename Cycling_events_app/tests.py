from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Cycling_events_app.models import Event, Category, Region

def create_event(limit):
    event_creator = User.objects.get(username='test')
    event_participant = User.objects.get(username='test2')
    return Event.objects.create(
        event_name='testname',
        event_type=1,
        limit=limit,
        distance=150,
        route_description='test',
        date="2022-09-17 00:00:00.000000 +00:00",
        start = 'test',
        finish = 'test',
        event_participant = event_participant,
        event_creator = event_creator
    )


def create_test_user(username, password):
    return User.objects.create_user(
        username=username,
        password=password
    )


class TestLoginSignupViews(TestCase):

    def test_signup(self):
        User.objects.create_user(
            username="username",
            password="password"
        )
        users = User.objects.all()
        self.assertEqual(users.count(), 1)

    def test_login(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        c = Client()
        logged_in = c.login(username='testuser', password='12345')
        self.assertTrue(logged_in)


class TestMyEventsView(TestCase):
    def setUp(self):
        self.client = Client()
        self.myevents_url = reverse('my-events')

    def test_anonymus_cannot_see_page(self):
         response = self.client.get(self.myevents_url)
         self.assertRedirects(response, '/accounts/login/?next=%2Fmy_events')

    def test_authenticated_user_can_see_page(self):
         user = User.objects.create_user('TestUser', 'test@xyz.com', 'testpassword')
         self.client.force_login(user=user)
         response = self.client.get(reverse('my-events'))
         self.assertEqual(response.status_code, 200)


class TestEventsView(TestCase):

    def setUp(self):
        self.client = Client()
        self.events_url = reverse('events')

    def test_event_list_GET(self):
        response = self.client.get(self.events_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events.html')







