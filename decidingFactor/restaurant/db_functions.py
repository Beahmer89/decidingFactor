import datetime

from django import db
from django.core import exceptions

from restaurant import models


def check_if_search_exists(user_id, search_location, terms):
    """
    Checks to see if user has used this search before. If they have the search
    is returned and if not None is returned.

    :param int user_id: logged in user id
    :param str search_location: the area in which user is searching
    :param str terms: string user entered to search for restaurants

    :return: search object or None
    """
    try:
        search = models.Location.objects.get(city=search_location,
                                             searchhistory__user_id=user_id,
                                             searchhistory__search_terms=terms)
    except exceptions.ObjectDoesNotExist:
        search = None

    return search


def save_search_form_info(user_id, search_location, terms):
    """
    Saves the search information that was used entered at the restaurant search
    page. If the location has not already been saved in the DB, it will be
    created in this fuction.

    :param int user_id: logged in user id
    :param str search_location: the area in which user is searching
    :param str terms: string user entered to search for restaurants
    """
    location, created = models.Location.objects.get_or_create(
        city=search_location)

    search = models.SearchHistory(user_id=user_id, location_id=location,
                                  search_terms=terms)
    search.save()


def save_restaurant_selection(name, location_id, price, restaurant_type):
    """
    Adds the given restaurant to the database.

    :param str location_id: location uuid of where restaurant is located
    :param str name: The name of the restaurant
    :param str price: Money signs indicating price range
    :param str restaurant_type: Category of restaurant

    :return: Restaurant object or None
    """
    try:
        restaurant, created = models.Restaurant.objects.get_or_create(
            name=name,
            location_id=location_id,
            restaurant_type=restaurant_type,
            price=price)
    except db.IntegrityError as error:
        return None

    return restaurant


def get_user_visit_history(user_id):
    return models.Restaurant.objects.filter(
        visithistory__user_id=user_id).values('restaurant_type', 'name',
                                              'visithistory__rating')
