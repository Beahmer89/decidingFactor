from django.db import models
from django.contrib.auth.models import User

import uuid


class Location(models.Model):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                   editable=False)
    city = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.city


class SearchHistory(models.Model):
    search_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 editable=False)
    user_id = models.ForeignKey(User)
    location_id = models.ForeignKey(Location)
    search_terms = models.CharField(max_length=30, null=True, default=None)

    def __str__(self):
        return self.search_terms


class Restaurant(models.Model):
    restaurant_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     editable=False)
    location_id = models.ForeignKey(Location)
    name = models.CharField(max_length=50, null=True, default=None)
    restaurant_type = models.CharField(max_length=50, null=True, default=None)
    price = models.CharField(max_length=10, null=True, default=None)

    def __str__(self):
        return self.name


class VisitHistory(models.Model):
    HATE = 'HATE'
    LIKE = 'LIKE'
    LOVE = 'LOVE'
    SAVE = 'SAVE'
    UNDECIDED = 'UNDECIDED'
    RATING = ((HATE, 'Hated'), (LIKE, 'Liked'), (LOVE, 'Loved'),
              (UNDECIDED, 'Undecided'), (SAVE, 'Saved'))

    user_id = models.ForeignKey(User)
    search_id = models.ForeignKey(SearchHistory)
    restaurant_id = models.ForeignKey(Restaurant)
    rating = models.CharField(max_length=10, default='undecided',
                              choices=RATING)
    last_visted = models.DateField(null=True, default=None)

    def __str__(self):
        return self.rating
