from django.db import models
from django.contrib.auth.models import User

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

class Cyclist(models.Model):
    age = models.IntegerField()
    weight = models.IntegerField
    region = models.IntegerField(choices=CATEGORY_NAME)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):
    category_name = models.IntegerField(choices=CATEGORY_NAME)


class Region(models.Model):
    voivodeship_name = models.IntegerField(choices=CATEGORY_NAME)


class Event(models.Model):
    event_name = models.CharField('Nazwa wydarzenia:', max_length=128)
    event_type = models.IntegerField(choices=EVENT_TYPE)
    limit = models.IntegerField('Ilość miejsc:', blank=True)
    distance = models.FloatField()
    route_description = models.TextField()
    date = models.DateTimeField()
    start = models.CharField(max_length=128)
    finish = models.CharField(max_length=128)
    region_name = models.ForeignKey(Region, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    cyclist = models.ManyToManyField(Cyclist, blank=True)



class Bike(models.Model):
    brand = models.CharField('Marka roweru:', max_length=64)
    model = models.CharField('Model roweru:', max_length=64)
    type = models.IntegerField(choices=CATEGORY_NAME)
    weight = models.FloatField()
