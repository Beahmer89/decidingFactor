from django.contrib import admin
from models import Location, SearchHistory, Restaurant, VisitHistory

# Register your models here.
admin.site.register(Location)
admin.site.register(SearchHistory)
admin.site.register(Restaurant)
admin.site.register(VisitHistory)
