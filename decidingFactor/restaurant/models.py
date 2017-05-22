from django.db import models
from django.contrib.auth.models import User


class Search(models.Model):
    user = models.ForeignKey(User, default=1)
    search_name = models.CharField(max_length=50, default=None)
    zip_code = models.IntegerField(default=0)
    city = models.CharField(max_length=50, blank=True)
    search_term = models.CharField(max_length=30, default=None)

    def __str__(self):
        return self.search_name


class Restaurant(models.Model):
    search = models.ForeignKey(Search, default=1)
    name = models.CharField(max_length=50, default=None)
    last_dining = models.DateField(default='null')
    times_gone = models.IntegerField(default=0)
    loved = models.BooleanField(default='False')
    liked = models.BooleanField(default='False')
    hated = models.BooleanField(default='False')
    trying = models.BooleanField('False')

    def __str__(self):
        return self.name
