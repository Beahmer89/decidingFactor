from django.core import exceptions

from restaurant import models


def check_if_search_exists(user_id, search_location, terms):
    try:
        search = models.Location.objects.get(city=search_location,
                                             searchhistory__user_id=user_id,
                                             searchhistory__search_terms=terms)
    except exceptions.ObjectDoesNotExist:
        search = None

    return search


def save_form_info(user_id, search_location, terms):
    try:
        location = models.Location.objects.get(city=search_location)
    except exceptions.ObjectDoesNotExist:
        location = models.Location(city=search_location)
        location.save()

    search = models.SearchHistory(user_id=user_id, location_id=location,
                                  search_terms=terms)
    search.save()


def get_user_visit_history(user_id):
    return models.Restaurant.objects.filter(
        visithistory__user_id=user_id).values('restaurant_type', 'name',
                                              'visithistory__rating')
