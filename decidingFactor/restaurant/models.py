from django.db import models
from django.contrib.auth.models import User

import uuid


class Location(models.Model):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                   editable=False)
    zip_code = models.IntegerField(default=0)
    city = models.CharField(max_length=50, blank=True)

    def __str__(self):
        if self.zip_code:
            return self.zip_code
        return self.city


class SearchHistory(models.Model):
    search_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 editable=False)
    location_id = models.ForeignKey(Location)
    search_terms = models.CharField(max_length=30, null=True, default=None)

    def __str__(self):
        return self.search_terms

class Restaurant(models.Model):
    restaurant_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)
    name = models.CharField(max_length=50, null=True, default=None)
    restaurant_type = models.CharField(max_length=50, null=True, default=None)
    price = models.CharField(max_length=10, null=True, default=None)

    def __str__(self):
        return self.name

class VisitHistory(models.Model):
    RATING = (('undecided', 'Undecided'), ('hate','Hated'),
              ('like','Liked'), ('love','Loved'))
    user_id = models.ForeignKey(User)
    search_id = models.ForeignKey(SearchHistory)
    restaurant_id = models.ForeignKey(Restaurant)
    rating = models.CharField(max_length=10, default='undecided', choices=RATING)
    last_visted = models.DateField(default='null')

    def __str__(self):
        return self.rating
