from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Cycling_events_app.models import Event, Bike


def create_event(event_name, limit):
    event_creator = User.objects.create(username='testuser')
    event_creator.set_password('12345')
    event_creator.save()
    return Event.objects.create(
        event_name=event_name,
        event_type=1,
        limit=limit,
        distance=150,
        route_description='test',
        date="2022-09-17 00:00:00.000000 +00:00",
        start='test',
        finish='test',
        event_creator=event_creator
    )


def create_event2(event_name, limit):
    event_creator = User.objects.create(username='testuser2')
    event_creator.set_password('12345')
    event_creator.save()
    return Event.objects.create(
        event_name=event_name,
        event_type=1,
        limit=limit,
        distance=150,
        route_description='test',
        date="2022-09-17 00:00:00.000000 +00:00",
        start='test',
        finish='test',
        event_creator=event_creator
    )


def create_bike():
    bike = Bike.objects.create(
        brand="testbike",
        model="testbike",
        bike_type=1,
        weight=8
    )
    return bike


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


class TestEditProfile(TestCase):
    """
    Modify view test.
    """

    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='12345')

    def test_profile_edit(self):
        profile = self.user.profile
        profile.age = 40
        profile.weight = 180
        self.client.login(username='test', password='12345')
        response = self.client.post(
            reverse('edit-profile'),
            {'age': '45', 'weight': 100})

        profile.refresh_from_db()
        self.assertEqual(profile.weight, 100)
        self.assertEqual(profile.age, 45)
        self.assertEqual(response.status_code, 302)

    def test_profile_no_edit(self):
        profile = self.user.profile

        self.client.login(username='test', password='12345')
        response = self.client.post(
            reverse('edit-profile'),
            {'age': '', 'weight': ''})

        profile.refresh_from_db()
        self.assertEqual(profile.weight, None)
        self.assertEqual(profile.age, None)
        self.assertEqual(response.status_code, 302)


class TestMyEventsView(TestCase):
    def setUp(self):
        self.client = Client()
        self.myevents_url = reverse('my-events')

    def test_anonymus_cannot_see_page(self):
        response = self.client.get(self.myevents_url)
        self.assertRedirects(response, '/accounts/login/?next=%2Fmy_events')

    def test_authenticated_user_can_see_page(self):
        user = User.objects.create_user(
            'TestUser', 'test@xyz.com', 'testpassword'
        )
        self.client.force_login(user=user)
        response = self.client.get(reverse('my-events'))
        self.assertEqual(response.status_code, 200)

    def test_display_events_created_by_user(self):
        event1 = create_event('test', 2)
        event2 = create_event2('test2', 2)
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('my-events'))
        self.assertQuerysetEqual(response.context['event_creator'], [event1])


class TestEventsView(TestCase):

    def setUp(self):
        self.client = Client()
        self.events_url = reverse('events')

    def test_event_list_GET(self):
        response = self.client.get(self.events_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events.html')

    def test_if_sorted(self):
        event1 = create_event('testb', 2)
        event2 = create_event2('testa', 2)
        response = self.client.get(self.events_url)
        self.assertQuerysetEqual(response.context['events'], [event2, event1])


class TestAddEditEventView(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_add_event_to_db(self):
        event2 = create_event('testname', 4)
        event1 = create_event2('testname2', 2)
        self.assertEqual(len(Event.objects.all()), 2)
        self.assertEqual(Event.objects.get(limit=4), event2)
        self.assertEqual(Event.objects.get(limit=2), event1)

    def test_event_edit(self):
        event_creator = User.objects.create(username='testuser2')
        event_creator.set_password('12345')
        event_creator.save()
        event = create_event('testname', 2)
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('edit-event', kwargs={'id': event.id}),
            {'event_name': 'test', 'distance': 100})

        self.assertEqual(response.status_code, 200)
        event.refresh_from_db()
        self.assertEqual(event.event_name, 'testname')
        self.assertEqual(event.distance, 150)


class TestEventSignupView(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.event = create_event('testname', 2)

    def test_event_signup(self):
        event = self.event
        user = User.objects.create_user(
            'TestUser', 'test@xyz.com', 'testpassword'
        )
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('event-signup', kwargs={"id": event.id}))
        self.assertEqual(len(event.event_participant.all()), 1)
        self.assertEqual(response.status_code, 302)

    def test_event_signup_if_limit(self):
        event = create_event2('testname', 0)
        user = User.objects.create_user(
            'TestUser', 'test@xyz.com', 'testpassword')
        self.client.force_login(user=user)
        response = self.client.get(
            reverse('event-signup', kwargs={"id": event.id}))
        self.assertEqual(len(event.event_participant.all()), 0)
        self.assertEqual(response.status_code, 302)

    def test_event_signup_if_already_signed(self):
        event = self.event
        user = User.objects.create_user(
            'TestUser', 'test@xyz.com', 'testpassword')
        self.client.force_login(user=user)
        self.client.get(reverse('event-signup', kwargs={"id": event.id}))
        self.client.get(reverse('event-signup', kwargs={"id": event.id}))
        self.assertEqual(len(event.event_participant.all()), 1)

    def test_event_signup_if_two_another_user(self):
        event = self.event
        user = User.objects.create_user(
            'TestUser', 'test@xyz.com', 'testpassword')
        user2 = User.objects.create_user(
            'TestUser2', 'test@xyz.com', 'testpassword')
        self.client.force_login(user=user)
        self.client.get(reverse('event-signup', kwargs={"id": event.id}))
        self.client.force_login(user=user2)
        self.client.get(reverse('event-signup', kwargs={"id": event.id}))
        self.assertEqual(len(event.event_participant.all()), 2)

    def test_event_signup_and_resignation(self):
        event = self.event
        user = User.objects.create_user(
            'TestUser', 'test@xyz.com', 'testpassword')
        self.client.force_login(user=user)
        self.client.get(reverse('event-signup', kwargs={"id": event.id}))
        response = self.client.get(
            reverse('event-resignation', kwargs={"id": event.id}))
        self.assertEqual(len(event.event_participant.all()), 0)
        self.assertEqual(response.status_code, 302)


class TestAddEditBike(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.bike = create_bike()

    def test_add_bike_to_db(self):
        response = self.client.get(reverse('add-bike'))
        self.assertEqual(len(Bike.objects.all()), 1)
        self.assertEqual(response.status_code, 200)

    def test_edit_bike(self):
        bike = self.bike
        response = self.client.post(
            reverse('edit-bike', kwargs={'id': bike.id}),
            {'brand': 'Trek',
             'model': 'Emonda',
             'bike_type': 1,
             'weight': 9,
             'image': ''})

        self.assertEqual(response.status_code, 302)
        bike.refresh_from_db()
        self.assertEqual(self.bike.brand, 'Trek')
        self.assertEqual(self.bike.weight, 9)
