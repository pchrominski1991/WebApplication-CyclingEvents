from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

CATEGORY_NAME = (
    (1, "rower szosowy"),
    (2, "MTB"),
    (3, "GRAVEL"),
    (4, "dowolny rower"),
)

VOIVODESHIP_NAME = (
    (1, "dolnośląskie"),
    (2, "kujawsko-pomorskie"),
    (3, "lubelskie"),
    (4, "lubuskie"),
    (5, "łódzkie"),
    (6, "małopolskie"),
    (7, "mazowieckie"),
    (8, "opolskie"),
    (9, "podkarpackie"),
    (10, "podlaskie"),
    (11, "pomorskie"),
    (12, "śląskie"),
    (13, "świętokrzyskie"),
    (14, "warmińsko-mazurskie"),
    (15, "wielkopolskie"),
    (16, "zachodniopomorskie"),
)

EVENT_TYPE = (
    (1, "wyścig"),
    (2, "trening"),
    (3, "coffee ride"),
)

GENDER_CHOICES = (
    ('M', 'mężczyzna'),
    ('F', 'kobieta')
)


class Bike(models.Model):
    """
    Stores a single Bike model.
    """
    brand = models.CharField('Marka roweru:', max_length=64)
    model = models.CharField('Model roweru:', max_length=64)
    bike_type = models.IntegerField(choices=CATEGORY_NAME)
    weight = models.FloatField()
    image = models.ImageField(upload_to='files/images', blank=True, null=True)


class Profile(models.Model):
    """
    Extend :model:`auth.User`.
    """
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    age = models.PositiveIntegerField(blank=True, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    region = models.IntegerField(choices=VOIVODESHIP_NAME, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True, max_length=15)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='files/images', blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """
        Create user profile after create user
        """
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        """
        Save profile instance
        """
        instance.profile.save()


class Category(models.Model):
    category_name = models.IntegerField(choices=CATEGORY_NAME)
    """
    Stores a single category.
    """
    def __str__(self):
        """
        Return category name as string
        """
        return self.get_category_name_display()


class Region(models.Model):
    """
    Stores a single region.
    """
    voivodeship_name = models.IntegerField(choices=VOIVODESHIP_NAME)

    def __str__(self):
        """
        Return voivodeship name as string
        """
        return self.get_voivodeship_name_display()


class Event(models.Model):
    """
    Stores a single event, related to
    :model:`Cycling_events_app.Region`,
    :model:`Cycling_events_app.Category`,
    :model:`Cycling_events_app.Profile` and
    :model:`auth.User`.
    """
    event_name = models.CharField('Nazwa wydarzenia:', max_length=128)
    event_type = models.IntegerField(choices=EVENT_TYPE)
    limit = models.IntegerField('Ilość miejsc:', blank=True)
    distance = models.FloatField()
    route_description = models.TextField()
    date = models.DateTimeField()
    start = models.CharField(max_length=128)
    finish = models.CharField(max_length=128)
    region_name = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    event_participant = models.ManyToManyField(Profile)
    event_creator = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
