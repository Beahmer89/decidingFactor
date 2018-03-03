from django.contrib import admin

import restaurant.models as models

# Register your models here.
admin.site.register(models.Location)
admin.site.register(models.SearchHistory)
admin.site.register(models.Restaurant)
admin.site.register(models.VisitHistory)
